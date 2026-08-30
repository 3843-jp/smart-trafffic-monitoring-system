# Smart Traffic Monitoring System

A production-ready web application for real-time vehicle speed detection and license plate recognition using YOLOv8, centroid tracking, and Tesseract OCR. Deployed on Streamlit Community Cloud.

## 🌟 Features

- **🚗 Vehicle Detection**: YOLOv8 Nano for accurate real-time vehicle detection (cars, motorcycles, buses, trucks)
- **📊 Speed Estimation**: Centroid tracking algorithm for frame-to-frame speed calculation
- **📷 License Plate Recognition**: Contour-based plate detection with Tesseract OCR
- **🚨 Speed Enforcement**: Real-time alerts for vehicles exceeding speed limits
- **📈 HUD Dashboard**: Live statistics including vehicle count, speeding violations, and FPS
- **📹 Video Output**: Download processed video with annotations
- **🌐 Web Interface**: User-friendly Streamlit interface for video upload and processing

## 🏗️ System Architecture

```
Streamlit Web Application
├── Video Upload (MP4, AVI, MOV)
├── YOLOv8 Vehicle Detection
├── Centroid Tracking
├── Speed Calculation
├── License Plate OCR (Tesseract)
└── Results Display & Video Download
```

## 📋 Technologies

- **Python 3.8+**
- **Streamlit**: Web framework for data applications
- **YOLOv8**: Object detection (Ultralytics)
- **OpenCV**: Computer vision processing
- **Tesseract OCR**: License plate text recognition
- **NumPy & imutils**: Image and array operations

## 🚀 Quick Start

### Local Installation

#### Prerequisites
- Python 3.8+
- pip package manager

#### Step 1: Clone the Repository
```bash
git clone https://github.com/3843-jp/smart-trafffic-monitoring-system.git
cd smart-trafffic-monitoring-system
```

#### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Install Tesseract OCR

