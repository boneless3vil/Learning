import os
import shutil
import cv2
import sys

def get_input(prompt):
    """
    Gets input from the user and exits the program if the user types 'exit' or 'quit'.
    """
    response = input(prompt)
    if response.strip().lower() in {"exit", "quit"}:
        print("Exiting program.")
        sys.exit()
    return response.strip()

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
    detections_eff = run_efficientdet(image)
    detections_yolo = run_yolov7(image)
    detections = merge_detections(detections_eff, detections_yolo)

    for det in detections:
        # Compare subject names in a case-insensitive way.
        if det['label'].lower() == subject.lower() and det['confidence'] >= threshold:
            return True
    return False

def process_folder(source_folder, destination_folder, subject):
    """
    Processes images in source_folder using the ensemble detector.
    Copies images that match the subject into destination_folder.
    """
    os.makedirs(destination_folder, exist_ok=True)
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(source_folder, filename)
            image = cv2.imread(file_path)
            if image is None:
                print(f"Could not read {filename}; skipping.")
                continue  # Skip unreadable files.
            if detect_subject_ensemble(image, subject):
                shutil.copy(file_path, os.path.join(destination_folder, filename))
                print(f"Copied {filename} to {destination_folder}")

def main():
    print("=== Photo Reorganization Script ===")
    print("At any prompt, type 'exit' or 'quit' to end the program.\n")
    
    # Get source and destination folders from the user.
    source_folder = get_input("Enter the source folder: ")
    destination_root = get_input("Enter the destination folder: ")
    
    # Get primary subject.
    primary_subject = get_input("Enter the primary subject (e.g., people): ")
    
    # Get additional detail selections.
    detail_subjects = []
    while True:
        detail = get_input("Enter additional detail (or press Enter to finish adding selections): ")
        if detail == "":
            break
        detail_subjects.append(detail)
    
    # Step 1: Process the source folder for the primary subject.
    primary_folder = os.path.join(destination_root, primary_subject)
    print(f"\nProcessing primary subject '{primary_subject}' from the source folder...")
    process_folder(source_folder, primary_folder, primary_subject)
    
    # Step 2: Process each additional detail level iteratively.
    current_folder = primary_folder
    for detail in detail_subjects:
        new_folder = os.path.join(current_folder, detail)
        print(f"\nProcessing detail '{detail}' in folder '{current_folder}'...")
        process_folder(current_folder, new_folder, detail)
        # Update current_folder for the next level of detail.
        current_folder = new_folder
    
    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
