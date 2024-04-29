# src/pitch_tester.py

from src.chat_summary_memory_buffer import ChatSummaryMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.openai import OpenAI as OpenAiLlm
import tiktoken
from global_variables import chat_history_tester, model, token_limit_full_text
from src.utilities import ChatSummarizer

chat_summarizer = ChatSummarizer()

# src/pitch_helper.py

from src.utilities import ChatSummarizer
from src.upsert_retrieve import DocumentRetriever, DocumentIndexer
from global_variables import pitch_tester_system_prompt, pitch_tester_easy , pitch_tester_medium , pitch_tester_hard , pitch_tester_extreme
from src.azurellm import llm
from llama_index.core.llms import ChatMessage

class PitchTester:
    def __init__(self, system_prompt=pitch_tester_system_prompt):
        """Initializes PitchTester with necessary components for handling chat sessions with document context."""
        self.chat_memory = ChatSummarizer()
        self.index = DocumentRetriever()
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            memory=self.chat_memory,
            system_prompt=system_prompt,
            llm=llm
        )

    def chat_with_Tester(self, messages):
        """
        Processes chat messages through the pitch helper system.
        
        Args:
            messages (list): A list of ChatMessage instances, where each ChatMessage contains 'role' and 'content'.

        Returns:
            Response from the pitch helper system after processing input messages.
        """
        response = self.chat_engine.chat(messages)
        return response