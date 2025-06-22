##Ishan Kharat
## Robot Decision and Live Detection Using YOLO V8 models for 8 camera detection.


import cv2
from ultralytics import YOLO

# Load a compact object detector
vision_system = YOLO("yolov8n.pt")

# Initialize webcam feed (0 = default laptop camera)
camera_feed = cv2.VideoCapture(0)

if not camera_feed.isOpened():
    print("🔌 Unable to access webcam")
    exit()

while True:
    success, current_frame = camera_feed.read()
    if not success:
        print("⚠️ Frame capture failed")
        break

    # Analyze the frame for known objects
    detection_result = vision_system(current_frame)
    visual_output = detection_result[0].plot()

    # Overlay source label (optional)
    label = "Warehouse Bot Vision"
    cv2.putText(visual_output, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 200), 2)

    # Display the processed view
    cv2.imshow("Live Feed", visual_output)

    # Simulate robot's behavior logic
    task_flag = False

    for object_box in detection_result[0].boxes:
        object_id = int(object_box.cls[0])
        object_name = vision_system.names[object_id]
        confidence = float(object_box.conf[0])
        print(f"🔎 Seen: {object_name} ({confidence:.2f})")

        # Trigger task if bottle is visible
        if object_name == "bottle" and confidence > 0.5:
            print("📦 Task: Bottle spotted — prepare for shelf inspection.")
            task_flag = True

        # Greet if human is seen
        if object_name == "person" and confidence > 0.5:
            print("👋 Task: Person found — greet or alert.")

    if not task_flag:
        print("🟢 Status: No action needed, environment stable.")

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Shutting down vision system.")
        break

# Cleanup
camera_feed.release()
cv2.destroyAllWindows()
