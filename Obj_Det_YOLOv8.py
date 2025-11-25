from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

class RetailObjectDetector:
    def __init__(self):
        # Start with pre-trained COCO model
        self.model = YOLO('yolov8n.pt')  # Downloads automatically
        
        # Relevant COCO classes for retail
        self.retail_classes = {
            39: 'bottle', 40: 'wine_glass', 41: 'cup', 
            42: 'fork', 43: 'knife', 44: 'spoon', 
            45: 'bowl', 46: 'banana', 47: 'apple',
            # Add more as needed
        }
    
    def detect(self, image_path, conf_threshold=0.5):
        results = self.model(image_path, conf=conf_threshold)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                
                # Filter for retail items
                if cls in self.retail_classes:
                    detections.append({
                        'class': self.retail_classes.get(cls, 'unknown'),
                        'confidence': float(box.conf[0]),
                        'bbox': box.xyxy[0].cpu().numpy().astype(int),
                        'class_id': cls
                    })
        
        return detections
    
    def visualize(self, image_path):
        img = cv2.imread(image_path)
        detections = self.detect(image_path)
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            label = f"{det['class']}: {det['confidence']:.2f}"
            cv2.putText(img, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title(f'Detected {len(detections)} objects')
        plt.axis('off')
        plt.show()
        
        return detections

# Test it
detector = RetailObjectDetector()
results = detector.visualize('/Users/ishankharat/Downloads/Quantum_Retail_Robot/Quantum Dataset/spill5.jpg')