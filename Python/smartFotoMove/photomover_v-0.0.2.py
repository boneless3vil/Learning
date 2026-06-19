import os
import shutil
import cv2
import sys

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
        # Normalize the path (this also removes extraneous spaces)
        response = os.path.normpath(response)
    return response

# Placeholder: integrate your actual EfficientDet-D7 model inference here.
def run_efficientdet(image):
    """
    Run EfficientDet-D7 inference on the image.
    TODO: Replace with your actual model integration.
    Expected output: a list of detections with dictionaries of the form
    {'label': 'object_label', 'confidence': confidence_value}
    """
    # For demonstration, this dummy function returns an empty list.
    return []

# Placeholder: integrate your actual YOLOv7 model inference here.
def run_yolov7(image):
    """
    Run YOLOv7 inference on the image.
    TODO: Replace with your actual model integration.
    Expected output: a list of detections with dictionaries of the form
    {'label': 'object_label', 'confidence': confidence_value}
    """
    # For demonstration, this dummy function returns an empty list.
    return []

def merge_detections(detections1, detections2):
    """
    Merge detections from two models.
    In a full implementation, you might run non-maximum suppression (NMS) or
    combine confidences. Here we simply concatenate the lists.
    """
    return detections1 + detections2

def detect_subject_ensemble(image, subject, threshold=0.5):
    """
    Runs both EfficientDet-D7 and YOLOv7 on the image and checks if the specified
    subject is detected with a confidence above the threshold.
    """
    detections_eff = ru
