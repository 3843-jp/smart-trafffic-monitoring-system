# Examples

This directory contains example scripts demonstrating different aspects of the Smart Traffic Monitoring System.

## Available Examples

### 1. Basic Speed Detection (`example_basic.py`)

Run the main speed detection system with default configuration.

```bash
python examples/example_basic.py
```

**What it does:**
- Loads a video file
- Detects vehicles using YOLOv8
- Tracks vehicles across frames
- Calculates speed based on centroid movement
- Recognizes license plates using OCR
- Displays real-time visualization with speed alerts

**Requirements:**
- Video file path configured in `config.py`
- Tesseract OCR installed
- YOLOv8 weights downloaded

---

### 2. Calibration Tool (`example_calibrate.py`)

Interactive tool to calibrate pixel-to-meter ratio for accurate speed estimation.

```bash
python examples/example_calibrate.py
```

**How to use:**
1. A video frame will open
2. Click two points on a known distance (e.g., lane width = 3.7m)
3. A measurement dialog will show the pixel-to-meter ratio
4. Copy the recommended `METERS_PER_PIXEL` value
5. Update `config.py` with the new value

**Example:**
```
[CALIBRATION] 74 pixels = 3.7m
[CALIBRATION] Set METERS_PER_PIXEL = 0.05
```

---

## Configuration for Examples

All examples use settings from `config.py`. Modify these values before running:

```python
# config.py
VIDEO_PATH = "path/to/your/video.mp4"
SPEED_LIMIT_KMH = 60
METERS_PER_PIXEL = 0.05  # Set after calibration
CONF_THRESHOLD = 0.45
```

---

## Quick Start

1. **Calibrate your video:**
   ```bash
   python examples/example_calibrate.py
   ```

2. **Update `config.py`** with the recommended `METERS_PER_PIXEL` value

3. **Run the main system:**
   ```bash
   python examples/example_basic.py
   ```

---

## Tips

- **Accuracy:** The calibration step is crucial for accurate speed measurements
- **Performance:** Use lower resolution videos (720p) for faster processing
- **OCR Quality:** Ensure vehicle ROI is at least 100px tall for better OCR results
- **GPU:** Enable CUDA in the config for faster processing on large videos

---

## Advanced Usage

You can customize behavior by modifying `config.py`:

```python
# Increase tracking history for slower scenes
MAX_TRACK_HISTORY = 50

# Adjust detection confidence
CONF_THRESHOLD = 0.5

# Change speed limit alert threshold
SPEED_LIMIT_KMH = 80

# Override video FPS (useful for slow-motion videos)
FPS_OVERRIDE = 60
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Video not found | Check `VIDEO_PATH` in `config.py` |
| No vehicles detected | Lower `CONF_THRESHOLD` or ensure vehicle is in COCO classes |
| Tesseract error | Install tesseract-ocr and set path in `config.py` |
| Poor speed accuracy | Run calibration tool again |

For more information, see [README.md](../README.md)
