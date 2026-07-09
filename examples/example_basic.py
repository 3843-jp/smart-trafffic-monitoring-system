"""
Example 1: Basic Speed Detection
================================

This example shows how to run the basic speed detection system
with default configuration.

Usage:
    python examples/example_basic.py
"""

import sys
sys.path.insert(0, '..')

from speed_detection import main, SPEED_LIMIT_KMH

if __name__ == "__main__":
    print(f"Starting Speed Detection System")
    print(f"Speed Limit: {SPEED_LIMIT_KMH} km/h")
    print(f"Press 'Q' to quit")
    print("-" * 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
