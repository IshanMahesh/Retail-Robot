# Script to help you label your own images
import cv2
from pathlib import Path

def create_test_dataset():
    """
    Instructions to note:
    1. Take photos with your phone if possible:
       - Spills (pour water/juice on floor)
       - Retail items (bottles, cans from your kitchen)
       - Empty spaces (for gap detection)
    2. Transfer to /Quantum_Dataset/
    3. Run this script to organize them
    """
    
    source_dir = Path('/Users/ishankharat/Downloads/Quantum_Retail_Robot/Quantum Dataset')
    
    # Create organized structure
    categories = ['spills', 'products', 'clean_floor', 'shelves']
    for cat in categories:
        Path(f'test_images/{cat}').mkdir(parents=True, exist_ok=True)
    
    print("Organize your images into:")
    for cat in categories:
        print(f"  - test_images/{cat}/")
    
    print("\nTip: Use your phone to take 20-30 images per category")
    print("Quality > Quantity for initial testing!")

create_test_dataset()