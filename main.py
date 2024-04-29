# main.py

from src.transcribetonic import TranscribeTonic
from src.interface import pitch_helper , pitch_trainer , pitch_tester
from src.azurellm import llm
import gradio as gr
import os
import dotenv
import logging  
from src.utilities import ChatSummarizer , Transcriber
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.core import Settings
from global_variables import embedding_model_name , model
import tiktoken

# from llama_index.llms.azure_openai import AzureOpenAI
import os
import dotenv
dotenv.load_dotenv()

logger = logging.getLogger("pitch-tonic")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

dotenv.load_dotenv()
voyage_api_key = os.environ.get("VOYAGE_API_KEY")
aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
aoai_key = os.environ['AZURE_OPENAI_API_KEY']   
aoai_version = os.environ['AZURE_OPENAI_VERSION']  

Settings.embed_model = VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=voyage_api_key)
Settings.llm = llm
Settings.tokenizer = tiktoken.encoding_for_model(model_name=model).encode 
Settings.chunk_size = 450
Settings.chunk_overlap = 250

if __name__ == "__main__":

    demo = gr.Blocks()
    with demo:
        gr.TabbedInterface([pitch_helper, pitch_tester, pitch_trainer], ["Tonic Pitch Assistant", "Test Your Pitch", "Train For Your Pitch"])

    demo.queue(max_size=5)
    demo.launch(server_name="0.0.0.0", show_api=False)

