# plugins/ytmp3.py

from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def download_youtube_audio(url, output_path='.'):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_path=output_path)
        
        mp4_file = AudioFileClip(audio_file)
        mp3_filename = os.path.join(output_path, f"{yt.title}.mp3")
        mp4_file.write_audiofile(mp3_filename)
        
        os.remove(audio_file)
        return mp3_filename
    except Exception as e:
        return str(e)
