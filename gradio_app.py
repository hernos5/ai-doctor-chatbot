import gradio as gr
from brain_of_the_doctor import analyze_skin_condition
from voice_of_the_patient import record_audio, transcribe_audio
from voice_of_the_doctor import speak_response
import tempfile
import os

def process_consultation(audio_input, image_input, text_input):
    try:
        # 1. Process Input
        if audio_input:
            user_query = transcribe_audio(audio_input)
        else:
            user_query = text_input

        # 2. Get Diagnosis
        diagnosis = analyze_skin_condition(
            query=user_query,
            image_path=image_input if image_input else None
        )

        # 3. Voice Response
        speak_response(diagnosis)
        
        return diagnosis

    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("## 🩺 AI Dermatologist Consultation")
    
    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Symptoms")
        image_input = gr.Image(type="filepath", label="Upload Skin Photo")
    
    text_input = gr.Textbox(label="Or Type Symptoms Here")
    submit_btn = gr.Button("Get Diagnosis")
    output = gr.Textbox(label="Diagnosis", interactive=False)
    
    submit_btn.click(
        fn=process_consultation,
        inputs=[audio_input, image_input, text_input],
        outputs=output
    )

if __name__ == "__main__":
    app.launch(server_port=7860)