from dotenv import load_dotenv
load_dotenv()

import os
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
import subprocess

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def speak_response(text):
    """Convert text to speech and play it"""
    try:
        # Use ElevenLabs if available
        if ELEVENLABS_API_KEY:
            client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
            audio = client.generate(
                text=text,
                voice="Rachel",
                model="eleven_turbo_v2"
            )
            elevenlabs.save(audio, "response.mp3")
        else:  # Fallback to gTTS
            tts = gTTS(text=text, lang='en')
            tts.save("response.mp3")
            
        # Play audio
        subprocess.run(["ffplay", "-nodisp", "-autoexit", "response.mp3"], 
                      stderr=subprocess.DEVNULL)
        
    except Exception as e:
        print(f"Voice synthesis error: {e}")