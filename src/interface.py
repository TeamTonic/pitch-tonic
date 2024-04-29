# ./src/interface.py

import gradio as gr
from src.transcribetonic import TranscribeTonic
from src.pitch_handlers import Handler

transcriber = TranscribeTonic()

title = "Welcome to Pitch Tonic"
description = """This demo helps you practice your pitch in two way : 
1. with help and evaluation of your answers to tough questions.
2. with real time support brining you precise answers to tough investor questions.
upload your documents to get started
"""

pitch_trainer = gr.Interface(
    fn=Handler.pitch_train_handler,
    inputs=[
        gr.Radio(["train", "test"], label="Select How You Would Like To Learn", type="value" ),
        gr.Dropdown(type="value", value="hard", choices=["easy", "medium", "hard", "extreme"]),
        gr.Audio(label="Use Your Microphone For Best Results" , type= "filepath"),
        gr.Textbox(label="Add Additional Information Via Text Here", ),
    ],
    outputs=[
        gr.Textbox(label="Tonic Pitch Trainer", multimodal=True),
        # gr.MultimodalTextbox(label="Tonic Pitch Trainer",file_types=["audio","text"],),
    ],
    allow_flagging="never",
    title=title,
    description=description,
#   article=article,
)

pitch_helper = gr.Interface(
    fn=PitchTonic.pitch_helper_handler,
    inputs=[
        gr.Audio(type="filepath"),
        gr.MultimodalTextbox(file_types=['audio','text']), #, value=['text': 'Ask your Question Here', 'files': [{path: 'docs/audio.wav'}]]) ,
        gr.Checkbox(value=False, label="Return timestamps")
        ],
    outputs=[
        # gr.Textbox(label="Tonic Pitch Helper", multimodal=True),
        # gr.Textbox(label="Tonic Pitch Helper", multimodal=True),
        gr.MultimodalTextbox(label="Tonic Pitch Trainer",file_types=["audio","text"],),
    ],
    allow_flagging="never",
    title=title,
    description=description,
#   article=article,
)

microphone_chunked = gr.Interface(
    fn=transcriber.transcribe,
    inputs=[
        gr.Audio(type="filepath"),
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
    fn=transcriber.transcribe,
    inputs=[
        gr.Audio(label="Audio file", type="filepath"),
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