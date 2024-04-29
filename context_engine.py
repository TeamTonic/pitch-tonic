from llama_index.core.chat_engine.context import ContextChatEngine
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer
from src.upsert_retrieve import DocumentRetriever
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.voyageai import VoyageEmbedding
import os


voyage_api_key = os.environ.get("VOYAGE_API_KEY")
aoai_endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
aoai_key = os.environ['AZURE_OPENAI_API_KEY']   
aoai_version = os.environ['AZURE_OPENAI_VERSION']  

llm = AzureOpenAI(
    # model="YOUR_AZURE_OPENAI_COMPLETION_MODEL_NAME",
    # deployment_name="YOUR_AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME",
    api_key=aoai_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_version,
    )

voyage_sample = VoyageEmbedding(
    voyage_api_key=voyage_api_key,
)

chat_memory = ChatMemoryBuffer(
    token_limit=1000,
    tokenizer_fn=voyage_sample.get_text_embedding
    
)

context_chat_engine = ContextChatEngine(
    retriever=DocumentRetriever,
    llm=llm,
    memory=chat_memory,
    
)

x = 0