"""
Smart Traffic Monitoring System - Streamlit Web Application
===========================================================

A production-ready Streamlit application for video-based traffic monitoring.
Features: YOLOv8 vehicle detection, centroid tracking, speed estimation, 
license plate OCR, and speed enforcement alerts.

Compatible with: Streamlit Community Cloud and Linux environments
"""

import streamlit as st
import cv2
import numpy as np
import tempfile
import time
from pathlib import Path
from collections import defaultdict, deque
import math
import re

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

import imutils

# ───────��─────────────────── PAGE CONFIG ────────────────────────────────

st.set_page_config(
    page_title="Smart Traffic Monitoring System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 Smart Traffic Monitoring System")
st.markdown("""
A real-time vehicle speed detection and license plate recognition system using 
YOLOv8, centroid tracking, and Tesseract OCR.
""")

# ─────────────────────────── CONFIGURATION ────────────────────────────────

CONF_THRESHOLD = 0.45
VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
MAX_TRACK_HISTORY = 30
DISAPPEAR_LIMIT = 15
MIN_SPEED_FRAMES = 5
OCR_INTERVAL = 20

# Colors (BGR)
COLOR_OK = (0, 220, 0)          # Green
COLOR_SPEEDING = (0, 0, 255)    # Red
COLOR_ZERO = (0, 200, 255)      # Yellow

FONT = cv2.FONT_HERSHEY_SIMPLEX


# ─────────────────────────── HELPERS ─────────────────────────────────────

