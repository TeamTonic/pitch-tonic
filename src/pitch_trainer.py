# src/pitch_trainer.py

from src.chat_summary_memory_buffer import ChatSummaryMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI as OpenAiLlm
import tiktoken
from global_variables import chat_history_tester, model, token_limit_full_text
from src.utilities import ChatSummarizer

chat_summarizer = ChatSummarizer()

class PitchTonic:
    

    
    def pitch_trainer(text):
        print(text)
        oaiclient = llm