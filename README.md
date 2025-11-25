# Retail-Robot

This project simulates a perception/planning/ and task prioritizing system for a retail robot using YOLOv8 and a webcam feed, potentially be simulated in Isaac Sim.

### Authors: Quantum Robotics Lab
        Ishan Kharat: Driver
        Abdul Manan: Navigator

### Features
- Real-time object detection using YOLOv8n
- Task simulation, like detecting all objects and  spill detection
- Humanized behavior simulation messages [Assigned]

### 🛠️ Requirements
- Python 3.9+
- Install dependencies:

        conda create -n retailbot python=3.10 -y
        conda activate retailbot

        conda install pip -y
  
        pip install opencv-python numpy matplotlib
        pip install torch torchvision  # PyTorch
        pip install ultralytics  # YOLOv8
        pip install pillow

- Import YOLO

        python
        from ultralytics import YOLO
        results = model("https://ultralytics.com/images/bus.jpg")

- Run

        python multi_camera_detection.py

