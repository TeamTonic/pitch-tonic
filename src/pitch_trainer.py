# src/pitch_trainer.py

from src.utilities import ChatSummarizer
from src.upsert_retrieve import DocumentRetriever, DocumentIndexer
from global_variables import pitch_helper_system_prompt
from src.utilities import AzureAIManager
from llama_index.core.llms import ChatMessage

class PitchTrainer:
    def __init__(self):
        """Initializes PitchHelper with necessary components for handling chat sessions with document context."""
        self.chat_memory = ChatSummarizer()
        self.index = DocumentRetriever()
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            memory=self.chat_memory,
            system_prompt=pitch_helper_system_prompt,
            llm=AzureAIManager.get_llm()
        )

    def chat_with_Trainer(self, messages):
        """
        Processes chat messages through the pitch helper system.
        
        Args:
            messages (list): A list of ChatMessage instances, where each ChatMessage contains 'role' and 'content'.

        Returns:
            Response from the pitch helper system after processing input messages.
        """
        response = self.chat_engine.chat(messages)
        return response