# ./src/interface.py

import gradio as gr
# from transcribetonic import TranscribeTonic
from src.pitch import PitchTonic

title = "Welcome to Pitch Tonic"
description = """This demo helps you practice your pitch in two way : 
1. with help and evaluation of your answers to tough questions.
2. with real time support brining you precise answers to tough investor questions.
upload your documents to get started
"""
pitch_trainer = gr.Interface(
    fn=PitchTonic.pitch_trainer_handler,
    inputs=[
        gr.Audio(source="microphone", type="filepath"),
        gr.MultimodalTextbox(file_types=["audio","text"]), #, value=['text': 'Ask your Question Here' , 'files': [{path: 'docs/audio.wav'}] ] ),
        gr.Radio(["evaluate", "test"], label="Task", value="evaluate"),
        gr.Checkbox(value=False, label="Return timestamps"),
    ],
    outputs=[
        gr.Textbox(label="Tonic Pitch Trainer", multimodal=True),
    ],
    allow_flagging="never",
    title=title,
    description=description,
#   article=article,
)

pitch_helper = gr.Interface(
    fn=PitchTonic.pitch_helper_handler,
    inputs=[
        gr.Audio(source="microphone", type="filepath"),
        gr.MultimodalTextbox(file_types=['audio','text']), #, value=['text': 'Ask your Question Here', 'files': [{path: 'docs/audio.wav'}]]) ,
        gr.Checkbox(value=False, label="Return timestamps")
        ],
    outputs=[
        gr.Textbox(label="Tonic Pitch Helper", multimodal=True),
    ],
    allow_flagging="never",
    title=title,
    description=description,
#   article=article,
)

microphone_chunked = gr.Interface(
    fn=transcribe_chunked_audio,
    inputs=[
        gr.Audio(source="microphone", type="filepath"),
        gr.Radio(["transcribe", "translate"], label="Task", value="transcribe"),
        gr.Checkbox(value=False, label="Return timestamps"),
    ],
    outputs=[
        gr.Textbox(label="Transcription", show_copy_button=True),
        gr.Textbox(label="Transcription Time (s)"),
    ],
    allow_flagging="never",
    title=title,
    description=description,
#   article=article,
)

audio_chunked = gr.Interface(
    fn=transcribe_chunked_audio,
    inputs=[
        gr.Audio(source="upload", label="Audio file", type="filepath"),
        gr.Radio(["transcribe", "translate"], label="Task", value="transcribe"),
        gr.Checkbox(value=False, label="Return timestamps"),
    ],
    outputs=[
        gr.Textbox(label="Transcription", show_copy_button=True),
        gr.Textbox(label="Transcription Time (s)"),
    ],
    allow_flagging="never",
    title=title,
    description=description,
#   article=article,
)