# PhotoMover - AI-powered Photo Organization Tool

PhotoMover is a Python tool that uses YOLOv8 to automatically organize your photos based on their content (people, cars, dogs, etc.).

## Virtual Environment Setup

1. Create and activate a virtual environment:
```bash
# On Windows:
python -m venv visual-env
visual-env\Scripts\activate

# On macOS/Linux:
python -m venv visual-env
source visual-env/bin/activate
```

2. Install required packages:
```bash
# Install base requirements for photo organization
pip install -r requirements-visual.txt

# For additional visual processing tasks, edit requirements-visual.txt
# and uncomment the packages you need
```

3. Verify installation:
```bash
python -c "import cv2; print('OpenCV installed successfully!')"
```

## Quick Start Guide

1. Download these files to your computer:
   - Save `photomover_standalone.py` to your project folder
   - Save `requirements-visual.txt` for dependency management
   - Save `README.md` for reference (optional)

2. Test with a small batch first:
```bash
# Create a test folder with a few images
mkdir test_photos
# Copy 5-10 photos to test_photos folder

# Run the script
python photomover_standalone.py
# Enter test_photos as source
# Enter organized_test as destination
```

3. For your full collection:
```bash
python photomover_standalone.py
# Enter your photos folder path
# Enter destination folder path
# Choose what to detect (e.g., people, cars, dogs)
```

## Features

- Fast batch processing (50 images at a time)
- Progress tracking with estimated time remaining
- Support for multiple image formats
- Hierarchical organization (primary subject + sub-categories)
- Error recovery and detailed logging

## Performance

- Processing speed: ~200ms per image
- Memory-efficient batch processing
- CPU-only operation (no GPU required)
- Example: 6000 images ≈ 20-30 minutes total processing time

## Troubleshooting Large Collections

1. Memory Usage:
   - The tool processes images in batches of 50 to manage memory
   - If you experience memory issues, close other applications
   - For very large images, the tool automatically resizes them for processing

2. Processing Time:
   - Expect about 20-30 minutes for 6000 images
   - Progress updates appear every 10 images
   - The tool shows estimated time remaining
   - It's safe to interrupt (Ctrl+C) and restart later

3. Image Format Issues:
   - If some images fail to process, check they are valid image files
   - The log file (photomover.log) lists any problematic files
   - Corrupted or zero-byte images are automatically skipped

4. Error Recovery:
   - The tool continues processing even if some images fail
   - Failed images are logged but don't stop the process
   - The final summary shows success/failure counts
   - You can safely rerun the tool - it won't duplicate copies

5. If Nothing is Detected:
   - Verify your images are not corrupted
   - Try with the example subjects shown in the prompt
   - Check the log file for detailed error messages

## Notes

- The first run will download the YOLOv8 model (this is automatic)
- Processing time depends on your CPU speed and number of images
- Images are copied (not moved) to preserve originals
- The tool creates a log file (photomover.log) with detailed information

## Support

If you encounter any issues:
1. Check the photomover.log file for error messages
2. Verify all required packages are installed
3. Make sure your Python version is 3.11 or newer
4. Try processing a smaller batch of images first