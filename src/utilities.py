# ./src/utilities.py

from src.transcribetonic import TranscribeTonic
from src.chat_summary_memory_buffer import ChatSummaryMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
# from llama_index.llms.openai import OpenAI as OpenAiLlm
import tiktoken
from llama_index.core.utils import get_tokenizer
from global_variables import model, token_limit_full_text , token_limit_sumarizer
from typing import List
from llama_index.llms.azure_openai import AzureOpenAI
from global_variables import model, engine
import os
import dotenv
import uuid

def generate_unique_name(base_name: str = "Tonic") -> str:
    """ Generate a unique name using a base name and a random UUID. """
    unique_suffix = uuid.uuid4().hex[:6]  
    return f"{base_name}_{unique_suffix}"

class AzureAIManager:
    def __init__(self):
        dotenv.load_dotenv()  # Load environment variables

        # Retrieve environment variables
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.azure_api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.azure_api_version = os.getenv('AZURE_OPENAI_VERSION')

        # Hardcoded or retrieved from environment
        self.engine = engine
        self.model = os.getenv('OPENAI_MODEL', model)  
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '1.0')) 

        # Initialize the Azure OpenAI API
        self.llm = AzureOpenAI(
            engine=self.engine,
            model=self.model,
            temperature=self.temperature,
            api_key=self.azure_api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.azure_api_version,
        )

    def get_llm(self):
        return self.llm

class ChatSummarizer:
    def __init__(self, chat_history:List[ChatMessage]):
        """
        Initialize the ChatSummarizer with a model, tokenizer, and optional initial chat history.
        
        Parameters:
            model (str): The model name for the LLM.
            tokenizer (Callable): The tokenizer function for the respective model.
            chat_history (List[ChatMessage], optional): Initial chat history. Defaults to None.
            token_limit (int): Token limit for the chat memory buffer. Defaults to 900.
        """
        self.model = model
        self.tokenizer = get_tokenizer()
        self.llm = AzureAIManager().get_llm()
        self.chat_history = chat_history
        self.memory = ChatSummaryMemoryBuffer.from_defaults(
            chat_history=chat_history,
            llm=self.llm,
            token_limit=token_limit_full_text,
            tokenizer_fn=self.tokenizer,
        )

    def get_history(self):
        """
        Retrieve the current chat history from memory.
        
        Returns:
            List[ChatMessage]: Current chat history.
        """
        return self.memory.get()

    def update_chat_history(self, new_messages):
        """
        Update the chat history with new messages.

        Parameters:
            new_messages (List[ChatMessage]): New messages to be added to the chat history.
        """
        for message in new_messages:
            self.memory.put(message)

class Transcriber:
    @staticmethod
    def transcribe(audio_location:str):
        tonic_transcriber = TranscribeTonic()
        transcription:str = tonic_transcriber.transcribe(audio_location)
        print(transcription)
        return {"text": transcription}

class MessageFormatter:
    def __init__(self, summarizer):
        """
        Initialize the formatter with a ChatSummarizer instance.

        Parameters:
            summarizer (ChatSummarizer): Instance of ChatSummarizer.

        """
        self.summarizer = summarizer

    def format_user_query(self, query):
        """
        Format and return a list of ChatMessage combining provided query and current chat history.

        Parameters:
            query (str): The user's query in string format.

        Returns:
            List[ChatMessage]: A list of ChatMessage incorporating history and the new user query.
        """
        #format query then add it to the history
        message = [ChatMessage(role=MessageRole.USER, content=query)]
        self.summarizer.update_chat_history([message])
        #return messages with history
        history = self.summarizer.get_history()
        return history

    def add_system_response(self, response):
        """
        Updates memory by adding a system response message.

        Parameters:
            response (str): The system's response in string format.
        """
        system_message = ChatMessage(role=MessageRole.SYSTEM, content=response)
        self.summarizer.update_chat_history([system_message])