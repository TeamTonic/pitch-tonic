# main.py
from global_variables import token_limit_sumarizer
from llama_index.core.base.llms.types import (
    ChatMessage,
    )
from src.interface import pitch_helper , pitch_trainer , pitch_tester
from src.utilities import AzureAIManager
import gradio as gr
import os
import dotenv
import logging  
from llama_index.embeddings.voyageai import VoyageEmbedding
from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser
from llama_index.core.memory.chat_summary_memory_buffer import  ChatSummaryMemoryBuffer
from llama_index.core import Settings, VectorStoreIndex, StorageContext
from global_variables import embedding_model_name , model, default_system_prompt, token_limit_sumarizer
import tiktoken
from src.utilities import AzureAIManager, generate_unique_name
from src.upsert_retrieve import DocumentIndexer, DocumentRetriever
# from src.pitch_handlers import Handler
# from src.utilities import Ha
from src.transcribetonic import TranscribeTonic
import voyageai
from voyageai import Client as VoyageClient

if __name__ == "__main__":
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
    voyageai.api_key = voyage_api_key  
    voyage_client = VoyageClient(os.getenv("VOYAGE_API_KEY"))

    aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
    aoai_key = os.environ['AZURE_OPENAI_API_KEY']   
    aoai_version = os.environ['AZURE_OPENAI_VERSION']  
    mongo_uri = os.environ['AZURE_COSMOSDB_MONGODB_URI']
    mongo_db_name = "tonic-data"
    mongo_db_collection_name = "tonic-collection"

    Settings.chunk_size = 450
    Settings.chunk_overlap = 250
    Settings.embed_model = VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=voyage_api_key)
    Settings.tokenizer = voyage_client.tokenize
    Settings.text_splitter = SentenceSplitter(chunk_size=450, chunk_overlap=200)
    Settings.node_parser = MarkdownNodeParser()
    Settings.llm = AzureAIManager()
    Settings.transformations = [
        SentenceSplitter(chunk_size=450, chunk_overlap=200), MarkdownNodeParser() , VoyageEmbedding(model_name=embedding_model_name, voyage_api_key=voyage_api_key)
    ]
    base_db_name = "pitch-tonic"
    base_collection_name = "pitch-tonic"
 
    # Generate unique names for the session
    mongo_db_name = generate_unique_name(base_db_name)
    mongo_db_collection_name = generate_unique_name(base_collection_name)
    

    # Init Chat History & Mempory
    chat_history = [ChatMessage()]
    chat_memory = ChatSummaryMemoryBuffer(
        token_limit=token_limit_sumarizer,
        chat_history=chat_history,
        )

    # Init Vector Store
    document_indexer = DocumentIndexer(mongo_uri=mongo_uri, db_name=mongo_db_name, collection_name=mongo_db_collection_name)
    vector_store = document_indexer.index_documents()

    # Init Retriever
    retriever = DocumentRetriever(connection_string=mongo_uri, db_name=mongo_db_name, collection_name=mongo_db_collection_name)

    # init transcription
    init_transcription = TranscribeTonic().transcribe("./res/audio/Rec.wav")

    # init Handler
    # Handler(retriever=retriever)

    demo = gr.Blocks()
    with demo:
        gr.TabbedInterface([pitch_helper, pitch_tester, pitch_trainer], ["Tonic Pitch Assistant", "Test Your Pitching", "Train For Your Pitch"])

    demo.queue(max_size=5)
    demo.launch(server_name="localhost", show_api=False)