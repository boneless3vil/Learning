#!/usr/bin/env python3
"""
PhotoMover - AI-powered photo organization tool
Standalone version for local execution
"""

import os
import logging
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import time

# Setup logging before imports to catch any import errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('photomover.log')
    ]
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import cv2
        from ultralytics import YOLO
        from rich.progress import Progress, SpinnerColumn
        from rich.console import Console
        from rich.panel import Panel
        from tqdm import tqdm
        from PIL import Image
        return True
    except ImportError as e:
        print("\nMissing required packages. Please run:")
        print("pip install -r requirements-visual.txt")
        print("\nOr install individual packages:")
        print("pip install ultralytics opencv-python-headless pillow rich tqdm")
        print(f"\nError details: {str(e)}")
        return False

if not check_dependencies():
    sys.exit(1)

# Now that we've checked dependencies, import them
import cv2
from ultralytics import YOLO
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.console import Console
from rich.panel import Panel

console = Console()

class PhotoMover:
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    BATCH_SIZE = 50

    def __init__(self):
        self.model = None
        self.processed = 0
        self.start_time = None
        self.copied_files = 0
        self.failed_files = 0

    def initialize(self) -> bool:
        """Initialize the YOLOv8 model"""
        try:
            with console.status("[bold green]Loading AI model...") as status:
                logger.info("Loading YOLOv8 model...")
                self.model = YOLO('yolov8n.pt')
                status.update("[bold green]Model loaded successfully!")
                return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            console.print("[bold red]Failed to load AI model!")
            return False

    def is_valid_image(self, filepath: str) -> bool:
        """Check if file is a valid image"""
        try:
            return (
                filepath.lower().endswith(self.SUPPORTED_FORMATS) and
                os.path.isfile(filepath) and
                os.path.getsize(filepath) > 0
            )
        except Exception:
            return False

    def get_input(self, prompt: str, is_path: bool = False) -> str:
        """Get and validate user input"""
        while True:
            response = input(prompt).strip()
            logger.debug(f"Raw input received: '{response}'")

            if response.lower() in {'exit', 'quit'}:
                sys.exit(0)

            if is_path:
                if (response.startswith('"') and response.endswith('"')) or \
                   (response.startswith("'") and response.endswith("'")):
                    response = response[1:-1].strip()
                    logger.debug(f"After quote removal: '{response}'")
                response = os.path.normpath(response)
                logger.debug(f"Normalized path: '{response}'")

            response = response.strip()
            logger.debug(f"Final trimmed response: '{response}'")
            return response

    def validate_path(self, path: str, should_exist: bool = True) -> bool:
        """Validate if path exists and is accessible"""
        try:
            if not path or not isinstance(path, str) or path.isspace():
                return False

            path = os.path.normpath(path)

            if should_exist:
                return os.path.exists(path) and os.access(path, os.R_OK)
            return os.access(os.path.dirname(path) or '.', os.W_OK)
        except Exception:
            return False

    def detect_subject(self, image, subject: str, threshold: float = 0.5) -> bool:
        """Detect if subject is present in image"""
        try:
            results = self.model(image)[0]
            for r in results.boxes.data:
                score = float(r[4])
                if score < threshold:
                    continue
                class_id = int(r[5])
                label = results.names[class_id]
                if label.lower() == subject.lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"Detection error: {str(e)}")
            return False

    def process_image(self, filepath: str, subject: str) -> Dict:
        """Process a single image"""
        result = {
            'filepath': filepath,
            'success': False,
            'matched': False,
            'error': None
        }

        try:
            if not self.is_valid_image(filepath):
                result['error'] = 'Invalid image file'
                return result

            image = cv2.imread(filepath)
            if image is None:
                result['error'] = 'Failed to load image'
                return result

            result['success'] = True
            result['matched'] = self.detect_subject(image, subject)
            return result
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error processing {filepath}: {str(e)}")
            return result

    def process_images(self, source_dir: str, dest_dir: str, subject: str) -> List[str]:
        """Process all images in a directory"""
        matching_images = []
        failed_images = []
        self.processed = 0
        self.start_time = time.time()

        # Get all image files
        image_files = [
            os.path.join(source_dir, f)
            for f in os.listdir(source_dir)
            if f.lower().endswith(self.SUPPORTED_FORMATS)
        ]

        total_images = len(image_files)
        if not total_images:
            console.print("[yellow]No image files found in source directory!")
            return []

        console.print(f"\nFound {total_images} images to process")

        # Process in batches
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task(
                f"Processing images for '{subject}'...",
                total=total_images
            )

            for i in range(0, total_images, self.BATCH_SIZE):
                batch = image_files[i:i + self.BATCH_SIZE]

                with ThreadPoolExecutor() as executor:
                    future_to_file = {
                        executor.submit(self.process_image, fp, subject): fp
                        for fp in batch
                    }

                    for future in as_completed(future_to_file):
                        try:
                            result = future.result()
                            if result['success']:
                                if result['matched']:
                                    matching_images.append(result['filepath'])
                            else:
                                failed_images.append(result['filepath'])

                            self.processed += 1
                            progress.update(task, completed=self.processed)

                        except Exception as e:
                            logger.error(f"Batch processing error: {str(e)}")
                            failed_images.append(future_to_file[future])

        if failed_images:
            logger.warning(f"Failed to process {len(failed_images)} images")

        return matching_images

    def copy_matching_images(self, matching_files: List[str], destination: str) -> None:
        """Copy matching images to destination folder"""
        try:
            os.makedirs(destination, exist_ok=True)

            for source_path in matching_files:
                try:
                    dest_path = os.path.join(destination, os.path.basename(source_path))
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    self.copied_files += 1
                except Exception as e:
                    logger.error(f"Error copying {source_path}: {str(e)}")
                    self.failed_files += 1

        except Exception as e:
            logger.error(f"Error creating directory {destination}: {str(e)}")

    def get_folders(self):
        """Get source and destination folders with confirmation"""
        while True:
            # Get source folder
            source = self.get_input("Enter source folder path (containing images): ", is_path=True)
            if not self.validate_path(source):
                console.print("[bold red]Invalid source folder path!")
                continue

            # Get destination folder
            dest = self.get_input("Enter destination folder path for organized images: ", is_path=True)
            if not self.validate_path(dest, should_exist=False):
                console.print("[bold red]Cannot write to destination folder!")
                continue

            # Show summary and get confirmation
            console.print("\nSelected paths:")
            console.print(f"Source: {source}")
            console.print(f"Destination: {dest}")

            confirm = self.get_input("\nProceed with these folders? (Y/n): ").lower()
            if confirm in ('', 'y', 'yes'):
                return source, dest
            elif confirm in ('n', 'no'):
                console.print("\nLet's try again...")
                continue
            else:
                console.print("[yellow]Invalid input. Please enter Y or n.")
                continue

    def run(self):
        """Main entry point"""
        console.print(Panel.fit(
            "[bold blue]PhotoMover[/bold blue] - AI-powered photo organization tool",
            subtitle="Type 'exit' or 'quit' at any prompt to end"
        ))

        if not self.initialize():
            return

        # Get and confirm folders
        source, dest = self.get_folders()
        if not source or not dest:
            return

        # Get subjects
        console.print("\nAvailable detection categories:", style="bold cyan")
        console.print("- person, car, dog, cat, bicycle, motorcycle")
        console.print("- airplane, bus, train, truck, boat")
        console.print("- and many more common objects\n")

        primary = self.get_input("Enter primary subject to detect (e.g., person): ")

        console.print("\nEnter additional details to further categorize (press Enter when done):")
        details = []
        while True:
            detail = self.get_input("> ")
            if not detail:
                break
            details.append(detail)

        # Process primary subject
        matching_files = self.process_images(source, dest, primary)
        primary_folder = os.path.join(dest, primary)
        self.copy_matching_images(matching_files, primary_folder)

        # Process additional details
        current_folder = primary_folder
        for detail in details:
            matching_files = self.process_images(current_folder, dest, detail)
            new_folder = os.path.join(current_folder, detail)
            self.copy_matching_images(matching_files, new_folder)
            current_folder = new_folder

        # Print summary
        console.print(f"\n[green]Successfully copied: {self.copied_files} files")
        if self.failed_files > 0:
            console.print(f"[red]Failed to copy: {self.failed_files} files")

if __name__ == "__main__":
    try:
        mover = PhotoMover()
        mover.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)