"""
Real-Time Vehicle Speed Detection + License Plate Recognition
=============================================================
- YOLOv8 for vehicle detection
- Centroid tracking for speed estimation
- Contour-based license plate detection
- Pytesseract OCR for plate number reading
- Speed limit enforcement alerts
"""

import random
import time
import math
import re
from collections import defaultdict, deque

import cv2
import numpy as np
import pytesseract
import imutils
from ultralytics import YOLO

# ─────────────────────────── CONFIGURATION ──────────────────────────────────

# Tesseract configuration (adjust path for your OS)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

VIDEO_PATH   = r"C:\Users\admin\Desktop\jp\py_ds\project\opencv\ocr\ultralytics\videos\video1.mp4"
COCO_TXT     = r"C:\Users\admin\Desktop\jp\py_ds\project\opencv\ocr\ultralytics\utils\coco.txt"
WEIGHTS_PATH = "weights/yolov8n.pt"
OUTPUT_PATH  = "output_speed_plate.avi"

SPEED_LIMIT_KMH   = 60
METERS_PER_PIXEL  = 0.05
FPS_OVERRIDE      = None

CONF_THRESHOLD    = 0.45
VEHICLE_CLASSES   = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

MAX_TRACK_HISTORY = 30
DISAPPEAR_LIMIT   = 15
MIN_SPEED_FRAMES  = 5

DISPLAY_WINDOW    = True
FONT              = cv2.FONT_HERSHEY_SIMPLEX

# ── Colors ──
COLOR_OK       = (0, 220, 0)      # Green  – within limit
COLOR_SPEEDING = (0, 0, 255)      # Red    – over limit
COLOR_ZERO     = (0, 200, 255)    # Yellow – speed not yet computed


# ─────────────────────────── HELPERS ────────────────────────────────────────

def load_classes(path: str) -> list[str]:
    """Load class names from COCO dataset file."""
    with open(path, "r") as f:
        return f.read().strip().split("\n")


def random_colors(n: int) -> list[tuple]:
    """Generate n random BGR colors."""
    return [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for _ in range(n)]


