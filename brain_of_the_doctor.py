from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def analyze_skin_condition(query, image_path=None):
    """Analyze skin condition with optional image reference"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = f"""As a dermatologist, analyze this skin concern:
        Patient Query: {query}
        {"Note: An image was provided but cannot be directly analyzed" if image_path else ""}
        Provide detailed analysis and recommendations:"""
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Analysis failed: {str(e)}"