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
    missing_packages = []
    try:
        import cv2
    except ImportError:
        missing_packages.append("opencv-python-headless")
    try:
        from ultralytics import YOLO
    except ImportError:
        missing_packages.append("ultralytics")
    try:
        from rich.progress import Progress, SpinnerColumn
        from rich.console import Console
        from rich.panel import Panel
    except ImportError:
        missing_packages.append("rich")
    try:
        from tqdm import tqdm
    except ImportError:
        missing_packages.append("tqdm")
    try:
        from PIL import Image
    except ImportError:
        missing_packages.append("pillow")

    if missing_packages:
        print("\nMissing required packages. Please run:")
        print("pip install -r requirements-visual.txt")
        print("\nOr install individual packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    return True

# Exit if dependencies are not met
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
    BATCH_SIZE = 20  # Reduced from 50 to 20 for better memory management

    def __init__(self):
        self.model = None
        self.processed = 0
        self.start_time = None
        self.copied_files = 0
        self.failed_files = 0

    def initialize(self) -> bool:
        """Initialize the YOLOv8 model with proper cleanup"""
        try:
            if self.model is not None:
                # Cleanup existing model if any
                del self.model
                import gc
                gc.collect()

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
        try:
            response = input(prompt).strip()
            logger.debug(f"Raw input received: '{response}'")

            if response.lower() in {'exit', 'quit'}:
                sys.exit(0)

            if is_path:
                # Remove quotes if present and trim spaces
                if (response.startswith('"') and response.endswith('"')) or \
                   (response.startswith("'") and response.endswith("'")):
                    response = response[1:-1].strip()
                    logger.debug(f"After quote removal: '{response}'")
                # Convert empty paths to empty string
                if not response or response.isspace():
                    return ""
                response = os.path.normpath(response)
                logger.debug(f"Normalized path: '{response}'")
                return response

            trimmed_response = response.strip()
            logger.debug(f"Final trimmed response: '{trimmed_response}'")
            return trimmed_response
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error getting input: {e}")
            return ""

    def validate_path(self, path: str, should_exist: bool = True) -> bool:
        """Validate if path exists and is accessible"""
        try:
            if not path or not isinstance(path, str) or path.isspace():
                return False

            # Convert path to system-appropriate format
            path = os.path.expanduser(os.path.normpath(path))

            if should_exist:
                return os.path.exists(path) and os.access(path, os.R_OK)

            # For destination paths, check if parent directory exists and is writable
            parent_dir = os.path.dirname(path) or '.'
            parent_dir = os.path.normpath(parent_dir)
            return os.path.exists(parent_dir) and os.access(parent_dir, os.W_OK)
        except Exception as e:
            logger.error(f"Error validating path: {e}")
            return False

    def detect_subject(self, image, subject: str, threshold: float = 0.5) -> bool:
        """Detect if subject is present in image with improved error handling"""
        try:
            if self.model is None:
                logger.error("Model not initialized")
                return False

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
        """Process images with improved memory management and progress tracking"""
        matching_images = []
        failed_images = []
        self.processed = 0
        self.start_time = time.time()

        # Setup progress tracking
        progress_file = os.path.join(dest_dir, '.progress')
        processed_files = set()

        # Resume from previous run if possible
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    processed_files = set(line.strip() for line in f)
                console.print(f"[yellow]Resuming from previous run ({len(processed_files)} images already processed)")
            except Exception as e:
                logger.error(f"Error reading progress file: {str(e)}")

        try:
            image_files = [
                os.path.join(source_dir, f)
                for f in os.listdir(source_dir)
                if f.lower().endswith(self.SUPPORTED_FORMATS)
            ]

            remaining_files = [f for f in image_files if f not in processed_files]
            total_remaining = len(remaining_files)

            if not total_remaining:
                console.print("[yellow]No new images to process!")
                return []

            console.print(f"\nProcessing {total_remaining} remaining images")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn()
            ) as progress:
                task = progress.add_task(
                    f"Processing images for '{subject}'...",
                    total=total_remaining
                )

                # Process in small batches
                for i in range(0, total_remaining, self.BATCH_SIZE):
                    batch = remaining_files[i:i + self.BATCH_SIZE]

                    with ThreadPoolExecutor(max_workers=4) as executor:
                        future_to_file = {
                            executor.submit(self.process_image, fp, subject): fp
                            for fp in batch
                        }

                        for future in as_completed(future_to_file):
                            filepath = future_to_file[future]
                            try:
                                result = future.result()

                                if result['success']:
                                    if result['matched']:
                                        matching_images.append(filepath)
                                else:
                                    failed_images.append(filepath)
                                    logger.warning(f"Failed to process {filepath}: {result.get('error', 'Unknown error')}")

                                # Update progress tracking
                                processed_files.add(filepath)
                                with open(progress_file, 'a') as f:
                                    f.write(f"{filepath}\n")

                                self.processed += 1
                                progress.update(task, completed=self.processed)

                            except Exception as e:
                                logger.error(f"Error processing {filepath}: {str(e)}")
                                failed_images.append(filepath)

                    # Memory management: force garbage collection between batches
                    import gc
                    gc.collect()
                    time.sleep(0.1)  # Small delay to prevent CPU overload

        except Exception as e:
            logger.error(f"Error during batch processing: {str(e)}")
            console.print("[bold red]Error during processing. Check the log file for details.")

        if failed_images:
            logger.warning(f"Failed to process {len(failed_images)} images")
            console.print(f"\n[yellow]Failed to process {len(failed_images)} images. Check photomover.log for details.")

        # Cleanup progress file only if all processing completed
        if len(processed_files) == len(image_files):
            try:
                os.remove(progress_file)
            except Exception as e:
                logger.error(f"Error removing progress file: {str(e)}")

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
            source = self.get_input("\nEnter source folder path (containing images)\nPath: ", is_path=True)
            if not self.validate_path(source):
                console.print("[bold red]Invalid source folder path!")
                continue

            # Get destination folder
            dest = self.get_input("\nEnter destination folder path for organized images\nPath: ", is_path=True)
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
            "[bold blue]PhotoMover[/bold blue] - AI-powered photo organization tool\n" +
            "[yellow]Follow these steps:[/yellow]\n" +
            "1. Enter source directory (e.g., 'test_images')\n" +
            "2. Enter destination directory (e.g., 'test_images/organized')\n" +
            "3. Choose what to detect (e.g., 'person', 'car', 'dog')\n" +
            "4. Add optional sub-categories",
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
        console.print("Common Objects:", style="bold")
        console.print("- person, car, dog, cat")
        console.print("- bicycle, motorcycle")
        console.print("\nVehicles:", style="bold")
        console.print("- airplane, bus, train")
        console.print("- truck, boat")
        console.print("========================")

        primary = self.get_input("\nEnter primary subject to detect (e.g., person): ")

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

# Add a test directory setup function to help users verify the installation
def setup_test_directory():
    """Create a test directory structure if it doesn't exist"""
    test_dir = "test_images"
    test_dest = os.path.join(test_dir, "organized")

    try:
        # Create test directory if it doesn't exist
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            console.print(f"\n[yellow]Created test directory: {test_dir}")
            console.print("[yellow]Please copy some test images into this folder before running the script.")
            return False
        elif not any(f.lower().endswith(PhotoMover.SUPPORTED_FORMATS) for f in os.listdir(test_dir)):
            console.print(f"\n[yellow]No images found in {test_dir}")
            console.print("[yellow]Please copy some test images into this folder before running the script.")
            return False
        return True
    except Exception as e:
        logger.error(f"Error setting up test directory: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        # Check if test directory is ready
        if not setup_test_directory():
            console.print("\n[bold cyan]Quick Start:[/bold cyan]")
            console.print("1. Copy some test images to the 'test_images' folder")
            console.print("2. Run this script again")
            console.print("3. Follow the on-screen prompts")
            sys.exit(0)

        mover = PhotoMover()
        mover.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)