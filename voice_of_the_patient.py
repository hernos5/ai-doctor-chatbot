from dotenv import load_dotenv
load_dotenv()

import os
import tempfile
from typing import Optional
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr

def record_audio(output_path: str = "recording.wav", duration: int = 5) -> Optional[str]:
    """Records audio using the default microphone with fallback methods"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"Recording for {duration} seconds...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=duration, phrase_time_limit=duration)
            
            # Save as WAV file
            with open(output_path, "wb") as f:
                f.write(audio.get_wav_data())
            
            return output_path
    except Exception as e:
        print(f"Recording error: {str(e)}")
        return None

def transcribe_audio(audio_path: str) -> str:
    """Converts speech to text with multiple fallback options"""
    try:
        # Convert to WAV if needed
        if not audio_path.lower().endswith('.wav'):
            sound = AudioSegment.from_file(audio_path)
            wav_path = os.path.splitext(audio_path)[0] + ".wav"
            sound.export(wav_path, format="wav")
            audio_path = wav_path

        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            return r.recognize_google(audio)
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")
