import numpy as np
import cv2
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import gc
import tensorflow as tf

# --- Global Variables Loaded Once at Server Startup ---
MODEL_PATH = "fingerprint_bloodgroup_model.keras"
IMG_SIZE = 128
CLASSES = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']

# Load the model outside of the prediction function for fast inference
try:
    GLOBAL_MODEL = load_model(MODEL_PATH)
    print("Model loaded successfully for serving.")
except Exception as e:
    print(f"Error loading model: {e}")
    GLOBAL_MODEL = None

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_and_crop_thumb(image_array):
    """
    Detect the thumb region from image and crop to optimal size.
    Uses edge detection and contour analysis.
    
    Args:
        image_array: Grayscale numpy array (any size)
    
    Returns:
        Cropped and resized 128x128 image, or None if detection fails
    """
    try:
        # Ensure image is grayscale
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        
        h, w = image_array.shape
        
        # 1. Binary threshold to isolate fingerprint area
        binary = cv2.adaptiveThreshold(image_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 15, 2)
        
        # 2. Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        # 3. Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # 4. Find largest contour (thumb region)
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        # Sanity check: contour should be reasonable size
        if area < (h * w * 0.05):  # At least 5% of image
            return None
        
        # 5. Get bounding rectangle
        x, y, w_bbox, h_bbox = cv2.boundingRect(largest_contour)
        
        # 6. Add padding and center the crop
        padding = max(w_bbox, h_bbox) * 0.1
        x = max(0, int(x - padding))
        y = max(0, int(y - padding))
        w_bbox = min(w - x, int(w_bbox + 2 * padding))
        h_bbox = min(h - y, int(h_bbox + 2 * padding))
        
        # 7. Crop to square region
        size = max(w_bbox, h_bbox)
        x_end = min(w, x + size)
        y_end = min(h, y + size)
        
        cropped = image_array[y:y_end, x:x_end]
        
        # 8. Resize to model input size
        resized = cv2.resize(cropped, (IMG_SIZE, IMG_SIZE))
        
        return resized
    
    except Exception as e:
        print(f"Thumb detection error: {str(e)}")
        return None

def predict_blood_group(image_bytes, use_thumb_detection=True):
    """
    Handles preprocessing and prediction for a single uploaded image.

    Args:
        image_bytes: The raw image data (e.g., a byte stream from a web upload).
        use_thumb_detection: Whether to use smart thumb detection/cropping

    Returns:
        The predicted blood group and its confidence score.
    """
    if GLOBAL_MODEL is None:
        return "Error: Model not loaded.", 0.0

    try:
        # 1. Decode image from bytes
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return "Error: Could not decode image.", 0.0

        # 2. Optional: Smart thumb detection and cropping for better accuracy
        if use_thumb_detection:
            detected_thumb = detect_and_crop_thumb(img)
            if detected_thumb is not None:
                img = detected_thumb
            else:
                # Fallback to simple resizing if detection fails
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        else:
            # Simple resize without detection
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        
        # 3. Enhance fingerprint image: Apply contrast enhancement
        # CLAHE (Contrast Limited Adaptive Histogram Equalization) improves ridge pattern visibility
        # This matches the training data processing and significantly improves accuracy
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        
        # 4. Apply sharpening kernel to enhance ridge details for better model accuracy
        # This helps the model detect fine fingerprint patterns just like in the training reference
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]]) / 1.0
        img = cv2.filter2D(img, -1, kernel)
        
        # 5. Clip values to valid range [0, 255] after enhancement
        img = np.clip(img, 0, 255).astype(np.uint8)
        
        # 6. Reshape and Normalize: (1, 128, 128, 1) and scale to 0-1
        input_array = img.reshape(1, IMG_SIZE, IMG_SIZE, 1).astype(np.float32) / 255.0
        
        # Free memory
        del img, nparr
        gc.collect()

        # 4. Predict with memory optimization
        with tf.device('/CPU:0'):
            predictions = GLOBAL_MODEL.predict(input_array, verbose=0, batch_size=1)[0]
        
        # 5. Decode results
        predicted_index = np.argmax(predictions)
        predicted_class = CLASSES[predicted_index]
        confidence = float(predictions[predicted_index] * 100)
        
        # Free memory
        del input_array, predictions
        gc.collect()

        return predicted_class, confidence
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return f"Error: Prediction failed - {str(e)}", 0.0

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def api_predict():
    """API endpoint for fingerprint blood group prediction."""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Please upload an image.'}), 400

        # Get user details from form
        name = request.form.get('name', 'N/A').strip()
        age = request.form.get('age', 'N/A').strip()
        gender = request.form.get('gender', 'N/A').strip()
        contact = request.form.get('contact', 'N/A').strip()

        # Read image bytes
        image_bytes = file.read()
        
        if not image_bytes:
            return jsonify({'success': False, 'error': 'Empty file uploaded'}), 400
        
        # Predict blood group
        predicted_class, confidence = predict_blood_group(image_bytes)

        # Check for errors in prediction
        if "Error" in predicted_class:
            print(f"Prediction error returned: {predicted_class}")
            return jsonify({'success': False, 'error': predicted_class}), 500

        # Save uploaded file
        filename = secure_filename(file.filename)
        name_part = name.replace(' ', '_')[:20] if name != 'N/A' else 'unknown'
        filename = f"{name_part}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.seek(0)
        file.save(filepath)

        response = {
            'success': True,
            'blood_group': predicted_class,
            'confidence': f"{confidence:.2f}%",
            'name': name,
            'age': age,
            'gender': gender,
            'contact': contact,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Force garbage collection
        gc.collect()
        
        return jsonify(response), 200

    except Exception as e:
        print(f"API error: {str(e)}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    model_status = "loaded" if GLOBAL_MODEL is not None else "not_loaded"
    return jsonify({'status': 'ok', 'model': model_status}), 200

if __name__ == '__main__':
    # For local development with LocalTunnel sharing
    port = int(os.environ.get('PORT', 5000))
    
    # Use threaded mode for better local performance
    # This allows multiple concurrent requests
    app.run(
        debug=False,
        host='0.0.0.0',  # Listen on all network interfaces
        port=port,
        threaded=True,   # Enable threading for concurrent requests
        use_reloader=False  # Disable reloader (causes issues with model loading)
    )
