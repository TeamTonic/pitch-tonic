# main.py

from src.transcribetonic import TranscribeTonic
from src.interface import pitch_helper , pitch_trainer
import gradio as gr
import os
import dotenv
import logging  

logger = logging.getLogger("pitch-tonic")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

dotenv.load_dotenv()



if __name__ == "__main__":



    demo = gr.Blocks()
    with demo:
        gr.TabbedInterface([pitch_trainer, pitch_helper], ["Practice Your Pitch", "Tonic Pitch Assistant"])
    demo.queue(max_size=5)
    demo.launch(server_name="0.0.0.0", show_api=False)

