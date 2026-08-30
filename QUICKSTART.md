# Quick Start Guide

Fast setup for local development and testing.

## 🚀 Local Development (5 minutes)

### Prerequisites
```bash
# Python 3.8+
python --version

# Git
git --version
```

### Install & Run

**Linux/Mac:**
```bash
# 1. Clone repository
git clone https://github.com/3843-jp/smart-trafffic-monitoring-system.git
cd smart-trafffic-monitoring-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Tesseract (Linux)
sudo apt-get update
sudo apt-get install tesseract-ocr

# 5. Run app
streamlit run app.py
```

**Windows:**
```bash
# 1. Clone repository
git clone https://github.com/3843-jp/smart-trafffic-monitoring-system.git
cd smart-trafffic-monitoring-system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Tesseract
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to default location: C:\Program Files\Tesseract-OCR

# 5. Run app
streamlit run app.py
```

### Access App
```
http://localhost:8501
```

---

## 📹 Quick Test

1. **Prepare test video** (10-30 seconds, MP4 format, 480p)
2. **Upload** via web interface
3. **Set speed limit**: 60 km/h
4. **Set calibration**: 0.05 meters/pixel
5. **Click**: "Process Video"
6. **Wait**: 30-60 seconds
7. **Download**: Processed video

Expected results:
- ✅ Vehicles detected (bounding boxes)
- ✅ Vehicle IDs assigned
- ✅ Speed estimated (if moving)
- ✅ Plates detected (if visible)

---

## ☁️ Streamlit Cloud Deployment (10 minutes)

### 1. Push to GitHub
```bash
git add .
git commit -m "Production ready"
git push origin main
```

### 2. Deploy
- Go to https://share.streamlit.io
- Click "New app"
- Select repository and main file (app.py)
- Click "Deploy"

### 3. Share
```
https://share.streamlit.io/YOUR_USERNAME/smart-trafffic-monitoring-system
```

---

## 🔧 Troubleshooting

### Module not found
```bash
pip install -r requirements.txt
```

### Tesseract not found (Windows)
- Install from https://github.com/UB-Mannheim/tesseract/wiki
- Default path works automatically

### Tesseract not found (Linux)
```bash
sudo apt-get install tesseract-ocr
```

### Video won't process
- Ensure video is MP4/AVI/MOV
- Check file size < 500 MB
- Try smaller resolution/duration

### No vehicles detected
- Check video quality
- Verify lighting
- Try different confidence threshold

---

## 📚 Full Documentation

- **README.md** - Features, architecture, configuration
- **DEPLOYMENT.md** - Streamlit Cloud setup guide
- **CONVERSION_SUMMARY.md** - Technical conversion details

---

## 💡 Tips

- **Test locally first** before cloud deployment
- **Use small test videos** (10-30 seconds)
- **Monitor cloud logs** after deployment
- **Recalibrate** meters_per_pixel for better accuracy

---

**Ready?** Run `streamlit run app.py` and test your first video! 🎬
