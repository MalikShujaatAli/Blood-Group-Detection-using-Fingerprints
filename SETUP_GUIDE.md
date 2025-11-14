# Fingerprint Based Blood Group Detection - Web Application

A web application that uses a trained deep learning model to predict blood groups from fingerprint images.

## Features

- **User-Friendly Interface**: Simple 3-step process (Personal Info → Upload Image → Results)
- **Real-time Prediction**: Fast fingerprint analysis using pre-trained Keras model
- **Report Generation**: Download test reports with all details
- **Image Preview**: See the uploaded fingerprint before analysis
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Comprehensive validation and error messages

## Project Structure

```
FingerPrint Based Bloodgroup/
├── app.py                           # Flask backend server
├── fingerprint_bloodgroup_model.keras # Trained model
├── requirements.txt                 # Python dependencies
├── templates/
│   └── index.html                  # Web interface
└── uploads/                         # Uploaded images (auto-created)
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Model File

Make sure `fingerprint_bloodgroup_model.keras` is in the project root directory.

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Enter Personal Information**
   - Full Name
   - Age
   - Gender
   - Contact Number

2. **Upload Fingerprint Image**
   - Click or drag-drop a fingerprint image
   - Supported formats: PNG, JPG, GIF, BMP, TIFF
   - Preferably grayscale images for best results
   - Preview the image before submission

3. **Check Blood Group**
   - Click "Check Blood Group" button
   - Wait for analysis
   - View results with confidence score

4. **View & Download Report**
   - See personal details and results
   - Download report as text file
   - Start a new test if needed

## Technical Details

### Backend Architecture

- **Framework**: Flask (Python web framework)
- **Model Loading**: Model is loaded once at server startup for optimal performance
- **Image Processing**: 
  - Images are decoded from bytes
  - Converted to grayscale
  - Resized to 128×128 pixels
  - Normalized to 0-1 range
  
### Supported Blood Groups

The model predicts 8 blood group types:
- A+, A-
- B+, B-
- AB+, AB-
- O+, O-

### API Endpoints

- `GET /` - Main application page
- `POST /predict` - Prediction endpoint
  - Parameters: name, age, gender, contact (form), file (image)
  - Returns: blood_group, confidence, timestamp
- `GET /health` - Health check endpoint

## File Upload Specifications

- **Max File Size**: 16 MB
- **Supported Formats**: PNG, JPG, JPEG, GIF, BMP, TIFF
- **Recommended**: Grayscale fingerprint images
- **Resolution**: Higher resolution images work better but will be resized to 128×128

## Troubleshooting

### Model Not Loading
- Verify `fingerprint_bloodgroup_model.keras` exists in the project root
- Check model file is not corrupted
- Ensure TensorFlow is properly installed

### Port Already in Use
- Change port in `app.py` line: `app.run(debug=True, host='0.0.0.0', port=5000)`
- Or stop the process using the port

### Image Upload Issues
- Ensure image is a valid image file
- Check file size is under 16 MB
- Try a different image format

## Model Information

- **Input Size**: 128×128 grayscale images
- **Output**: 8-class blood group classification
- **Preprocessing**: Normalization to 0-1 range
- **Confidence**: Percentage-based confidence score

## Security Notes

- File uploads are saved with timestamps to prevent collisions
- Filenames are sanitized using `secure_filename`
- Maximum file size is limited to 16 MB
- Only specific image formats are allowed

## Performance

- **Model Loading Time**: ~2-5 seconds (one-time at startup)
- **Prediction Time**: ~1-2 seconds per image
- **Concurrent Users**: Depends on server resources

## Notes

- This application is for demonstration purposes
- Blood group predictions should be verified with actual blood tests for medical use
- Always consult medical professionals for clinical purposes

## License

Refer to LICENSE file in the project directory.

## Support

For issues or questions, please check the troubleshooting section or contact the development team.
