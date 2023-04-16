# Requires administrator mode
# will ask for a download link from YouTube, then download link onto computer
# Tutorial:CODE WITH ME | Build in Python a YouTube Downloader | How To Build
#   YouTube Downloader Using Python
# Coder: Tiff In Tech (YouTube channel)
# https://www.youtube.com/watch?v=EMlM6QTzJo0

import re
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox
import pyperclip
# import pytube
from pytube import YouTube
import os

stream_list = []


def paste_link():
    link = pyperclip.paste()
    match = re.search(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$', link)
    if match:
        link_textbox.delete(0, tk.END)
        link_textbox.insert(0, link)
        on_select()  # Automatically populate the resolution field
    else:
        messagebox.showerror("Error", "Invalid YouTube link")


def on_select():
    global stream_list

    # Get the YouTube/clipboard link from the text field
    link = link_textbox.get()

    try:
        # Create a YouTube object using the link
        yt = YouTube(link)

        # Iterate through the streams and add them to the list if they have a resolution
        for stream in yt.streams:
            if stream.resolution:
                stream_list.append(stream)

        # Clear the listbox and populate it with the available stream resolutions
        stream_listbox.delete(0, tk.END)
        for stream in stream_list:
            display_text = stream.resolution
            if not stream.includes_audio_track:
                display_text += " (video only)"
            stream_listbox.insert(tk.END, display_text)

        # Bind a double-click event on the listbox to trigger the download_video function
        stream_listbox.bind("<Double-Button-1>", download_video)

    except Exception as e:
        messagebox.showerror("Error", e)


def download_video(event=None):
    global stream_list
    # Get the selected stream from the stream_list
    stream = stream_list[stream_listbox.curselection()[0]]

    # Ask for confirmation to download the selected stream
    result = messagebox.askquestion("Download Confirmation",
                                    "Do you want to download this stream?")

    if result == "yes":
        # Start downloading the selected stream
        try:
            # Get the user's home directory
            user_home = os.path.expanduser('~')

            # Set the default download directory
            download_directory = os.path.join(user_home,
                                              '../Tutorials_misc/Downloads')

            # Download the video to the specified directory
            stream.download(output_path=download_directory)

            # Show a success message when the download is completed
            messagebox.showinfo("Success", "Video downloaded successfully!")

        except Exception as e:
            # Show an error message if there's an exception during the download process
            messagebox.showerror("Error", e)


def save_as():
    global stream_list

    # Get the selected stream from the stream_list
    stream = stream_list[stream_listbox.curselection()[0]]

    # Open a save file dialog to choose the custom location and file name
    save_file_path = \
        filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=
        [("MP4 Files", "*.mp4"), ("All Files", "*.*")])

    # If a file path is provided, download the video to the specified path
    if save_file_path:
        try:
            stream.download(output_path=os.path.dirname(save_file_path),
                            filename=os.path.basename(save_file_path))
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", e)


# Create the main GUI window
root = tk.Tk()
root.title("YouTube Scraper")

# Create GUI components
link_label = tk.Label(root, text="Enter YouTube video link:")
link_label.grid(row=0, column=0, sticky=tk.W)  # Top left corner

link_textbox = tk.Entry(root, width=40)
link_textbox.grid(row=1, column=0, padx=(0, 5), sticky=tk.W)  # One row down from link_label

stream_listbox = Listbox(root, selectmode='SINGLE', width=40)
stream_listbox.grid(row=2, column=0, pady=(10, 10), sticky=tk.W)  # One row down from link_textbox

download_button = tk.Button(root, text="Download", command=download_video, width=10)  # Widen button
download_button.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)  # Bottom left

save_as_button = tk.Button(root, text="Save As...", command=save_as, width=10)  # Widen button
save_as_button.grid(row=3, column=0, pady=(0, 10))  # Bottom middle

paste_button = tk.Button(root, text="Paste", command=paste_link, width=10)  # Widen button
paste_button.grid(row=3, column=0, pady=(0, 10), sticky=tk.E)  # Bottom right

root.mainloop()



