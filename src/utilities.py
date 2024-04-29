# ./src/utilities.py

from src.transcribetonic import TranscribeTonic
from src.chat_summary_memory_buffer import ChatSummaryMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI as OpenAiLlm
import tiktoken
from global_variables import model, token_limit_full_text , token_limit_sumarizer

class ChatSummarizer:
    def __init__(self, chat_history):
        """
        Initialize the ChatSummarizer with a model, tokenizer, and optional initial chat history.
        
        Parameters:
            model (str): The model name for the LLM.
            tokenizer (Callable): The tokenizer function for the respective model.
            chat_history (List[ChatMessage], optional): Initial chat history. Defaults to None.
            token_limit (int): Token limit for the chat memory buffer. Defaults to 900.
        """
        self.model = model
        self.tokenizer = tokenizer_fn
        self.summarizer_llm = OpenAiLlm(model_name=self.model, max_tokens=token_limit_sumarizer)
        self.memory = ChatSummaryMemoryBuffer.from_defaults(
            chat_history=chat_history,
            summarizer_llm=self.summarizer_llm,
            token_limit_full_text=token_limit_full_text,
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
    def transcriber(audio_location:str):
        tonic_transcriber = TranscribeTonic()
        results:str = tonic_transcriber.transcribe(audio_location)
        # debug print print(results)
        results = {"text":results}
        return results


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