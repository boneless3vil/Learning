# Created by ChatGPT, moves image and video files from downloads folder to
# folders of the user's choice.

import os
import shutil

# list of extensions of image files
img_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

# list of extensions of video files
vid_exts = [".mp4", ".mkv", ".flv", ".avi", ".wmv"]

# directory to move files from
src_dir = os.path.join(os.path.expanduser('~'), "Downloads")

# ask for the destination directory for image files
img_dst_dir = input("Enter the full path for the image destination folder: ")

# ask for the destination directory for video files
vid_dst_dir = input("Enter the full path for the video destination folder: ")

if not os.path.exists(img_dst_dir):
    os.mkdir(img_dst_dir)
if not os.path.exists(vid_dst_dir):
    os.mkdir(vid_dst_dir)

# iterate through all files in src_dir
for file in os.listdir(src_dir):
    # check if file is an image file
    if any(file.endswith(ext) for ext in img_exts):
        # move the file to img_dst_dir
        shutil.move(os.path.join(src_dir, file), img_dst_dir)
    elif any(file.endswith(ext) for ext in vid_exts):
        # move the file to vid_dst_dir
        shutil.move(os.path.join(src_dir, file), vid_dst_dir)
