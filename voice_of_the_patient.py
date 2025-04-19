from dotenv import load_dotenv
load_dotenv()

import os

# Try to import only if running locally
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    from io import BytesIO
    MICROPHONE_SUPPORTED = True
except ImportError:
    print("Speech recognition or audio modules not available.")
    sr = None
    MICROPHONE_SUPPORTED = False


def record_audio(output_path="patient_recording.mp3", duration=5):
    """Record and save patient audio — only works locally"""
    if not MICROPHONE_SUPPORTED:
        print("Microphone access not available on this platform.")
        return None

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source, timeout=duration)

        # Convert to MP3
        audio_segment = AudioSegment.from_wav(BytesIO(audio.get_wav_data()))
        audio_segment.export(output_path, format="mp3")
        return output_path


def transcribe_audio(audio_path):
    """Convert speech to text using Whisper API"""
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file
        )
        return transcription.text
