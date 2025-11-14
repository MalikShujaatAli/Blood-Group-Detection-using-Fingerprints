import numpy as np
import cv2
from tensorflow.keras.models import load_model
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from datetime import datetime

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

def predict_blood_group(image_bytes):
    """
    Handles preprocessing and prediction for a single uploaded image.

    Args:
        image_bytes: The raw image data (e.g., a byte stream from a web upload).

    Returns:
        The predicted blood group and its confidence score.
    """
    if GLOBAL_MODEL is None:
        return "Error: Model not loaded.", 0.0

    # 1. Decode image from bytes
    # Convert image bytes to a numpy array, then decode as a grayscale image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return "Error: Could not decode image.", 0.0

    # 2. Resize and Preprocess
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    
    # 3. Reshape and Normalize: (1, 128, 128, 1) and scale to 0-1
    input_array = img.reshape(1, IMG_SIZE, IMG_SIZE, 1) / 255.0

    # 4. Predict
    # verbose=0 suppresses the prediction output log
    predictions = GLOBAL_MODEL.predict(input_array, verbose=0)[0]
    
    # 5. Decode results
    predicted_index = np.argmax(predictions)
    predicted_class = CLASSES[predicted_index]
    confidence = float(predictions[predicted_index] * 100)  # Convert to percentage

    return predicted_class, confidence

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
        
        # Predict blood group
        predicted_class, confidence = predict_blood_group(image_bytes)

        # Check for errors in prediction
        if "Error" in predicted_class:
            return jsonify({'success': False, 'error': predicted_class}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        name_part = name.replace(' ', '_')[:20] if name != 'N/A' else 'unknown'
        filename = f"{name_part}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.seek(0)
        file.save(filepath)

        return jsonify({
            'success': True,
            'blood_group': predicted_class,
            'confidence': f"{confidence:.2f}%",
            'name': name,
            'age': age,
            'gender': gender,
            'contact': contact,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    model_status = "loaded" if GLOBAL_MODEL is not None else "not_loaded"
    return jsonify({'status': 'ok', 'model': model_status}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
