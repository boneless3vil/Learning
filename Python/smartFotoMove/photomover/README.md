# PhotoMover

PhotoMover is a Python tool that uses YOLOv8 to automatically organize your photos based on their content (people, cars, dogs, etc.).

## System Requirements

- Python 3.12
  - Download from [python.org](https://www.python.org/downloads/) (Do not use Windows Store version)
  - During installation, check "Add Python 3.12 to PATH"
  - The application is tested and works with Python 3.12
- 4GB RAM minimum (8GB recommended for large collections)
- At least 2GB free disk space

## Windows Installation Guide

1. **Remove Windows Store Python (if installed)**
   - Open Windows Settings
   - Go to Apps & Features
   - Search for "Python"
   - Uninstall any Python versions from Microsoft Store

2. **Install Python Correctly**
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.12.x (latest stable version)
   - Run the installer
   - Important: Check "Add Python 3.12 to PATH" ✓
   - Choose "Customize installation"
   - Ensure "pip" is selected
   - Click Install

3. **Verify Installation**
   - Open Command Prompt (cmd.exe)
   - Type: `python --version`
   - Should show: Python 3.12.x
   - Type: `pip --version`
   - Should show pip version

4. **Update pip and Configure PATH**
   - Open Command Prompt as Administrator
   - Run: `python -m pip install --upgrade pip`
   - If you see a warning about Scripts not being in PATH:
       1. Copy the Scripts path from the warning message
       2. Open Windows Settings
       3. Search for "Environment Variables"
       4. Click "Edit the system environment variables"
       5. Click "Environment Variables"
       6. Under "User variables", select "Path"
       7. Click "New" and add BOTH:
          - `C:\Program Files\Python312`
          - `C:\Users\YourUsername\AppData\Roaming\Python\Python312\Scripts`
       8. Click "OK" on all windows
       9. Close and reopen Command Prompt to apply changes
       10. Verify by running: `pip --version` (should work without python -m)

5. **Download PhotoMover**
   - Download `photomover_standalone.py` and `requirements-visual.txt`
   - Create a new folder for your project
   - Place both files in that folder

6. **Install Required Packages**
   - Open Command Prompt in your project folder
   - Run: `pip install -r requirements-visual.txt`

7. **Run the Program**
   - In the same Command Prompt window
   - Run: `python photomover_standalone.py`

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

## Performance Tips for Large Collections

If you're processing a large number of images (1000+):

1. **Memory Management**
   - Close other applications while processing
   - Process one category at a time (e.g., first "people", then "cars")
   - The program creates a progress file (.progress) to track completed images
   - You can safely interrupt and resume processing

2. **Processing Strategy**
   - Start with a small test folder (50-100 images) to verify setup
   - For very large collections (5000+ images), consider splitting into subfolders
   - Process during off-hours when your computer has more free resources

3. **Resuming Interrupted Processing**
   - If processing stops, just run the script again with the same parameters
   - The progress tracking system will skip already processed images
   - Check photomover.log for any warnings or errors

## Troubleshooting

1. **Installation Issues**
   - Make sure you downloaded Python from python.org (not Windows Store)
   - Confirm Python is in PATH: type `python` in Command Prompt
   - If "python not found", uninstall and reinstall with "Add to PATH" checked

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
3. Make sure your Python version is 3.12 or newer
4. Try processing a smaller batch of images first

## Notes

- First run will download the YOLOv8 model (automatic)
- Processing time depends on your CPU speed
- Images are copied (not moved) to preserve originals
- A log file (photomover.log) is created with detailed information