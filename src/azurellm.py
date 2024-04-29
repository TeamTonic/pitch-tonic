from llama_index.llms.azure_openai import AzureOpenAI
from global_variables import model, engine
import os
import dotenv

dotenv.load_dotenv()
aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
aoai_key = os.environ['AZURE_OPENAI_API_KEY']   
aoai_version = os.environ['AZURE_OPENAI_VERSION']  

llm = AzureOpenAI(
    engine="GPT4",
    model=model,
    temperature=0.0,
    api_key=aoai_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_version,
    )