**Windows:**
- Download installer from [tesseract-ocr/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- Run the installer (default path: `C:\Program Files\Tesseract-OCR`)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

#### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## ☁️ Streamlit Community Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Community Cloud account (free at https://streamlit.io/cloud)

### Deployment Steps

1. **Push to GitHub**
   - Fork or push this repository to your GitHub account

2. **Deploy on Streamlit Cloud**
   - Go to [Streamlit Community Cloud](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch, and main file (`app.py`)
   - Click "Deploy"

3. **Configuration**
   - The application includes `packages.txt` for system dependencies (tesseract-ocr)
   - The application includes `requirements.txt` for Python packages
   - `.streamlit/config.toml` provides UI customization

4. **Access Your App**
   - Your app will be available at: `https://share.streamlit.io/YOUR_USERNAME/smart-trafffic-monitoring-system`

## 📖 Usage

### Web Interface

1. **Upload Video**
   - Click "Choose a traffic video" to upload an MP4, AVI, MOV, MKV, or FLV file
   - Maximum file size: 500 MB (Streamlit Cloud limit)

2. **Configure Settings**
   - **Speed Limit**: Set the target speed limit (10-200 km/h)
   - **Meters per Pixel**: Calibration factor for speed calculation (default: 0.05)

3. **Process Video**
   - Click "Process Video" to start analysis
   - Progress will be displayed in real-time
   - Processing time depends on video length and cloud resources

4. **View Results**
   - **Total Vehicles Detected**: Count of unique vehicles tracked
   - **Speeding Vehicles**: Count of vehicles exceeding speed limit
   - **Unique Plates Detected**: Count of distinct license plates recognized
   - **Detected License Plates**: List of extracted plate numbers

5. **Download Processed Video**
   - After processing, download the annotated video with:
     - Bounding boxes (color-coded by speed)
     - Vehicle IDs and speed information
     - License plate text overlay
     - HUD with statistics

## ⚙️ Configuration

### Speed Limit Calibration

The speed calculation depends on accurate calibration of **meters per pixel**:

```
Speed (km/h) = (pixel_distance × meters_per_pixel) / time_interval × 3.6
```

**To calibrate:**
1. Measure a known distance in your video (e.g., lane width = 3.7 m)
2. Adjust the "Meters per Pixel" slider until speed estimates seem reasonable
3. Typically: 0.03-0.08 for highway videos

### YOLOv8 Confidence Threshold

Default: 0.45 (45% confidence)
- Lower values: More detections, more false positives
- Higher values: Fewer detections, higher precision

### Tracking Parameters

- **MAX_TRACK_HISTORY**: Frames to keep in vehicle history (default: 30)
- **MIN_SPEED_FRAMES**: Minimum frames needed to compute speed (default: 5)
- **DISAPPEAR_LIMIT**: Frames before removing disappeared track (default: 15)

## 🎨 Output Color Scheme

- 🟢 **Green**: Vehicle within speed limit
- 🔴 **Red**: Vehicle speeding (over limit)
- 🟡 **Yellow**: Speed still computing

## 📊 Display Information

### HUD Dashboard
- Total vehicles detected
- Speeding violations count
- Current speed limit
- Vehicles with speed computing
- Real-time FPS

### Per-Vehicle Information
- Unique ID
- Current speed (km/h)
- Status (OK / SPEEDING / Computing)
- License plate (if detected)
- Tracking trail (trajectory path)

## 🔍 Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- FLV (.flv)

## ⚠️ Important Notes

### Speed Estimation Accuracy

Speed measurements depend on:
- ✅ Accurate camera calibration (meters_per_pixel)
- ✅ Clear video quality and lighting
- ✅ Stable camera position (no panning/zooming)
- ✅ Sufficient frame rate (≥20 FPS recommended)

Speed estimates are **demonstration-quality** and should not be used for legal enforcement without proper calibration and validation.

### License Plate Recognition

OCR accuracy:
- Best with clear, well-lit plates
- Typical accuracy: ~70-85% on clear plates
- Factors affecting accuracy:
  - Plate angle and distance from camera
  - Lighting conditions
  - Vehicle height in frame (>100px recommended)
  - Plate cleanliness and visibility

### Performance Considerations

- **CPU-based processing**: Streamlit Cloud uses CPU-only instances
- **Processing time**: 1-5 minutes per minute of video (depends on resolution)
- **File size limit**: 500 MB upload limit on Streamlit Cloud
- **Memory**: Limited to ~1 GB per app instance
- **Timeout**: Apps have max runtime limits; long videos may fail

### Known Limitations

- Single camera setup only
- Speed accuracy depends heavily on calibration
- Real-time processing limited by cloud CPU resources
- Large video files may timeout
- No database persistence (results not saved between sessions)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Video upload fails | Ensure file is <500 MB and in supported format |
| No vehicles detected | Lower detection confidence or check video quality |
| Tesseract error | Tesseract should auto-install; restart app if needed |
| Slow processing | Use lower resolution or shorter video clips |
| Poor speed accuracy | Recalibrate meters_per_pixel using reference distances |
| License plates not detected | Ensure vehicles are >100px tall in frame |
| App timeout | Process shorter videos or retry with lower resolution |

## 📈 Performance Metrics

- **Detection**: YOLOv8 Nano (~5-10 FPS on CPU for 720p)
- **Tracking**: Centroid-based (very fast, <1ms per frame)
- **Speed Accuracy**: ±10-15% (depends on calibration)
- **Plate Recognition**: ~70-85% accuracy on clear plates
- **Overall FPS**: 1-5 FPS typical (CPU-limited)

## 🔄 How It Works

### Detection & Tracking
1. **Frame Input**: Read video frame by frame
2. **YOLOv8 Detection**: Detect vehicles in each frame
3. **Centroid Calculation**: Calculate center point of bounding box
4. **Euclidean Matching**: Match centroids between frames using distance
5. **ID Assignment**: Assign unique ID to each vehicle

### Speed Calculation
1. **History Tracking**: Keep last N centroid positions for each vehicle
2. **Pixel Distance**: Calculate movement in pixels between frames
3. **Conversion**: Multiply by calibration factor (meters_per_pixel)
4. **Time Division**: Divide by elapsed time to get speed
5. **Unit Conversion**: Convert m/s to km/h (×3.6)

### License Plate Recognition
1. **Bounding Box Extraction**: Extract vehicle region
2. **Preprocessing**: Gray, filter, Canny edge detection
3. **Contour Analysis**: Find rectangular shapes (potential plates)
4. **Segmentation**: Isolate plate region from vehicle
5. **Tesseract OCR**: Extract text using Tesseract
6. **Cleanup**: Remove non-alphanumeric characters

## 📝 Example Workflow

```bash
# Local development
streamlit run app.py

# Upload traffic_video.mp4
# Set speed limit to 60 km/h
# Click "Process Video"
# Wait for processing
# Download output video and review results
```

## 🔐 Privacy & Legal

**⚠️ Important Disclaimer:**
This system is for **educational and authorized traffic monitoring purposes only**. Ensure compliance with:
- Local privacy laws and regulations
- Data protection regulations (GDPR, CCPA, etc.)
- Consent requirements for video recording and processing
- Traffic authority guidelines
- Camera placement and monitoring restrictions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit:
- Bug reports
- Feature requests
- Performance improvements
- Better OCR implementations
- Multi-camera support ideas

## 📜 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created for intelligent traffic monitoring systems education and demonstration.

## 🚀 Future Improvements

- [ ] Multi-camera support
- [ ] Deep SORT for better tracking
- [ ] EasyOCR for improved plate recognition
- [ ] Database integration for violation logging
- [ ] Real-time alerts via email/SMS
- [ ] GPU support for faster processing
- [ ] Historical analytics dashboard
- [ ] Batch processing mode
- [ ] API endpoint for external integration

## 📞 Support

For issues, questions, or suggestions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Known Limitations](#known-limitations)
3. Open an issue on GitHub
4. Check Streamlit documentation

---

**Note**: This system is a demonstration of computer vision techniques. Speed measurements are not legally accurate without proper calibration and validation for traffic enforcement purposes.
