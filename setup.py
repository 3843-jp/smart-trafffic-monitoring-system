#!/usr/bin/env python
"""
Setup script for Smart Traffic Monitoring System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smart-traffic-monitoring",
    version="1.0.0",
    author="Traffic Monitoring Team",
    description="Real-time vehicle speed detection and license plate recognition system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3843-jp/smart-trafffic-monitoring-system",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ultralytics>=8.0.0",
        "opencv-python-headless>=4.8.0",
        "pytesseract>=0.3.10",
        "imutils>=0.5.4",
        "numpy>=1.24.0",
    ],
)
