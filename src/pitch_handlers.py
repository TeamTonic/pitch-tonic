# ./src/pitch_handlers.py
import json
from src.pitch_helper import PitchHelper
from src.pitch_tester import PitchTester
from src.pitch_trainer import pass
from src.upsert_retrieve import AzureCosmosDBMongoDBVectorSearch
# from src.transcribetonic import TranscribeTonic
from src.utilities import Transcriber
from src.utilities import MessageFormatter
from global_variables import pitch_tester_system_prompt, pitch_tester_easy , pitch_tester_medium , pitch_tester_hard , pitch_tester_extreme, pitch_tester_anq_prompt , pitch_tester_anq_easy , pitch_tester_anq_medium , pitch_tester_anq_hard , pitch_tester_anq_extreme
from llama_index.core import PromptTemplate


class Handler:
    
    first_query = True

    # Creating a template for generating questions based on difficulty
    anq_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, {difficulty} please create a complete question:"
    )

    def __init__(self):
        self.retriever = AzureCosmosDBMongoDBVectorSearch()

    def create_question(self, query_str="", difficulty="extreme"):
        """
        Retrieves context based on a query and uses it to ask a question
        based on the specified difficulty.

        Args:
            query_str (str): The query string to retrieve context.
            difficulty (str): The level of difficulty to adjust the subsequent prompt.

        Returns:
            str: A formatted question prompt for user interaction.
        """
        # Retrieve context based on the query string
        context = self.retriever.search(query_str)

        if context is None:
            return "Unable to retrieve relevant context. Please try a different query."

        # Create text prompt based on the retrieved context and difficulty
        question = self.qa_template.format(context_str=json.dumps(context), difficulty=difficulty)
        
        return question

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
        # Transcribe the audio
        transcription = Transcriber.transcriber(audio_location=audio_input)['text']

        # Combine transcribed audio with additional text
        combined_text = transcription
        if additional_text:
            combined_text += " " + additional_text

        # Initialize PitchHelper and MessageFormatter
        pitch_helper = PitchHelper()
        message_formatter = MessageFormatter(pitch_helper.chat_memory)

        # Format the combined text as a user query in the form of ChatMessage
        chat_messages = message_formatter.format_user_query(combined_text)

        # Use PitchHelper to get responses
        response = pitch_helper.chat_with_helper(chat_messages)

        # Append system's response to chat history
        message_formatter.add_system_response(response)

        # Return response
        return response
    
    def pitch_test_handler(self, audio_input: str, difficulty: str, additional_text: str = ""):
        """
        Handler for pitch training based on the provided audio,
        difficulty level, and additional textual information.

        Args:
            audio_input (str): path to the audio input.
            difficulty (str): difficulty level of training ['easy', 'medium', 'hard', 'extreme'].
            additional_text (str): optional additional text input.

        Returns:
            str: Pitch-related guidance or feedback.
        """

        # Transcribe the audio input
        transcription = Transcriber.transcriber(audio_input)['text']

        # Combine transcribed text with any additional user input
        combined_text = transcription
        if additional_text:
            combined_text += " " + additional_text

        # Define difficulty to prompt mappings
        initial_difficulty_prompts = {
            'easy': pitch_tester_easy,
            'medium': pitch_tester_medium,
            'hard': pitch_tester_hard,
            'extreme': pitch_tester_extreme
        }
        subsequent_difficulty_prompts = {
            'easy': pitch_tester_anq_easy,
            'medium': pitch_tester_anq_medium,
            'hard': pitch_tester_anq_hard,
            'extreme': pitch_tester_anq_extreme
        }

        # Check if it's the first query and set prompts accordingly
        if Handler.first_query:
            # Use initial prompts for the first query
            selected_prompt = pitch_tester_system_prompt + " " + initial_difficulty_prompts.get(difficulty, "")
            Handler.first_query = False
            # Initialize the PitchTester with the combined system prompt
            pitch_tester = PitchTester(system_prompt=selected_prompt)
            message_formatter = MessageFormatter(pitch_tester.chat_memory)

            # Formulate the query as a set of structured chat messages
            chat_messages = message_formatter.format_user_query(combined_text)

            # Process these messages and collect the response
            response = pitch_tester.chat_with_Tester(chat_messages)

            # Update the chat history to include the received response
            message_formatter.add_system_response(response)

            # Return the formulated response
            return response

        else:
            # Use subsequent prompts for additional queries
            testquestion = self.create_question(query_str=selected_prompt)
            return testquestion

    def pitch_train_handler(audio_location:str, userquery:str = ""):
        pass


    @staticmethod
    def reset_session():
        """
        Resets the first_query flag to True. This should be called when starting a new session.
        """
        Handler.first_query = True
