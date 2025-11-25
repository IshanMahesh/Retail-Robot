import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class SpillDetector:
    def __init__(self):
        # Adjust these HSV ranges based on your spill colors
        self.spill_ranges = {
            'yellow_liquid': ([20, 100, 100], [30, 255, 255]),
            'brown_liquid': ([10, 50, 50], [20, 255, 200]),
            'water': ([0, 0, 200], [180, 30, 255])  # bright/reflective
        }
    
    def detect(self, image_path):
        # Read image
        img = cv2.imread(str(image_path))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        combined_mask = np.zeros(img.shape[:2], dtype=np.uint8)
        
        # Check each spill type
        for spill_type, (lower, upper) in self.spill_ranges.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # Clean up noise
        kernel = np.ones((5,5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum spill size
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w//2, y + h//2)
                detections.append({
                    'bbox': (x, y, w, h),
                    'center': center,
                    'area': area,
                    'confidence': min(area / 10000, 1.0)  # Simple confidence
                })
        
        return detections, combined_mask, img
    
    def visualize(self, image_path, save_path=None):
        detections, mask, img = self.detect(image_path)
        
        # Draw detections
        result = img.copy()
        for det in detections:
            x, y, w, h = det['bbox']
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(result, f"Spill: {det['confidence']:.2f}", 
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 255, 0), 2)
        
        # Show results
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Original')
        axes[1].imshow(mask, cmap='gray')
        axes[1].set_title('Detection Mask')
        axes[2].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        axes[2].set_title(f'Detections: {len(detections)}')
        
        for ax in axes:
            ax.axis('off')
        
        if save_path:
            plt.savefig(save_path)
        plt.show()

# Test it
detector = SpillDetector()
detector.visualize('/Users/ishankharat/Downloads/Quantum_Retail_Robot/Quantum Dataset/spill5.jpg')