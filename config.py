"""
Configuration module for Speed Detection System
Centralize all configuration parameters here for easy management
"""

# ─────────────────────────── VIDEO PATHS ────────────────────────────────────

VIDEO_PATH   = r"C:\Users\admin\Desktop\jp\py_ds\project\opencv\ocr\ultralytics\videos\video1.mp4"
COCO_TXT     = r"C:\Users\admin\Desktop\jp\py_ds\project\opencv\ocr\ultralytics\utils\coco.txt"
WEIGHTS_PATH = "weights/yolov8n.pt"
OUTPUT_PATH  = "output_speed_plate.avi"

# Tesseract configuration (adjust for your OS)
# Windows: r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Linux/Mac: "/usr/bin/tesseract" or just "tesseract"
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ─────────────────────────── SPEED SETTINGS ────────────────────────────────

SPEED_LIMIT_KMH = 60          # Speed limit threshold (km/h)
METERS_PER_PIXEL = 0.05       # Calibrate this value using calibration tool
FPS_OVERRIDE = None           # Override video FPS (None = auto-detect)

# ─────────────────────────── DETECTION SETTINGS ─────────────────────────────

CONF_THRESHOLD = 0.45         # YOLOv8 confidence threshold (0.0-1.0)

# Vehicle classes to detect (from COCO dataset)
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle", 
    5: "bus",
    7: "truck"
}

# ─────────────────────────── TRACKING SETTINGS ──────────────────────────────

MAX_TRACK_HISTORY = 30        # Max frames to keep in centroid history
DISAPPEAR_LIMIT = 15          # Frames before removing disappeared track
MIN_SPEED_FRAMES = 5          # Minimum frames needed to compute speed

# ─────────────────────────── DISPLAY SETTINGS ───────────────────────────────

DISPLAY_WINDOW = True         # Show live preview window
FONT = None                   # Will be set to cv2.FONT_HERSHEY_SIMPLEX in main

# ─────────────────────────── COLOR SCHEME ───────────────────────────────────

COLOR_OK       = (0, 220, 0)      # Green  – within speed limit
COLOR_SPEEDING = (0, 0, 255)      # Red    – exceeding speed limit  
COLOR_ZERO     = (0, 200, 255)    # Yellow – speed still computing

# ─────────────────────────── OCR SETTINGS ───────────────────────────────────

OCR_INTERVAL = 20             # Perform OCR every N frames
OCR_CONFIG = "--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# ─────────────────────────── CALIBRATION SETTINGS ───────────────────────────

LANE_WIDTH_METERS = 3.7       # Standard lane width used for calibration
