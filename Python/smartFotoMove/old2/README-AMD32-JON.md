# PhotoMover - AI-powered Photo Organization Tool

PhotoMover is a Python tool that uses YOLOv8 to automatically organize your photos based on their content (people, cars, dogs, etc.).

## Quick Setup Guide

1. **Download Required Files**
   - Download `photomover_standalone.py` and `requirements-visual.txt` to your computer
   - Create a new folder for your project
   - Place both files in that folder

2. **Install Python**
   - Make sure you have Python 3.11 or newer installed
   - You can download it from [python.org](https://www.python.org/downloads/)

3. **Install Required Packages**
   ```bash
   # Open terminal/command prompt in your project folder
   pip install -r requirements-visual.txt
   ```

4. **Run the Program**
   ```bash
   python photomover_standalone.py
   ```

## Usage Guide

1. **Prepare Your Photos**
   - Create a folder with the photos you want to organize
   - Note down the folder path

2. **Start the Program**
   - Run the script using the command above
   - Follow the on-screen prompts:
     1. Enter source folder path (where your photos are)
     2. Enter destination folder path (where organized photos will go)
     3. Choose what to detect (e.g., person, car, dog)
     4. Add optional sub-categories

3. **Available Detection Categories**
   - Common Objects: person, car, dog, cat, bicycle, motorcycle
   - Vehicles: airplane, bus, train, truck, boat
   - And many more standard objects

## Features

- Fast batch processing (50 images at a time)
- Progress tracking with estimated time remaining
- Support for multiple image formats (.jpg, .jpeg, .png, .bmp, .webp)
- Hierarchical organization (primary subject + sub-categories)
- Error recovery and detailed logging

## Performance

- Processing speed: ~200ms per image
- Memory-efficient batch processing
- CPU-only operation (no GPU required)
- Example: 6000 images ≈ 20-30 minutes total processing time

## Troubleshooting

1. **Installation Issues**
   - Make sure you're using Python 3.11 or newer
   - Try running: `pip install --upgrade pip` before installing requirements
   - If you see GPU errors, don't worry - the tool works fine on CPU

2. **Running the Program**
   - Use forward slashes (/) or double backslashes (\\\\) in paths
   - Example path: `C:/Users/YourName/Pictures` or `C:\\Users\\YourName\\Pictures`
   - The program will create the destination folder if it doesn't exist

3. **Processing Issues**
   - The tool processes images in batches to manage memory
   - Progress updates appear every 10 images
   - It's safe to interrupt (Ctrl+C) and restart later
   - Check photomover.log for detailed error messages

## Support

If you encounter issues:
1. Check the photomover.log file for error messages
2. Verify all required packages are installed
3. Make sure your Python version is 3.11 or newer
4. Try processing a smaller batch of images first

## Notes

- First run will download the YOLOv8 model (automatic)
- Processing time depends on your CPU speed
- Images are copied (not moved) to preserve originals
- A log file (photomover.log) is created with detailed information