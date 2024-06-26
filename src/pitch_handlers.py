# ./src/pitch_handlers.py
import json
from src.pitch_helper import PitchHelper
from src.pitch_tester import PitchTester
from src.pitch_trainer import PitchTrainer
from src.upsert_retrieve import AzureCosmosDBMongoDBVectorSearch
# from src.transcribetonic import TranscribeTonic
from src.utilities import Transcriber
from src.utilities import MessageFormatter
from global_variables import pitch_tester_system_prompt, pitch_tester_easy , pitch_tester_medium , pitch_tester_hard , pitch_tester_extreme, pitch_tester_anq_prompt , pitch_tester_anq_easy , pitch_tester_anq_medium , pitch_tester_anq_hard , pitch_tester_anq_extreme, pitch_trainer_easy, pitch_trainer_extreme, pitch_trainer_system_prompt, pitch_trainer_medium, pitch_helper_system_prompt, pitch_trainer_hard
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from src.upsert_retrieve import DocumentRetriever, DocumentIndexer
from pymongo.mongo_client import MongoClient
from llama_index.core.indices.vector_store import VectorStoreIndex

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

    evaluation_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, {difficulty} please create a complete evaluation:"
    )

    def __init__(self):
        # self.retriever = AzureCosmosDBMongoDBVectorSearch()
        self.chat_memory = []

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
        question = self.anq_template.format(context_str=json.dumps(context), difficulty=difficulty)
        
        return question

    def pitch_helper_handler(self,drop_down_value:str,audio_input:str, additional_text):
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
        transcription = Transcriber.transcribe(audio_location=audio_input)['text']

        # Combine transcribed audio with additional text
        combined_text = transcription
        if additional_text:
            combined_text += " " + additional_text
            
        # from llama_index.core.llms import ChatMessage, MessageRole
        current_user_message = ChatMessage(
            content=combined_text,
            )
        
        import os
        
        azure_conn_string = os.getenv("AZURE_COSMOSDB_MONGODB_URI")
        client = MongoClient(os.getenv('AZURE_COSMOSDB_MONGODB_URI'))
        
        # store = AzureCosmosDBMongoDBVectorSearch(
        #     client,
        #     # db_name=os.getenv('MONGODB_DATABASE'),
        #     # collection_name=os.getenv('MONGODB_VECTORS'), # this is where your embeddings will be stored
        #     # index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index you will need to create
        #     # db_name="Tonic",
        #     # collection_name="sample_collection", # this is where your embeddings will be stored
        #     # index_name="sample_vector_index" # this is the name of the index you will need to create
        # )
        store = AzureCosmosDBMongoDBVectorSearch(
            client,
            db_name="tonic-data",
            collection_name="tonic-collection", # this is where your embeddings will be stored
            # index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index you will need to create
            # db_name="Tonic",
            # collection_name="sample_collection", # this is where your embeddings will be stored
            index_name="Sample" # this is the name of the index you will need to create
        )
        
        index = VectorStoreIndex.from_vector_store(store)
        query_engine = index.as_query_engine(similarity_top_k=20)
        response = query_engine.query("What does the author think of web frameworks?")
        print(response)
        

        
        # retriever = DocumentRetriever(azure_conn_string, "demo_vectordb", "paul_graham_essay")
        
        self.chat_memory.append(current_user_message)

        # Initialize PitchHelper and MessageFormatter
        # pitch_helper = PitchHelper(
        #     chat_memory=self.chat_memory,
        #     index=retriever,
        # )
        # message_formatter = MessageFormatter(pitch_helper.chat_memory)

        # Format the combined text as a user query in the form of ChatMessage
        # chat_messages = message_formatter.format_user_query(combined_text)

        # Use PitchHelper to get responses
        # response = pitch_helper.chat_with_helper(chat_messages)

        # Append system's response to chat history
        # message_formatter.add_system_response(response)

        # Return response
        return response.response
    
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

    def pitch_train_handler(self, difficulty: str, audio_location:str,  userquery:str = ""):

        # Transcribe the audio input
        try:
            transcription = Transcriber.transcribe(audio_location)["text"]
            # Further processing and handling after transcription
            print("Transcribed text:", transcription)
            # More code handling with transcription result...
        except FileNotFoundError as e:
            # Handle scenario where file does not exist
            print(str(e))
        except Exception as e:
            # Handle other exceptions that may occur
            print(f"An error occurred: {str(e)}")
        # Combine transcribed text with any additional user input
        combined_text = transcription
        if userquery:
            combined_text += " " + userquery
        
        difficulty = {
            'easy': pitch_trainer_easy,
            'medium': pitch_trainer_medium,
            'hard': pitch_trainer_hard,
            'extreme': pitch_trainer_extreme
            }
        
    # Check if it's the first query and set prompts accordingly
    # if Handler.first_query:
        # Use initial prompts for the first query
        selected_prompt = pitch_trainer_system_prompt + " " + difficulty.get(difficulty, "")
    #   Handler.first_query = False
        # Initialize the PitchTester with the combined system prompt
        pitch_trainer = PitchTrainer(system_prompt=selected_prompt)
        message_formatter = MessageFormatter(pitch_trainer.chat_memory)
        context = self.retriever.search(combined_text)

        if context is None:
            return "Unable to retrieve relevant context. Please try a different query."

        # Formulate the query as a set of structured chat messages
        chat_messages = message_formatter.format_user_query(combined_text)
        evaluation = self.evaluation_template.format(context_str=json.dumps(context), difficulty=difficulty)

        # Process these messages and collect the response
        response = pitch_trainer.chat_with_Trainer(chat_messages)
        response += evaluation + self.create_question(userquery = response, difficulty=difficulty)           
        return response

    @staticmethod
    def reset_session():
        """
        Resets the first_query flag to True. This should be called when starting a new session.
        """
        Handler.first_query = True
