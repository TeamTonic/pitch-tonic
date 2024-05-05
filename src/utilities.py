# ./src/utilities.py

from src.transcribetonic import TranscribeTonic
from llama_index.core.memory.chat_summary_memory_buffer import ChatSummaryMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
import tiktoken
from llama_index.core.utils import get_tokenizer
from global_variables import model, token_limit_full_text , token_limit_sumarizer
from typing import List
from llama_index.llms.azure_openai import AzureOpenAI
from global_variables import model, engine
import os
import dotenv
import json
import uuid
from global_variables import pitch_tester_system_prompt, pitch_tester_easy , pitch_tester_medium , pitch_tester_hard , pitch_tester_extreme, pitch_tester_anq_prompt , pitch_tester_anq_easy , pitch_tester_anq_medium , pitch_tester_anq_hard , pitch_tester_anq_extreme, pitch_trainer_easy, pitch_trainer_extreme, pitch_trainer_system_prompt, pitch_trainer_medium, pitch_helper_system_prompt, pitch_trainer_hard,  pitch_evaluator_easy , pitch_evaluator_medium , pitch_evaluator_hard , pitch_evaluator_extreme

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
    def __init__(self, audio_location: str): 
        self.audio_location = audio_location

    @staticmethod
    def transcribe(self):
        tonic_transcriber = TranscribeTonic()
        transcription:str = tonic_transcriber.transcribe(self.audio_location)
        print(transcription)
        return {"text": transcription}

