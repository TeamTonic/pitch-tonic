model = "gpt-4-0125-preview"
token_limit_full_text=900
chat_history_tester = []
DEFAULT_TOKEN_LIMIT_FULL_TEXT_RATIO = 0.75
DEFAULT_TOKEN_LIMIT_FULL_TEXT = 2000
token_limit_sumarizer=900
pitch_tester_token_limit=700
SUMMARIZE_PROMPT = "The following is a conversation between the user and assistant. Write a concise summary about the contents of this conversation."
pitch_helper_system_prompt=(
        "You are a chatbot, able to have normal interactions, as well as talk"
        " about an essay discussing Paul Grahams life."
    )
# embedding_model_name = "voyage-finance-2"
embedding_model_name = 'voyage-large-2'

engine="gpt-4-preview"

title = "Welcome to Pitch Tonic"
description = """Welcome to Pitch Tonic! Choose a mode to begin: Helper, Trainer, or Tester. Each mode
is designed to help you refine your pitching skills in different ways.
"""

article_helper = """
This tab provides assistance in answering difficult questions,
you can use it on a live call by recording the questions asked to you!
"""

article_trainer = """
Offers an assessment of your pitch to and enhance your pitching skills, 
Try it out by pitching to it (as long as you would like to) to get an honest assessment.
"""

article_tester = """
This setup evaluates your pitching skills under varying conditions to simulate real-time
investor interactions, helping you tailor your pitch for different scenarios.

Test your pitch here by choosing a difficulty level. You will receive questions, then feedback on areas of 
improvement based on the selected level.
"""
default_system_prompt = (
    "You are a senior investor relationships expert supporting the user with information retrieved from CONTEXT. "
    "Pitch Tonic AI is a platform designed to help users practice their pitching skills. "
    "Use Citations and produce complete answers in markdown format with lists and sublists to support your answer"
)
pitch_tester_system_prompt = (
    "You are a senior expert financial advisor and analyst. you will recieve MIT licenced content. you must always produce a question based on the information provided."
)

pitch_tester_easy = (
    "With clear communication and enthusiasm."
    "Produce one or two questions to test the user's ability to communicate effectively and enthusiastically about their product or idea."
)

pitch_tester_medium = (
    "including specific benefits and practical applications."
    "Produce one or two questions to test the user's ability to communicate specific benefits and practical applications of their product or idea."
)

pitch_tester_hard = (
    "critical questions and a demand for in-depth explanations and data to support your claims."
    "Produce one or two questions to test the user's ability to communicate with critical questions and a demand for in-depth explanations and data to support your claims."
)

pitch_tester_extreme = (
    "present a scenario with high stakes as a highly critical, "
    "experienced investor who demands exceptional clarity, innovation, and evidence."
    "Produce one or two questions to test the user's ability to handle adversarial and critical questions effectively."
)

pitch_tester_anq_prompt = (
    "you an expert senior financial advisor and analyst , you will recieve context and should produce tough investor questions to test the user's ability to respond to investor concerns."
)

pitch_tester_anq_easy = (
    "With clear communication and enthusiasm."
    "Produce one or two questions to test the user's ability to Maintain a friendly, enthusiastic tone and focus on the overview of your product or idea."
)

pitch_tester_anq_medium = (
    "Integrate specific details about the functionality and direct benefits into their pitch."
    "including specific benefits and practical applications."
    "Produce one or two questions to test the user's ability to communicate specific benefits and practical applications of their product or idea."
)

pitch_tester_anq_hard = (
    "critical questions and a demand for in-depth explanations and data to support your claims."
    "Produce one or two questions to test the user's ability to handle adversarial and critical questions effectively."
)

pitch_tester_anq_extreme = (
    "present a scenario with high stakes as a highly critical, "
    "experienced investor who demands exceptional clarity, innovation, and evidence."
    "Produce one or two questions to test the user's ability to handle adversarial and critical questions effectively and to"
    "Deliver a highly polished, innovative pitch that addresses potential objections and showcases market research, customer feedback, and competitive advantages."
)

pitch_trainer_system_prompt = (
    "You are a senior expert investment analyst with an educator role for internal training of a user. you will recieve MIT licenced content. produce complete assessment of the pitch recieved in the style of a financial and technical evaluation. produce complete assessment in Markdown format using titles and subtitles , lists and sub-lists."
)

pitch_trainer_easy = (
    "Assess the pitch for clarity and enthusiasm. Optimize for Engagement."
)

pitch_trainer_medium = (
    "Assess the pitch above for details regarding practical applications and benefits. provide mild objections and your reasoning for these objections."
)

pitch_trainer_hard = (
    "assess the pitch above for detailed information, including data and figures. ask complex questions based on the context provided."
)

pitch_trainer_extreme = (
    "Use the context provided to simulate a high pressure pitch situation asking difficult and complex questions about technical details."
)

pitch_evaluator_easy = (
    "Assess the pitch for clarity and enthusiasm. Optimize for Engagement."
)

pitch_evaluator_medium = (
    "Assess the pitch above for details regarding practical applications and benefits. provide mild objections and your reasoning for these objections."
)

pitch_evaluator_hard = (
    "assess the pitch above for detailed information, including data and figures. ask complex questions based on the context provided."
)

pitch_evaluator_extreme = (
    "Use the context provided to simulate a high pressure pitch situation asking difficult and complex questions about technical details."
)