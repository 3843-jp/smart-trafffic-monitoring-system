"""
Example 2: Calibration Tool
============================

This example demonstrates how to calibrate the pixel-to-meter ratio
for accurate speed estimation.

Steps:
1. Click two points on the video that represent a known distance (e.g., lane width)
2. The tool calculates the meters-per-pixel ratio
3. Update METERS_PER_PIXEL in config.py with the calculated value

Usage:
    python examples/example_calibrate.py
"""

import sys
sys.path.insert(0, '..')

from speed_detection import calibrate_on_first_frame
from config import VIDEO_PATH

if __name__ == "__main__":
    print("=" * 60)
    print("CALIBRATION TOOL")
    print("=" * 60)
    print("\nInstructions:")
    print("1. A video frame will appear")
    print("2. Click two points representing a known distance")
    print("3. The recommended METERS_PER_PIXEL will be displayed")
    print("4. Update config.py with the calculated value")
    print("\nExample: Click lane edges (typically 3.7 meters apart)")
    print("-" * 60)
    
    try:
        calibrate_on_first_frame(VIDEO_PATH)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
