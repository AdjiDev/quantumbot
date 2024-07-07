# plugins/ytmp4.py

from pytube import YouTube
import os

def download_youtube_video(url, output_path='.'):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        print(f"Downloading video: {yt.title}")
        video_file = video_stream.download(output_path=output_path)
        return video_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)

if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'
    output_directory = './downloaded_videos'
    download_youtube_video(youtube_url, output_directory)