def euclidean(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def get_speed_color(speed_kmh, has_history):
    """Return BGR color based on speed state."""
    if not has_history:
        return COLOR_ZERO
    if speed_kmh > st.session_state.speed_limit:
        return COLOR_SPEEDING
    return COLOR_OK


def extract_plate_text(roi):
    """Extract license plate text from ROI using Tesseract OCR."""
    if not TESSERACT_AVAILABLE or roi is None or roi.size == 0:
        return ""
    
    try:
        roi_resized = imutils.resize(roi, width=400)
        gray = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)
        
        cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        
        plate_roi = gray
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                plate_roi = gray[y:y + h, x:x + w]
                break
        
        plate_big = cv2.resize(plate_roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        _, plate_thresh = cv2.threshold(plate_big, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        config = "--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        text = pytesseract.image_to_string(plate_thresh, config=config)
        text = re.sub(r"[^A-Z0-9]", "", text.upper()).strip()
        return text
    except Exception as e:
        st.warning(f"OCR error: {e}")
        return ""


def draw_box(frame, x1, y1, x2, y2, color, label):
    """Draw bounding box with label."""
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    lbl_size, _ = cv2.getTextSize(label, FONT, 0.55, 2)
    cv2.rectangle(frame, (x1, y1 - lbl_size[1] - 6), (x1 + lbl_size[0] + 4, y1), color, -1)
    cv2.putText(frame, label, (x1 + 2, y1 - 4), FONT, 0.55, (255, 255, 255), 2)


def draw_speed_alert(frame, obj_id, speed_kmh, plate_text, x1, y1, has_history):
    """Draw speed info and plate text above bounding box."""
    color = get_speed_color(speed_kmh, has_history)
    
    if not has_history:
        status = "Computing..."
        speed_str = "-- km/h"
    else:
        over_limit = speed_kmh > st.session_state.speed_limit
        status = "!! SPEEDING !!" if over_limit else "OK"
        speed_str = f"{speed_kmh:.1f} km/h"
    
    info = f"ID:{obj_id} | {speed_str} | {status}"
    if plate_text:
        info += f" | Plate: {plate_text}"
    
    cv2.putText(frame, info, (x1, y1 - 28), FONT, 0.5, color, 2)


def draw_hud(frame, tracked_ids, speed_store, computed_ids, speeding_count, fps_val):
    """Draw HUD with statistics on top-left panel."""
    total = len(tracked_ids)
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (370, 100), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    
    cv2.putText(frame, f"Vehicles detected  : {total}",
                (10, 22), FONT, 0.55, (200, 200, 200), 1)
    cv2.putText(frame, f"Speeding vehicles  : {speeding_count}",
                (10, 44), FONT, 0.55, COLOR_SPEEDING if speeding_count > 0 else (200, 200, 200), 1)
    cv2.putText(frame, f"Speed limit        : {st.session_state.speed_limit} km/h",
                (10, 66), FONT, 0.55, (180, 180, 180), 1)
    cv2.putText(frame, f"Computing speed for: {total - len(computed_ids)} vehicle(s)",
                (10, 88), FONT, 0.45, COLOR_ZERO, 1)
    
    cv2.putText(frame, f"FPS: {fps_val:.1f}",
                (frame.shape[1] - 100, 22), FONT, 0.55, (100, 255, 100), 1)


# ─────────────────────────── CENTROID TRACKER ───────────────────────────────

class CentroidTracker:
    """Track vehicle centroids across frames using distance-based matching."""
    
    def __init__(self, max_disappeared=DISAPPEAR_LIMIT):
        self.next_id = 0
        self.objects = {}
        self.disappeared = defaultdict(int)
        self.max_disappeared = max_disappeared
    
    def register(self, centroid):
        """Register a new object centroid."""
        self.objects[self.next_id] = centroid
        self.next_id += 1
    
    def deregister(self, obj_id):
        """Remove an object by ID."""
        del self.objects[obj_id]
        del self.disappeared[obj_id]
    
    def update(self, detections):
        """Update tracker with new detections."""
        if not detections:
            for obj_id in list(self.disappeared):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)
            return self.objects
        
        if not self.objects:
            for c in detections:
                self.register(c)
            return self.objects
        
        obj_ids = list(self.objects.keys())
        obj_centroids = list(self.objects.values())
        
        D = np.zeros((len(obj_centroids), len(detections)))
        for r, oc in enumerate(obj_centroids):
            for c, dc in enumerate(detections):
                D[r, c] = euclidean(oc, dc)
        
        rows = D.min(axis=1).argsort()
        cols = D.argmin(axis=1)[rows]
        
        used_rows, used_cols = set(), set()
        for r, c in zip(rows, cols):
            if r in used_rows or c in used_cols:
                continue
            obj_id = obj_ids[r]
            self.objects[obj_id] = detections[c]
            self.disappeared[obj_id] = 0
            used_rows.add(r)
            used_cols.add(c)
        
        for r in set(range(len(obj_centroids))) - used_rows:
            obj_id = obj_ids[r]
            self.disappeared[obj_id] += 1
            if self.disappeared[obj_id] > self.max_disappeared:
                self.deregister(obj_id)
        
        for c in set(range(len(detections))) - used_cols:
            self.register(detections[c])
        
        return self.objects


# ─────────────────────────── VIDEO PROCESSING ───────────────────────────────

def process_video(input_video_path, output_video_path, speed_limit, meters_per_pixel, progress_callback=None):
    """
    Process video and return detection results.
    
    Args:
        input_video_path: Path to input video file
        output_video_path: Path to save processed video
        speed_limit: Speed limit in km/h
        meters_per_pixel: Calibration factor for speed calculation
        progress_callback: Callback function for progress updates
    
    Returns:
        Dictionary with statistics about the processing
    """
    
    # Check if dependencies are available
    if not ULTRALYTICS_AVAILABLE:
        st.error("❌ Ultralytics YOLO not available. Please check installation.")
        return None
    
    try:
        # Load model
        if progress_callback:
            progress_callback("Loading YOLOv8 model...")
        model = YOLO("yolov8n.pt")
        
        # Open video
        if progress_callback:
            progress_callback("Opening video file...")
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            st.error(f"❌ Cannot open video: {input_video_path}")
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_video_path, fourcc, fps, (w, h))
        
        # Initialize tracking and detection structures
        tracker = CentroidTracker()
        centroid_hist = defaultdict(lambda: deque(maxlen=MAX_TRACK_HISTORY))
        speed_store = defaultdict(float)
        computed_ids = set()
        plate_store = defaultdict(str)
        plate_timer = defaultdict(int)
        
        # Statistics
        frame_count = 0
        t_prev = time.time()
        display_fps = 0.0
        all_vehicle_ids = set()
        all_speeding_ids = set()
        all_plate_texts = []
        
        if progress_callback:
            progress_callback(f"Processing {total_frames} frames...")
        
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_idx += 1
            frame_count += 1
            
            # Update FPS
            t_now = time.time()
            if t_now - t_prev >= 0.5:
                display_fps = frame_count / max(t_now - t_prev, 1e-6)
                t_prev = t_now
                frame_count = 0
            
            # YOLOv8 detection
            results = model.predict(source=[frame], conf=CONF_THRESHOLD, verbose=False)
            detections_obj = results[0].boxes
            
            vehicle_detections = []
            if detections_obj is not None:
                for box in detections_obj:
                    cls_id = int(box.cls.numpy()[0])
                    if cls_id not in VEHICLE_CLASSES:
                        continue
                    conf = float(box.conf.numpy()[0])
                    x1, y1, x2, y2 = map(int, box.xyxy.numpy()[0])
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    vehicle_detections.append((cx, cy, x1, y1, x2, y2, cls_id, conf))
            
            # Update tracking
            centroids_only = [(d[0], d[1]) for d in vehicle_detections]
            tracked = tracker.update(centroids_only)
            
            det_map = {}
            for d in vehicle_detections:
                cx, cy = d[0], d[1]
                for obj_id, tc in tracked.items():
                    if tc == (cx, cy):
                        det_map[obj_id] = d
                        break
            
            speeding_count = 0
            
            # Process each tracked vehicle
            for obj_id, centroid in tracked.items():
                all_vehicle_ids.add(obj_id)
                
                centroid_hist[obj_id].append((centroid, time.time()))
                hist = centroid_hist[obj_id]
                
                has_history = obj_id in computed_ids
                
                # Speed computation
                if len(hist) >= MIN_SPEED_FRAMES:
                    (prev_cx, prev_cy), t0 = hist[0]
                    (curr_cx, curr_cy), t1 = hist[-1]
                    dt = t1 - t0
                    if dt > 0:
                        pixel_dist = euclidean((prev_cx, prev_cy), (curr_cx, curr_cy))
                        meters = pixel_dist * meters_per_pixel
                        speed_ms = meters / dt
                        speed_kmh = speed_ms * 3.6
                        speed_store[obj_id] = speed_kmh
                        computed_ids.add(obj_id)
                        has_history = True
                
                speed_kmh = speed_store.get(obj_id, 0.0)
                
                # Count speeding
                if has_history and speed_kmh > speed_limit:
                    speeding_count += 1
                    all_speeding_ids.add(obj_id)
                
                # Draw bounding box
                if obj_id in det_map:
                    cx, cy, x1, y1, x2, y2, cls_id, conf = det_map[obj_id]
                    label = f"{VEHICLE_CLASSES[cls_id]} {conf:.2f}"
                    box_color = get_speed_color(speed_kmh, has_history)
                    
                    draw_box(frame, x1, y1, x2, y2, box_color, label)
                    
                    # OCR
                    plate_timer[obj_id] += 1
                    if plate_timer[obj_id] % OCR_INTERVAL == 1:
                        roi = frame[max(0, y1):y2, max(0, x1):x2]
                        text = extract_plate_text(roi)
                        if text:
                            plate_store[obj_id] = text
                            all_plate_texts.append(text)
                    
                    plate_text = plate_store.get(obj_id, "")
                    draw_speed_alert(frame, obj_id, speed_kmh, plate_text, x1, y1, has_history)
                
                # Trail
                pts = [h[0] for h in hist]
                for i in range(1, len(pts)):
                    cv2.line(frame, pts[i - 1], pts[i], (255, 180, 0), 1)
            
            draw_hud(frame, list(tracked.keys()), speed_store, computed_ids, speeding_count, display_fps)
            
            # Write frame
            writer.write(frame)
            
            # Progress update
            if progress_callback and frame_idx % 30 == 0:
                progress_callback(f"Processing frame {frame_idx}/{total_frames}")
        
        cap.release()
        writer.release()
        
        # Prepare results
        results_dict = {
            "total_vehicles": len(all_vehicle_ids),
            "speeding_vehicles": len(all_speeding_ids),
            "unique_plates": len(set(all_plate_texts)),
            "plates": list(set(all_plate_texts)),
            "output_path": output_video_path,
            "success": True
        }
        
        return results_dict
    
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        return None


