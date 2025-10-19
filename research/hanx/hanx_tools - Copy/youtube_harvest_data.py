#<=====>#
# Description
#<=====>#
"""
YouTube video downloader using pytubefix
Downloads videos in highest quality available
"""

#<=====>#
# Known To Do List
#<=====>#
# TODO: Add error handling
# TODO: Add progress bar
# TODO: Add support for playlists

#<=====>#
# Imports
#<=====>#
# from pytube import YouTube
from pytubefix import YouTube

#<=====>#
# Variables
#<=====>#
yt_url = 'https://www.youtube.com/watch?v=eur8dUO9mvE'
dl_dir = './dl'
# Default download directory (change this to your preferred location)

#<=====>#
# Functions
#<=====>#
def download_video(url, output_path=dl_dir):
    """
    Downloads a YouTube video in highest quality
    Args:
        url (str): YouTube video URL
        output_path (str): Directory where the video will be downloaded. Defaults to './dl'
    """
    try:
        # Create output directory if it doesn't exist
        import os
        os.makedirs(output_path, exist_ok=True)
        
        yt = YouTube(url)
        print(f"Downloading: {yt.title}")
        print(f"Download directory: {os.path.abspath(output_path)}")
        
        # Get highest quality progressive stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(output_path=output_path)
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#<=====>#
# Default Run
#<=====>#
if __name__ == "__main__":
    download_video(yt_url)  # Uses default download directory
    # To specify a different directory, uncomment and modify the line below:
    # download_video(yt_url, output_path='C:/Users/YourUsername/Videos')