def euclidean(p1, p2) -> float:
    """Calculate Euclidean distance between two points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def get_speed_color(speed_kmh: float, has_history: bool) -> tuple:
    """Return BGR color based on speed state."""
    if not has_history:
        return COLOR_ZERO       # Still computing
    if speed_kmh > SPEED_LIMIT_KMH:
        return COLOR_SPEEDING   # RED – over limit
    return COLOR_OK             # GREEN – within limit


# ─────────────────────────── CENTROID TRACKER ───────────────────────────────

class CentroidTracker:
    """Track vehicle centroids across frames using distance-based matching."""
    
    def __init__(self, max_disappeared=DISAPPEAR_LIMIT):
        self.next_id     = 0
        self.objects     = {}
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

        obj_ids       = list(self.objects.keys())
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


# ─────────────────────────── LICENSE PLATE OCR ──────────────────────────────

def extract_plate_text(roi: np.ndarray) -> str:
    """Extract license plate text from ROI using Tesseract OCR."""
    if roi is None or roi.size == 0:
        return ""

    roi_resized = imutils.resize(roi, width=400)
    gray = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

    plate_roi = gray
    for c in cnts:
        peri  = cv2.arcLength(c, True)
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


# ─────────────────────────── DRAWING UTILS ──────────────────────────────────

def draw_box(frame, x1, y1, x2, y2, color, label):
    """Draw bounding box with label."""
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    lbl_size, _ = cv2.getTextSize(label, FONT, 0.55, 2)
    cv2.rectangle(frame, (x1, y1 - lbl_size[1] - 6), (x1 + lbl_size[0] + 4, y1), color, -1)
    cv2.putText(frame, label, (x1 + 2, y1 - 4), FONT, 0.55, (255, 255, 255), 2)


def draw_speed_alert(frame, obj_id, speed_kmh, plate_text, x1, y1, has_history: bool):
    """Draw speed info and plate text above bounding box."""
    color = get_speed_color(speed_kmh, has_history)

    if not has_history:
        status = "Computing..."
        speed_str = "-- km/h"
    else:
        over_limit = speed_kmh > SPEED_LIMIT_KMH
        status    = "!! SPEEDING !!" if over_limit else "OK"
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
    cv2.putText(frame, f"Speed limit        : {SPEED_LIMIT_KMH} km/h",
                (10, 66), FONT, 0.55, (180, 180, 180), 1)
    cv2.putText(frame, f"Computing speed for: {total - len(computed_ids)} vehicle(s)",
                (10, 88), FONT, 0.45, COLOR_ZERO, 1)

    cv2.putText(frame, f"FPS: {fps_val:.1f}",
                (frame.shape[1] - 100, 22), FONT, 0.55, (100, 255, 100), 1)


# ── CALIBRATION TOOL ──

def calibrate_on_first_frame(video_path):
    """Interactive calibration tool: Click two points to measure pixel-to-meter ratio."""
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return

    points = []

    def click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            if len(points) == 2:
                dist = euclidean(points[0], points[1])
                real_meters = 3.7  # one lane width in meters
                mpp = real_meters / dist
                cv2.line(frame, points[0], points[1], (0, 255, 0), 2)
                cv2.putText(frame, f"{dist:.0f}px → MPP={mpp:.4f}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                print(f"\n[CALIBRATION] {dist:.0f} pixels = {real_meters}m")
                print(f"[CALIBRATION] Set METERS_PER_PIXEL = {mpp:.5f}\n")
            cv2.imshow("Calibrate - Click lane edges", frame)

    cv2.imshow("Calibrate - Click lane edges", frame)
    cv2.setMouseCallback("Calibrate - Click lane edges", click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ─────────────────────────── MAIN ───────────────────────────────────────────

def main():
    """Main processing loop."""
    class_list  = load_classes(COCO_TXT)
    det_colors  = random_colors(len(class_list))

    model = YOLO(WEIGHTS_PATH, "v8")

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("[ERROR] Cannot open video:", VIDEO_PATH)
        return

    fps = FPS_OVERRIDE or cap.get(cv2.CAP_PROP_FPS) or 30.0
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = None
    if OUTPUT_PATH:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (w, h))

    tracker       = CentroidTracker()
    centroid_hist = defaultdict(lambda: deque(maxlen=MAX_TRACK_HISTORY))
    speed_store   = defaultdict(float)
    computed_ids  = set()          # IDs that have a valid speed reading
    plate_store   = defaultdict(str)
    plate_timer   = defaultdict(int)
    OCR_INTERVAL  = 20

    frame_count = 0
    t_prev      = time.time()
    display_fps = 0.0

    print(f"[INFO] Processing video at {fps:.1f} FPS | Speed limit: {SPEED_LIMIT_KMH} km/h")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of video.")
            break
        frame_count += 1

        t_now = time.time()
        if t_now - t_prev >= 0.5:
            display_fps = frame_count / max(t_now - t_prev, 1e-6)
            t_prev      = t_now
            frame_count = 0

        # ── YOLOv8 detection ──
        results    = model.predict(source=[frame], conf=CONF_THRESHOLD, verbose=False)
        detections = results[0].boxes

        vehicle_detections = []
        if detections is not None:
            for box in detections:
                cls_id = int(box.cls.numpy()[0])
                if cls_id not in VEHICLE_CLASSES:
                    continue
                conf = float(box.conf.numpy()[0])
                x1, y1, x2, y2 = map(int, box.xyxy.numpy()[0])
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                vehicle_detections.append((cx, cy, x1, y1, x2, y2, cls_id, conf))

        centroids_only = [(d[0], d[1]) for d in vehicle_detections]
        tracked        = tracker.update(centroids_only)

        det_map = {}
        for d in vehicle_detections:
            cx, cy = d[0], d[1]
            for obj_id, tc in tracked.items():
                if tc == (cx, cy):
                    det_map[obj_id] = d
                    break

        speeding_count = 0

        for obj_id, centroid in tracked.items():
            centroid_hist[obj_id].append((centroid, time.time()))
            hist = centroid_hist[obj_id]

            has_history = obj_id in computed_ids

            # ── Speed computation ──
            if len(hist) >= MIN_SPEED_FRAMES:
                (prev_cx, prev_cy), t0 = hist[0]
                (curr_cx, curr_cy), t1 = hist[-1]
                dt = t1 - t0
                if dt > 0:
                    pixel_dist = euclidean((prev_cx, prev_cy), (curr_cx, curr_cy))
                    meters     = pixel_dist * METERS_PER_PIXEL
                    speed_ms   = meters / dt
                    speed_kmh  = speed_ms * 3.6
                    speed_store[obj_id] = speed_kmh
                    computed_ids.add(obj_id)
                    has_history = True

            speed_kmh = speed_store.get(obj_id, 0.0)

            # ── Count speeding (only for vehicles with valid speed) ──
            if has_history and speed_kmh > SPEED_LIMIT_KMH:
                speeding_count += 1

            # ── Get color ──
            box_color = get_speed_color(speed_kmh, has_history)

            # ── Draw bounding box ──
            if obj_id in det_map:
                cx, cy, x1, y1, x2, y2, cls_id, conf = det_map[obj_id]
                label = f"{VEHICLE_CLASSES[cls_id]} {conf:.2f}"

                draw_box(frame, x1, y1, x2, y2, box_color, label)

                # ── OCR ──
                plate_timer[obj_id] += 1
                if plate_timer[obj_id] % OCR_INTERVAL == 1:
                    roi  = frame[max(0, y1):y2, max(0, x1):x2]
                    text = extract_plate_text(roi)
                    if text:
                        plate_store[obj_id] = text

                plate_text = plate_store.get(obj_id, "")
                draw_speed_alert(frame, obj_id, speed_kmh, plate_text, x1, y1, has_history)

            # ── Trail ──
            pts = [h[0] for h in hist]
            for i in range(1, len(pts)):
                cv2.line(frame, pts[i - 1], pts[i], (255, 180, 0), 1)

        draw_hud(frame, list(tracked.keys()), speed_store, computed_ids, speeding_count, display_fps)

        if writer:
            writer.write(frame)

        if DISPLAY_WINDOW:
            cv2.imshow("Speed + Plate Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("[INFO] Quit by user.")
                break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    print("[DONE] Output saved to:", OUTPUT_PATH or "(not saved)")


if __name__ == "__main__":
    main()