# ─────────────────────────── SESSION STATE ──────────────────────────────────

if "speed_limit" not in st.session_state:
    st.session_state.speed_limit = 60

if "meters_per_pixel" not in st.session_state:
    st.session_state.meters_per_pixel = 0.05


# ─────────────────────────── SIDEBAR ─────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.session_state.speed_limit = st.slider(
        "Speed Limit (km/h)",
        min_value=10,
        max_value=200,
        value=st.session_state.speed_limit,
        step=5
    )
    
    st.session_state.meters_per_pixel = st.slider(
        "Meters per Pixel (Calibration)",
        min_value=0.01,
        max_value=0.5,
        value=st.session_state.meters_per_pixel,
        step=0.01,
        help="Adjust this based on your camera's field of view. Default: 0.05"
    )
    
    st.markdown("---")
    st.subheader("ℹ️ About")
    st.markdown("""
    **Smart Traffic Monitoring System**
    
    - 🎯 YOLOv8 vehicle detection
    - 📊 Centroid tracking
    - ⚡ Speed estimation
    - 📷 License plate OCR
    - 🚨 Speed alerts
    """)
    
    st.markdown("---")
    st.subheader("📝 Tips")
    st.info("""
    1. Upload a traffic video (MP4, AVI, MOV)
    2. Configure speed limit
    3. Click "Process Video"
    4. Wait for results
    5. Download processed video
    """)


