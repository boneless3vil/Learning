# will ask for a download link from YouTube, then download link onto computer
# Tutorial:CODE WITH ME | Build in Python a YouTube Downloader | How To Build
#   YouTube Downloader Using Python
# Coder: Tiff In Tech (YouTube channel)
# https://www.youtube.com/watch?v=EMlM6QTzJo0

# ! Didn't work the first time. Had to update import file, pytube and follow
#   original site git project!
# original site: https://towardsdatascience.com/build-a-youtube-downloader-with-python-8ef2e6915d97


# import pytube
from pytube import YouTube

#ask for the link from user
link = input("Enter the link of YouTube video you want to download:  ")
yt = YouTube(link)

#Showing details
print("Title: ",yt.title)
print("Number of views: ",yt.views)
print("Length of video: ",yt.length)
print("Rating of video: ",yt.rating)
#Getting the highest resolution possible
ys = yt.streams.get_highest_resolution()

#Starting download
print("Downloading...")
ys.download('G:\download\YouTube')
print("Download completed!!")