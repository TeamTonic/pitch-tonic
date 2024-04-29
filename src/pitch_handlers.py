# ./src/pitch.py

# from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.voyageai import VoyageEmbedding # https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/embeddings/llama-index-embeddings-voyageai/llama_index/embeddings/voyageai/base.py
from llama_index.llms.azure_openai import AzureOpenAI
import os
import dotenv
dotenv.load_dotenv()

from src.transcribetonic import TranscribeTonic

# get API key and create embeddings
voyage_api_key = os.environ.get("VOYAGE_API_KEY")
aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
aoai_key = os.environ['AZURE_OPENAI_API_KEY']   
aoai_version = os.environ['AZURE_OPENAI_VERSION']  

embedding_model_name = "voyage-finance-2"  # Please check https://docs.voyageai.com/docs/embeddings for the available models

embed_model = VoyageEmbedding(
    model_name=embedding_model_name, voyage_api_key=voyage_api_key
)

# embeddings = embed_model.get_query_embedding("What is llamaindex?")

# aoai_api_key = "YOUR_AZURE_OPENAI_API_KEY"
# aoai_endpoint = "YOUR_AZURE_OPENAI_ENDPOINT"
# aoai_api_version = "2023-07-01-preview"
llm = AzureOpenAI(
    model="YOUR_AZURE_OPENAI_COMPLETION_MODEL_NAME",
    deployment_name="YOUR_AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME",
    api_key=aoai_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_version,
    )

class Handler:
    
    def pitch_handler(audio_location:str, user_query:str = ""):
        pass
    
    def pitch_train_handler(audio_location:str, pitch_type:bool , difficulty_level:bool, userquery:str = ""):
        oaiclient = llm
