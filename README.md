# 🩸 Fingerprint-Based Blood Group Detection

![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20+-ff6f00?style=flat-square&logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask)
![Accuracy](https://img.shields.io/badge/Accuracy-84%25-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> **Deep learning model predicting blood groups from fingerprints with 84% accuracy**

## 🌟 Key Highlights

- ✅ **84% Accuracy** across all 8 blood group types
- ✅ **Lightweight Model** - Only 434 KB (ideal for edge deployment)
- ✅ **Fast Inference** - ~1-2 seconds per prediction
- ✅ **Beautiful Web UI** - 3-step process with drag-and-drop
- ✅ **Production-Ready** - Flask backend with comprehensive error handling

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Test Accuracy | 84% |
| F1-Score | 0.84 |
| Model Size | 434 KB |
| Parameters | 111,112 |
| Training Time | 46 epochs |

**Per-Class Results:**
- **A+**: 90% Precision, 91% Recall
- **B-**: 83% Precision, **94% Recall** ⭐
- **O-**: **94% Precision**, 94% Recall ⭐
- **O+**: 94% Precision, 73% Recall
- All other classes: 80-90% range

---

## 🏗️ Architecture Overview

```
Input (128×128×1)
  ↓
Conv32 → BatchNorm → MaxPool → Conv64 → BatchNorm → MaxPool
  ↓
Conv128 → BatchNorm → MaxPool → GlobalAvgPool
  ↓
Dense(128, ReLU, Dropout=0.5) → Dense(8, Softmax)
  ↓
Output: 8 Blood Groups
```

**Training:**
- Optimizer: RMSprop (lr=0.0005)
- Loss: Categorical Crossentropy
- Batch Size: 32
- Data Augmentation: Rotation ±5°, Zoom ±5%, Shift ±12%
- Class Weights: Balanced for imbalanced dataset
- Early Stopping: Patience=10

---

## 🚀 Installation & Usage

### 1️⃣ Setup (2 minutes)
```bash
git clone https://github.com/MalikShujaatAli/Blood-Group-Detection-using-Fingerprints.git
cd "FingerPrint Based Bloodgroup"
pip install -r requirements.txt
```

### 2️⃣ Run
```bash
python app.py
# Open http://localhost:5000 in browser
```

### 3️⃣ Use
1. Enter personal details (Name, Age, Gender, Contact)
2. Upload grayscale fingerprint image (PNG, JPG, etc.)
3. Get instant blood group prediction + confidence score
4. Download report

---

## ✨ Features

**Web App:**
- 🎯 Intuitive 3-step process
- 📷 Drag-and-drop image upload with preview
- 📊 Real-time results with confidence percentage
- 📥 Download test report
- 📱 Fully responsive design
- 🎨 Modern gradient UI

**Backend:**
- ⚡ Model loads once at startup (optimized)
- 🔒 File validation & secure handling
- 📝 Timestamped file storage
- 🏥 Clean API endpoints

---

## 📁 Project Structure

```
FingerPrint Based Bloodgroup/
├── app.py                                 (Flask backend)
├── fingerprint_bloodgroup_model.keras     (Trained model - 434 KB)
├── requirements.txt                       (Dependencies)
├── README.md                              (This file)
├── templates/
│   └── index.html                         (Web UI)
└── uploads/                               (Storage - auto-created)
```

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Flask 3.0.0 |
| **ML** | TensorFlow/Keras 2.20.0 |
| **Image Processing** | OpenCV 4.12.0.88 |
| **Frontend** | HTML5, CSS3, Vanilla JS |
| **Model Format** | Keras (.keras) |

---

## ⚙️ Configuration

**Change Port:**
```python
# Edit app.py, line ~122
app.run(port=8080)  # Default: 5000
```

**Adjust Upload Size:**
```python
# Edit app.py, line ~20
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Default: 16MB
```

---

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not loading | Check `fingerprint_bloodgroup_model.keras` exists |
| Port 5000 in use | `netstat -ano \| findstr :5000` then kill process |
| Upload fails | Verify image format (PNG/JPG) and size < 16MB |
| Slow prediction | Check RAM available, close other apps |

---

## 📊 Dataset & Training

**Dataset:**
- Source: Kaggle Fingerprint Blood Group
- Total: 6,000+ images
- Classes: 8 blood group types (A+, A-, B+, B-, AB+, AB-, O+, O-)
- Format: 128×128 grayscale

**Training Results:**
- Epoch 1: 39.4% accuracy
- Epoch 32: 82.25% validation accuracy
- Epoch 46: **84.25% best validation** (early stopped)

---

## ⚠️ Disclaimer

⚠️ **For educational and research purposes only**
- NOT for clinical blood group determination
- Always perform actual blood tests for medical use
- Consult qualified medical professionals
- Accuracy varies with image quality

---

## 📄 License & Author

**MIT License** © 2025 Malik Shujaat Ali

**GitHub:** [@MalikShujaatAli](https://github.com/MalikShujaatAli)
**Repo:** [Blood-Group-Detection](https://github.com/MalikShujaatAli/Blood-Group-Detection-using-Fingerprints)

---

<div align="center">

**⭐ Found this helpful? Star the repo!**

Made with ❤️ by Malik Shujaat Ali

</div>
