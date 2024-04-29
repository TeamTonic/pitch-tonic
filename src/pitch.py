# ./src/pitch.py

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
import os
import dotenv
dotenv.load_dotenv()


aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
aoai_key = os.environ['AZURE_OPENAI_API_KEY']   
aoai_version = os.environ['AZURE_OPENAI_VERSION']  
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

class PitchTonic:
    
    def pitchhelper():
        oaiclient = llm
    
    def pitchtrainer():
        oaiclient = llm

    def pitch_trainer_handler():
        oaiclient = llm

    def pitch_helper_handler():
        oaiclient = llm
