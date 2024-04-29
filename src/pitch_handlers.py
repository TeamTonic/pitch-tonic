# ./src/pitch_handlers.py
from src.pitch_helper import PitchHelper
from src.pitch_tester import pass
from src.pitch_trainer import pass
# from src.transcribetonic import TranscribeTonic
from src.utilities import Transcriber
from src.utilities import MessageFormatter

class Handler:
    
    def pitch_helper_handler(audio_input:str, additional_text):
        """
        Processes audio input through transcription, combines it with any additional text,
        and uses PitchHelper to generate a helpful response in a chat context.

        Args:
            audio_input (str): File path to audio input.
            additional_text (str): Additional text input from the user.

        Returns:
            str: The combined and processed response from the pitch helper system.
        """
        # Step 1: Transcribe the audio
        transcription = Transcriber.transcriber(audio_location=audio_input)['text']

        # Step 2: Combine transcribed audio with additional text
        combined_text = transcription
        if additional_text:
            combined_text += " " + additional_text

        # Step 3: Initialize PitchHelper and MessageFormatter
        pitch_helper = PitchHelper()
        message_formatter = MessageFormatter(pitch_helper.chat_memory)

        # Step 4: Format the combined text as a user query in the form of ChatMessage
        chat_messages = message_formatter.format_user_query(combined_text)

        # Step 5: Use PitchHelper to get responses
        response = pitch_helper.chat_with_helper(chat_messages)

        # Step 6: Append system's response to chat history
        message_formatter.add_system_response(response)

        # Step 7: Return response
        return response
    
    def pitch_train_handler(audio_location:str, pitch_type:bool , difficulty_level:bool, userquery:str = ""):
        pass
