import os
import shutil
import cv2
import sys

# ---------------------------
# Import for EfficientDet-D7 (TensorFlow)
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

# ---------------------------
# Import for YOLOv7 (PyTorch)
import torch
from PIL import Image

# ---------------------------
# Global: Load EfficientDet-D7 model from TF Hub
print("Loading EfficientDet-D7 model from TensorFlow Hub (this may take a while)...")
effdet_model = hub.load("https://tfhub.dev/tensorflow/efficientdet/d7/1")
print("EfficientDet-D7 model loaded.")

# ---------------------------
# Global: Load YOLOv7 model from Torch Hub
print("Loading YOLOv7 model from Torch Hub (this may take a while)...")
yolov7_model = torch.hub.load('WongKinYiu/yolov7', 'yolov7', pretrained=True)
print("YOLOv7 model loaded.")

# ---------------------------
# COCO Labels mapping for EfficientDet-D7 (partial list; extend as needed)
COCO_LABELS = {
    1: "person",
    2: "bicycle",
    3: "car",
    4: "motorcycle",
    5: "airplane",
    6: "bus",
    7: "train",
    8: "truck",
    9: "boat",
    10: "traffic light",
    11: "fire hydrant",
    13: "stop sign",
    14: "parking meter",
    15: "bench",
    # Add more labels if needed
}

def get_input(prompt, is_path=False):
    """
    Gets input from the user, trims extra spaces, and if is_path is True,
    removes surrounding quotes and normalizes the path.
    Exits if the user types 'exit' or 'quit'.
    """
    response = input(prompt).strip()
    if response.lower() in {"exit", "quit"}:
        print("Exiting program.")
        sys.exit()
    if is_path:
        # Remove surrounding double or single quotes if present.
        if (response.startswith('"') and response.endswith('"')) or (response.startswith("'") and response.endswith("'")):
            response = response[1:-1]
        # Normalize the path
        response = os.path.normpath(response)
    return response

def run_efficientdet(image):
    """
    Runs EfficientDet-D7 inference on the given image.
    The image should be in BGR format (as read by OpenCV).
    Returns a list of detections:
      [{'label': 'object_label', 'confidence': confidence_value}, ...]
    """
    # Convert image from BGR to RGB and resize to model input size (1536x1536)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_size = 1536
    image_resized = cv2.resize(image_rgb, (input_size, input_size))
    
    # Convert image to tensor and add batch dimension
    input_tensor = tf.convert_to_tensor(image_resized, dtype=tf.float32)
    input_tensor = tf.expand_dims(input_tensor, axis=0)
    
    # Run inference
    outputs = effdet_model(input_tensor)
    
    # Process the outputs. The model returns:
    #   'detection_scores': [1, num_detections],
    #   'detection_classes': [1, num_detections], etc.
    detection_scores = outputs['detection_scores'].numpy()[0]
    detection_classes = outputs['detection_classes'].numpy()[0].astype(int)
    
    detections = []
    threshold = 0.5  # Confidence threshold
    for score, cls in zip(detection_scores, detection_classes):
        if score < threshold:
            continue
        label = COCO_LABELS.get(cls, "N/A")
        detections.append({'label': label, 'confidence': float(score)})
    return detections

def run_yolov7(image):
    """
    Runs YOLOv7 inference on the given image.
    The image should be in BGR format (as read by OpenCV).
    Returns a list of detections:
      [{'label': 'object_label', 'confidence': confidence_value}, ...]
    """
    # Convert image from BGR to RGB and then to a PIL image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(image_rgb)
    
    # Run inference with YOLOv7. The model returns a results object.
    results = yolov7_model(pil_img)
    
    detections = []
    threshold = 0.5  # Confidence threshold
    # The results are assumed to be in results.xyxy[0] with each detection as:
    #   [x1, y1, x2, y2, confidence, class]
    if hasattr(results, 'xyxy'):
        for *xyxy, conf, cls in results.xyxy[0].tolist():
            if conf < threshold:
                continue
            label = yolov7_model.names[int(cls)]
            detections.append({'label': label, 'confidence': conf})
    return detections

def merge_detections(detections1, detections2):
    """
    Merges detections from the two models.
    Here we simply concatenate the two lists.
    """
    return detections1 + detections2

def detect_subject_ensemble(image, subject, threshold=0.5):
    """
    Runs both EfficientDet-D7 and YOLOv7 on the image and checks if the specified
    subject (case-insensitive) is detected with a confidence above the threshold.
    """
    detections_eff = run_efficientdet(image)
    detections_yolo = run_yolov7(image)
    detections = merge_detections(detections_eff, detections_yolo)
    
    for det in detections:
        if det['label'].lower() == subject.lower() and det['confidence'] >= threshold:
            return True
    return False

def process_folder(source_folder, destination_folder, subject):
    """
    Processes all images in source_folder using the ensemble detector.
    Copies images that match the subject into destination_folder.
    """
    os.makedirs(destination_folder, exist_ok=True)
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(source_folder, filename)
            image = cv2.imread(file_path)
            if image is None:
                print(f"Could not read {filename}; skipping.")
                continue
            if detect_subject_ensemble(image, subject):
                shutil.copy(file_path, os.path.join(destination_folder, filename))
                print(f"Copied {filename} to {destination_folder}")

def main():
    print("=== Photo Reorganization Script ===")
    print("At any prompt, type 'exit' or 'quit' to end the program.\n")
    
    # Get source and destination folders from the user
    source_folder = get_input("Enter the source folder: ", is_path=True)
    destination_root = get_input("Enter the destination folder: ", is_path=True)
    
    # Get primary subject
    primary_subject = get_input("Enter the primary subject (e.g., people): ")
    
    # Get additional detail selections
    detail_subjects = []
    while True:
        detail = get_input("Enter additional detail (or press Enter to finish adding selections): ")
        if detail == "":
            break
        detail_subjects.append(detail)
    
    # Step 1: Process the source folder for the primary subject
    primary_folder = os.path.join(destination_root, primary_subject)
    print(f"\nProcessing primary subject '{primary_subject}' from the source folder...")
    process_folder(source_folder, primary_folder, primary_subject)
    
    # Step 2: Process each additional detail level iteratively
    current_folder = primary_folder
    for detail in detail_subjects:
        new_folder = os.path.join(current_folder, detail)
        print(f"\nProcessing detail '{detail}' in folder '{current_folder}'...")
        process_folder(current_folder, new_folder, detail)
        current_folder = new_folder
    
    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
