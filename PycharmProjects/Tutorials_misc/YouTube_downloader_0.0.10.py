# will ask for a download link from YouTube, then download link onto computer
# Tutorial:CODE WITH ME | Build in Python a YouTube Downloader | How To Build
#   YouTube Downloader Using Python
# Coder: Tiff In Tech (YouTube channel)
# https://www.youtube.com/watch?v=EMlM6QTzJo0

# ! Didn't work the first time. Had to update import file, pytube and follow
#   original site git project!
# original site: https://towardsdatascience.com/build-a-youtube-downloader-with-python-8ef2e6915d97

import sys
import tkinter as tk
from tkinter import messagebox, Listbox, StringVar
import pyperclip
import os
import time
import re
import pytube
from pytube import YouTube

def download_video():
    link = link_textbox.get()
    try:
        yt = YouTube(link)
        selected_streams = [stream_listbox.get(i) for i in stream_listbox.curselection()]
        if not selected_streams:
            messagebox.showerror("Error", "Please select at least one stream to download")
            return
        for stream in selected_streams:
            ys = yt.streams.filter(resolution=stream).first()
            filesize = ys.filesize
            start_time = time.time()
            print("Title: ",yt.title)
            print("Downloading...")
            ys.download(directory)
            end_time = time.time()
            download_time = end_time - start_time
            speed = filesize / (download_time * 1_000_000)
            estimated_time = filesize / (speed * 1_000_000)
            minutes, seconds = divmod(estimated_time, 60)
            print("Internet speed: {speed:.2f} Mbps")
            print(f"Estimated time: {int(minutes)} minutes {int(seconds)} seconds")
            sys.stdout.flush()
            print("Download completed!!")
    except Exception as e:
        messagebox.showerror("Error", e)


def paste_link():
    link = pyperclip.paste()
    match = re.search(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$', link)
    if match:
        try:
            yt = pytube.YouTube(link)
            link_textbox.delete(0, tk.END)
            link_textbox.insert(tk.END, link)
            on_select()
        except pytube.exceptions.RegexMatchError:
            messagebox.showerror("Error", "Not a valid YouTube link, please...couch potato!")
    else:
        messagebox.showerror("Error", "Not a valid YouTube link, please...couch potato!")



def on_select(event):
    link = link_textbox.get()
    try:
        yt = YouTube(link)
        stream_list = []
        for stream in yt.streams:
            if stream.resolution:
                stream_list.append(stream.resolution)
        stream_listbox.delete(0, tk.END)
        for stream in stream_list:
            stream_listbox.insert(tk.END, stream)
    except Exception as e:
        messagebox.showerror("Error", e)


root = tk.Tk()
root.title("YouTube Downloader")

link_label = tk.Label(root, text="Enter YouTube video link:")
link_label.pack()

link_textbox = tk.Entry(root)
link_textbox.pack()

paste_button = tk.Button(root, text="Paste", command=paste_link)
paste_button.pack(side=tk.RIGHT)

stream_listbox = Listbox(root, selectmode='multiple')
stream_listbox.pack()

directory = "Downloads"

download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

link_textbox.bind("<FocusOut>", on_select)

root.mainloop()


