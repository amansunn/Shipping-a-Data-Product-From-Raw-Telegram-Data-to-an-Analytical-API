import os
from pathlib import Path
import json
from ultralytics import YOLO

# Load YOLOv8 model (pre-trained)
model = YOLO('yolov8n.pt')  # You can use yolov8s.pt, yolov8m.pt, etc.

# Directory containing images (adjust path as needed)
images_dir = Path("data/raw/telegram_messages")
output = []

# Recursively find all images (jpg, png) in all subfolders
image_files = list(images_dir.rglob("*.jpg")) + list(images_dir.rglob("*.png"))
print(f"Found {len(image_files)} images.")

if not image_files:
    print("No images found. Please check your folder structure and file extensions.")
else:
    for img_path in image_files:
        print(f"Processing {img_path}")
        try:
            results = model(img_path)
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue
        for result in results:
            for box in result.boxes:
                detected = {
                    "image_path": str(img_path),
                    "message_id": img_path.stem,  # Adjust if you have a mapping from image to message_id
                    "detected_object_class": model.names[int(box.cls)],
                    "confidence_score": float(box.conf)
                }
                output.append(detected)
    print(f"Total detections: {len(output)}")

# Ensure output directory exists
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Save detections to a JSON file for later loading to PostgreSQL
with open("data/processed/image_detections.json", "w") as f:
    json.dump(output, f, indent=2)
if output:
    print(f"Detections saved to data/processed/image_detections.json")
else:
    print("No detections to save.")