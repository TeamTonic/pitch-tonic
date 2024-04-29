# src/pitch_helper.py

from src.utilities import ChatSummarizer
from src.upsert_retrieve import DocumentRetriever, DocumentIndexer
from global_variables import pitch_helper_system_prompt
from src.azurellm import llm
from llama_index.core.llms import ChatMessage

class PitchHelper:
    def __init__(self):
        """Initializes PitchHelper with necessary components for handling chat sessions with document context."""
        self.chat_memory = ChatSummarizer()
        self.index = DocumentRetriever()
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            memory=self.chat_memory,
            system_prompt=pitch_helper_system_prompt,
            llm=llm
        )

    def chat_with_helper(self, messages):
        """
        Processes chat messages through the pitch helper system.
        
        Args:
            messages (list): A list of ChatMessage instances, where each ChatMessage contains 'role' and 'content'.

        Returns:
            Response from the pitch helper system after processing input messages.
        """
        response = self.chat_engine.chat(messages)
        return response
    
# # Example usage and testing outside in a separate module or testing block.
# if __name__ == "__main__":
#     pitch_helper_instance = PitchHelper()
#     example_chat_messages = [
#         ChatMessage(role="system", content="You are a pirate with a colorful personality."),
#         ChatMessage(role="user", content="Hello")
#     ]
#     response = pitch_helper_instance.chat_with_helper(example_chat_messages)
#     print(response)
# ```