# ─────────────────────────── MAIN INTERFACE ──────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Upload Video")
    uploaded_file = st.file_uploader(
        "Choose a traffic video",
        type=["mp4", "avi", "mov", "mkv", "flv"]
    )

with col2:
    st.subheader("⚙️ Processing Settings")
    st.info(f"""
    **Current Configuration:**
    - Speed Limit: {st.session_state.speed_limit} km/h
    - Meters/Pixel: {st.session_state.meters_per_pixel}
    - YOLOv8 Confidence: {CONF_THRESHOLD}
    """)

st.markdown("---")

# Process button
if uploaded_file is not None:
    st.subheader("🎬 Process Video")
    
    if st.button("▶️ Process Video", key="process_btn"):
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_input:
            tmp_input.write(uploaded_file.read())
            input_path = tmp_input.name
        
        # Output path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_output:
            output_path = tmp_output.name
        
        # Progress tracking
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        def update_progress(msg):
            status_placeholder.write(msg)
        
        # Process video
        with st.spinner("🔄 Processing video... This may take a while."):
            results = process_video(
                input_path,
                output_path,
                st.session_state.speed_limit,
                st.session_state.meters_per_pixel,
                progress_callback=update_progress
            )
        
        if results and results.get("success"):
            st.success("✅ Video processed successfully!")
            
            # Display results
            st.subheader("📊 Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Vehicles Detected", results["total_vehicles"])
            with col2:
                st.metric("Speeding Vehicles", results["speeding_vehicles"])
            with col3:
                st.metric("Unique Plates Detected", results["unique_plates"])
            
            # License plates
            if results["plates"]:
                st.subheader("📷 Detected License Plates")
                plate_cols = st.columns(3)
                for i, plate in enumerate(results["plates"]):
                    with plate_cols[i % 3]:
                        st.write(f"**{plate}**")
            
            # Video playback
            st.subheader("🎥 Processed Video")
            try:
                with open(output_path, "rb") as f:
                    video_bytes = f.read()
                st.video(video_bytes)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Processed Video",
                    data=video_bytes,
                    file_name="processed_traffic_video.mp4",
                    mime="video/mp4"
                )
            except Exception as e:
                st.error(f"Error displaying video: {e}")
        
        # Clean up temp files
        try:
            Path(input_path).unlink()
            Path(output_path).unlink()
        except:
            pass

else:
    st.info("👆 Upload a video file to get started")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
Smart Traffic Monitoring System v1.0 | 
<a href='https://github.com/3843-jp/smart-trafffic-monitoring-system'>GitHub</a>
</div>
""", unsafe_allow_html=True)
