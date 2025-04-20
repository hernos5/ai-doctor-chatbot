from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
from PIL import Image

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Medical specialization configuration
MEDICAL_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH", 
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=MEDICAL_CONFIG,
    safety_settings=safety_settings
)

def analyze_condition(query, image_path=None):
    """Analyze medical condition with optional image"""
    try:
        prompt = f"""As a senior doctor, analyze this case:
        
        Patient Description: {query}
        
        Provide:
        1. Differential diagnosis (most likely first)
        2. Recommended tests/actions
        3. Red flag symptoms
        4. When to seek urgent care
        
        Use layman's terms and be compassionate."""
        
        if image_path:
            img = Image.open(image_path)
            # Resize if too large
            if max(img.size) > 1024:
                img.thumbnail((1024, 1024))
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content(prompt)
            
        return response.text
    except Exception as e:
        return f"Medical analysis error: {str(e)}"
