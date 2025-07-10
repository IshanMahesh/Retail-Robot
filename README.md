# Retail-Robot

This project simulates a perception system for a retail robot using YOLOv8 and a webcam feed.

### Features
- Real-time object detection using YOLOv8n
- Task simulation like detecting all objects and  greeting people
- Humanized behavior simulation messages [Assigned]

### 🛠️ Requirements
- Python 3.9+
- Install dependencies:

        conda create -n retailbot python=3.9 -y
        conda activate retailbot

        conda install pip -y
        pip install ultralytics opencv-python

        pip install -r requirements.txt

- Import YOLO

        python
        from ultralytics import YOLO
        results = model("https://ultralytics.com/images/bus.jpg")

- Run

        python multi_camera_detection.py

