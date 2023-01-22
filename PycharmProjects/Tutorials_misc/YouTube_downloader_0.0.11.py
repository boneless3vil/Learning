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
from datetime import timedelta
import time
import re
import pytube
from pytube import YouTube

root = tk.Tk()


def download_video(event, stream_list):
    stream = stream_list[stream_listbox.curselection()[0]]
    result = messagebox.askquestion("Download Confirmation", "Do you want to download this stream?")
    if result == "yes":
        # start download
        start_time = time.time()
        stream.download()
        # start progress bar
        progress = tk.Toplevel(root)
        progress.title("Download Progress")
        progress_bar = ttk.Progressbar(progress, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack()
        time_remaining_label = tk.Label(progress, text="Time Remaining: Calculating...")
        time_remaining_label.pack()
        progress_bar.start()
        while stream.downloading:
            time_remaining = (time.time() - start_time) * (1 - stream.progress()) / stream.progress()
            time_remaining = timedelta(seconds=int(time_remaining))
            progress_bar["value"] = stream.progress() * 100
            time_remaining_label.configure(text="Time Remaining: " + str(time_remaining))
            progress.update()
            time.sleep(1)
        progress_bar.stop()
        progress.destroy()


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
            messagebox.showerror("Error", "Not a valid YouTube link...couch potato!")
    else:
        messagebox.showerror("Error", "Not a valid YouTube link, bruh!")


def on_select():
    link = link_textbox.get()
    try:
        yt = YouTube(link)
        stream_list = []
        for stream in yt.streams:
            if stream.resolution:
                stream_list.append(stream)
        stream_listbox.delete(0, tk.END)
        for stream in stream_list:
            stream_listbox.insert(tk.END, stream.resolution)
        stream_listbox.bind("<Double-Button-1>", lambda event: download_video(event, stream_list))
        if len(stream_listbox.curselection()) > 0:
            stream = stream_list[stream_listbox.curselection()[0]]
            result = messagebox.askquestion("Download Confirmation", "Do you want to download this stream?")
            if result == "yes":
                start_download()
            else:
                messagebox.showerror("Error", "Please select a stream to download.")
    except Exception as e:
        messagebox.showerror("Error", e)



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

download_button = tk.Button(root, text="Download", command=lambda:
download_video(link_textbox.get()))


link_textbox.bind("<FocusOut>", on_select)

root.mainloop()


