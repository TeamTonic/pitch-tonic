# ./src/interface.py

import gradio as gr
from src.transcribetonic import TranscribeTonic
from src.pitch_handlers import Handler
from global_variables import title , description , article_trainer , article_helper , article_tester

transcriber = TranscribeTonic()

pitch_trainer = gr.Interface(
    fn=Handler.pitch_train_handler,
    inputs=[
        gr.Dropdown(type="value", value="hard", choices=["easy", "medium", "hard", "extreme"]),
        gr.Audio(label="Use Your Microphone For Best Results" , type= "filepath"),
        gr.Textbox(label="Add Additional Information Via Text Here", ),
    ],
    outputs=[
        gr.Textbox(label="Tonic Pitch Trainer"),
    ],
    allow_flagging="never",
    title=title,
    description=description,
    article=article_trainer,
)


pitch_tester = gr.Interface(
    fn=Handler.pitch_test_handler,
    inputs=[
        gr.Dropdown(type="value", value="hard", choices=["easy", "medium", "hard", "extreme"]),
        gr.Audio(label="Use Your Microphone For Best Results" , type= "filepath"),
        gr.Textbox(label="Add Additional Information Via Text Here", ),
    ],
    outputs=[
        gr.Textbox(label="Tonic Pitch Trainer"),
    ],
    allow_flagging="never",
    title=title,
    description=description,
    article=article_tester,
)

pitch_helper = gr.Interface(
    fn=Handler().pitch_helper_handler,
    inputs=[
        gr.Dropdown(type="value", value="hard", choices=["easy", "medium", "hard", "extreme"]),
        gr.Audio(type="filepath"),
        gr.Textbox(label="Add Additional Information Via Text Here", ),
        ],
    outputs=[
        gr.Textbox(label="Tonic Pitch Helper"),
    ],
    allow_flagging="never",
    title=title,
    description=description,
    article=article_helper,
)
