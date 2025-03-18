# Install required libraries
# !pip install pytube
# !pip install pydub
# !pip install speechrecognition

import os
from pytube import YouTube
from pydub import AudioSegment
import speech_recognition as sr


def download_audio_from_youtube(url, download_path="audio"):
    # Create download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Download video from YouTube
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    downloaded_file = video.download(output_path=download_path)

    # Convert to WAV format (SpeechRecognition library works best with WAV)
    audio = AudioSegment.from_file(downloaded_file)
    audio_file_path = os.path.join(download_path, yt.title + ".wav")
    audio.export(audio_file_path, format="wav")

    # Remove the original file (optional)
    os.remove(downloaded_file)

    return audio_file_path


def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    return text


def save_transcription_to_file(transcription, filename="transcription.txt"):
    with open(filename, "w") as file:
        file.write(transcription)


youtube_url = "https://youtu.be/_Gv4ex7bt9Q?si=9nyLe2dCP7PGYRut"
audio_file = download_audio_from_youtube(youtube_url)
transcription = convert_audio_to_text(audio_file)
# Save transcription to a .txt file
save_transcription_to_file(transcription, filename="transcription.txt")

print(f"Transcription saved to transcription.txt")
print(transcription)
