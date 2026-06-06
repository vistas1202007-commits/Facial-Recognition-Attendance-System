# Facial-Recognition-Attendance-System
A Python attendance system that uses facial recognition to detect and mark attendance automatically via webcam. Saves records in CSV file
# 🎭 Facial Recognition Attendance System

A Python project that uses facial recognition to mark attendance automatically through webcam. No manual entry needed!

## Features
- Real-time face detection via webcam
- Automatically marks attendance when face is recognized
- One entry per person per day (no duplicates)
- Saves attendance in CSV file with name, date, time
- Shows green box for known faces, red for unknown

## Tech Used
- Python 3.x
- OpenCV
- face_recognition
- NumPy
- CSV module

## Installation
pip install opencv-python face_recognition numpy

## How to Run
python face_attendance.py

## How to Use
1. Create a folder named known_faces
2. Add photos of each person (name the file as person's name)
   Example: Shivani.jpg, Rahul.png
3. Run the script
4. Press Q to stop webcam

## Project Structure
face-attendance/
├── face_attendance.py
├── known_faces/
│   ├── Shivani.jpg
│   └── Rahul.png
├── attendance.csv
└── README.md

## Attendance CSV Format
Name     | Date       | Time
---------|------------|--------
Shivani  | 2025-01-15 | 09:32