class MessageProcessor:
        
    first_query = True

    # Creating a template for generating questions based on difficulty
    anq_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, {difficulty} please create a complete question:"
    )
    report_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, {difficulty} please create a complete evaluation:"
    )

    retrieval_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, {difficulty} please create a complete evaluation:"
    )

    helper_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, please create a complete evaluation:"
    )
    evaluation_template = PromptTemplate(
        "We have provided context information below. \n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Given this information, please create a complete evaluation:"
    )

    def __init__(self, chat_history, retriever):
        """
        Initialize the Processor with a ChatSummarizer instance.

        Parameters:
            summarizer (ChatSummarizer): Instance of ChatSummarizer.

        """
        self.chat_history = chat_history
        self.retriever = retriever
        self.llm = AzureAIManager.get_llm()
        self.summarizer = ChatSummarizer(chat_history=chat_history)
    
    def return_complete_user_message(self, audio_location, additional_text):

        # Transcribe the audio
        transcription = Transcriber.transcribe(audio_location=audio_location)['text']
        # Combine transcribed audio with additional text
        combined_text = transcription
        if additional_text:
            combined_text += " " + additional_text
            
        # from llama_index.core.llms import ChatMessage, MessageRole
        current_user_message = ChatMessage(
            content=combined_text,
            )

        user_message, history = MessageProcessor.format_user_query(query=current_user_message)
        return user_message, history

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
        return message, history

    def add_system_response(self, response):
        """
        Updates memory by adding a system response message.

        Parameters:
            response (str): The system's response in string format.
        """
        system_message = ChatMessage(role=MessageRole.SYSTEM, content=response)
        self.summarizer.update_chat_history([system_message])

    # def create_question(self, query_str=[], difficulty="extreme"):
    #     """
    #     Retrieves context based on a query and uses it to ask a question
    #     based on the specified difficulty.

    #     Args:
    #         query_str (str): The query string to retrieve context.
    #         difficulty (str): The level of difficulty to adjust the subsequent prompt.

    #     Returns:
    #         str: A formatted question prompt for user interaction.
    #     """
    #     # Retrieve context based on the query string
    #     context = self.retriever.search(query_str)

    #     if context is None:
    #         return "Unable to retrieve relevant context. Please try a different query."

    #     # Create text prompt based on the retrieved context and difficulty
    #     question = self.anq_template.format(context_str=json.dumps(context), difficulty=difficulty)
        
    #     return question

    def pitch_helper_handler(self,drop_down_value:str,audio_input:str, additional_text , retriever):
        """
        Processes audio input through transcription, combines it with any additional text,
        and uses PitchHelper to generate a helpful response in a chat context.

        Args:
            audio_input (str): File path to audio input.
            additional_text (str): Additional text input from the user.

        Returns:
            str: The combined and processed response from the pitch helper system.
        """     
        chat_memory = self.chat_history
        retriever = self.retriever
        llm = self.llm
        complete_text , history = self.return_complete_user_message(drop_down_value=drop_down_value, audio_location=audio_input, additional_text=additional_text)
        context = retriever.search(query=complete_text)
        
        if context is None:
            return "Unable to retrieve relevant context. Please try a different query."

        # Create text prompt based on the retrieved context and difficulty
        formatted_message = self.retrieval_template.format(context_str=json.dumps(context))
        self.summarizer.update_chat_history(new_messages=formatted_message)
        messages = self.summarizer.get_history()
        response = llm.chat(messages)
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
        first_query = self.first_query
        chat_memory = self.chat_history
        retriever = self.retriever
        llm = self.llm

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

        # context = retriever.search(query=complete_text)
        
        # if context is None:
        #     return "Unable to retrieve relevant context. Please try a different query."

        # Create text prompt based on the retrieved context and difficulty
        # Check if it's the first query and set prompts accordingly
        if first_query:
            # Use initial prompts for the first query
            selected_prompt = pitch_tester_system_prompt + " " + initial_difficulty_prompts.get(difficulty, "")
            self.add_system_response(selected_prompt)
            self.first_query = False
            first_query = False
            complete_text , history = self.return_complete_user_message(drop_down_value=difficulty, audio_location=audio_input, additional_text=additional_text)
            context = retriever.search(query=complete_text)
            formatted_message = self.anq_template.format(context_str=json.dumps(context))
            self.summarizer.update_chat_history(new_messages=formatted_message)
            user_query, chat_messages = self.format_user_query(complete_text)
            response = self.llm.chat(chat_messages)
            self.add_system_response(response.response)
            return response.response

        else:
            selected_prompt = pitch_tester_system_prompt + " " + subsequent_difficulty_prompts.get(difficulty, "")
            self.add_system_response(selected_prompt)
            complete_text , history = self.return_complete_user_message(drop_down_value=difficulty, audio_location=audio_input, additional_text=additional_text)
            context = retriever.search(query=complete_text)
            question_prompt = self.anq_template.format(context_str=json.dumps(context))
            self.add_system_response(question_prompt)
            self.summarizer.update_chat_history(new_messages=formatted_message)
            messages = self.summarizer.get_history()
            # user_query, chat_messages = self.format_user_query(complete_text)
            testquestion = llm.chat(messages)
        return testquestion.response

    def pitch_train_handler(self, difficulty: str, audio_location:str,  userquery:str = ""):

        difficulty = {
            'easy': pitch_trainer_easy,
            'medium': pitch_trainer_medium,
            'hard': pitch_trainer_hard,
            'extreme': pitch_trainer_extreme
            }
        selected_prompt = pitch_trainer_system_prompt + " " + difficulty.get(difficulty, "")
    # #   Handler.first_query = False
    #     # Initialize the PitchTester with the combined system prompt
    #     pitch_trainer = PitchTrainer(system_prompt=selected_prompt)
    #     message_formatter = MessageFormatter(pitch_trainer.chat_memory)
        context = self.retriever.search(query=complete_text)

        if context is None:
            return "Unable to retrieve relevant context. Please try a different query."

        evaluation = self.evaluation_template.format(context_str=json.dumps(context), difficulty=difficulty)
        self.add_system_response(evaluation)
        complete_text , history = self.return_complete_user_message(drop_down_value=difficulty, audio_location=audio_location, additional_text=userquery)
        # Process these messages and collect the response
        response = self.llm.chat(history)
        # response += self.create_question(userquery = response.response, difficulty=difficulty)           
        return response.response
    
    def pitch_evaluator(self, difficulty="extreme" , chat_history=[]):
        difficulty = {
            'easy': pitch_evaluator_easy,
            'medium': pitch_evaluator_medium,
            'hard': pitch_evaluator_hard,
            'extreme': pitch_evaluator_extreme
            }
        evaluation = self.report_template.format(difficulty=difficulty.get(difficulty, ""))
        self.add_system_response(evaluation)
        history = self.summarizer.get_history
        response = self.llm.chat(history)
        return response.response