from dotenv import load_dotenv
load_dotenv()

import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

def record_audio(output_path="patient_recording.mp3", duration=5):
    """Record and save patient audio"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source, timeout=duration)
        
        # Convert to MP3
        audio_segment = AudioSegment.from_wav(BytesIO(audio.get_wav_data()))
        audio_segment.export(output_path, format="mp3")
        return output_path

def transcribe_audio(audio_path):
    """Convert speech to text using Whisper"""
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file
        )
        return transcription.text