import gradio as gr
from brain_of_the_doctor import analyze_condition
from voice_of_the_patient import record_audio, transcribe_audio
from voice_of_the_doctor import speak_response
import tempfile
import os
from PIL import Image
import traceback

# Custom CSS for better UI
custom_css = """
.diagnosis-box {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    border-left: 4px solid #4e73df;
}
.record-btn {
    background-color: #4e73df !important;
    color: white !important;
}
"""

def handle_consultation(audio_input, image_input, text_input):
    """Complete consultation workflow with robust error handling"""
    temp_files = []
    try:
        # Initialize variables
        user_query = text_input.strip() if text_input else ""
        
        # Process audio if provided and no text input
        if audio_input and not user_query:
            try:
                # Create temporary WAV file (Gradio audio comes as temp file)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
                    audio_path = tmp_audio.name
                    temp_files.append(audio_path)
                
                # Convert Gradio audio to proper WAV format
                from pydub import AudioSegment
                audio = AudioSegment.from_file(audio_input)
                audio.export(audio_path, format="wav")
                
                # Transcribe audio
                user_query = transcribe_audio(audio_path)
                if not user_query:
                    return "🔇 Could not transcribe audio. Please try again or type your symptoms."
                    
            except Exception as e:
                print(f"Audio processing error: {traceback.format_exc()}")
                return f"🎤 Audio Error: {str(e)}"

        if not user_query:
            return "📝 Please describe your symptoms using voice or text"

        # Process image if provided
        image_path = None
        if image_input:
            try:
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_img:
                    image_path = tmp_img.name
                    temp_files.append(image_path)
                    
                    if isinstance(image_input, str):
                        # Handle file path
                        Image.open(image_input).save(image_path)
                    else:
                        # Handle numpy array or PIL Image
                        Image.fromarray(image_input).save(image_path)
            except Exception as e:
                print(f"Image processing error: {traceback.format_exc()}")
                return f"🖼️ Image Error: {str(e)}"

        # Get diagnosis from AI
        print("Analyzing condition...")
        diagnosis = analyze_condition(
            query=user_query,
            image_path=image_path
        )
        
        # Voice response
        speak_response(diagnosis)
        
        return diagnosis

    except Exception as e:
        print(f"System error: {traceback.format_exc()}")
        return f"⚠️ System Error: {str(e)}"
    finally:
        # Clean up temporary files
        for file_path in temp_files:
            try:
                if file_path and os.path.exists(file_path):
                    os.unlink(file_path)
            except:
                pass

# Create the Gradio interface
with gr.Blocks(title="AI Doctor", css=custom_css, theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🩺 AI Medical Consultant
    *Describe your symptoms verbally or upload medical images for analysis*
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="1. Record Symptoms",
                interactive=True,
                elem_classes=["record-btn"]
            )
            gr.Markdown("*Speak clearly for 5-7 seconds*")
            
            image_input = gr.Image(
                type="filepath",
                label="2. Upload Medical Image (Optional)",
                height=200
            )
            gr.Markdown("*Supports JPG, PNG formats*")
            
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="Or Type Your Symptoms Here",
                placeholder="Example: I've had a fever and cough for 3 days...",
                lines=5,
                max_lines=10
            )
            
            with gr.Row():
                submit_btn = gr.Button("Get Diagnosis", variant="primary")
                clear_btn = gr.Button("Clear All")
    
    # Diagnosis output
    diagnosis_output = gr.Textbox(
        label="Medical Analysis",
        interactive=False,
        lines=12,
        elem_classes=["diagnosis-box"]
    )
    
    # Examples for quick testing
    gr.Examples(
        examples=[
            [None, None, "Persistent headache with light sensitivity"],
            [None, None, "Red rash on my arms that itches"]
        ],
        inputs=[audio_input, image_input, text_input],
        label="Try these examples:"
    )
    
    # Button actions
    submit_btn.click(
        fn=handle_consultation,
        inputs=[audio_input, image_input, text_input],
        outputs=diagnosis_output
    )
    
    clear_btn.click(
        fn=lambda: [None, None, "", ""],
        inputs=[],
        outputs=[audio_input, image_input, text_input, diagnosis_output]
    )

if __name__ == "__main__":
    # Check for required packages
    try:
        import speech_recognition
        import pydub
    except ImportError:
        print("Missing required packages. Please run:")
        print("pip install SpeechRecognition pydub")
    
    # Launch the app
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
