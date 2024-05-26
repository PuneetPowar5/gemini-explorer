import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, ChatSession

project = "gemini-explorer-424303"
vertexai.init(project=project)

config = generative_models.GenerationConfig(temperature=0.4)
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat = model.start_chat(response_validation=False)


# Helper function to send messages between Gimini and User
def llm(chat: ChatSession, user_prompt):

    # Send prompt to Gemini
    gem = chat.send_message(user_prompt)

    # Convert the Gemini response to text
    try:
        response = gem.text
    except ValueError as e:
        response = "I'm sorry, but I couldn't process your request due to " \
                   "safety filters or another issue."

    # Display Gemini response to the model
    with st.chat_message("assistant"):
        st.markdown(response)

    # Record the User input and store it into chat history
    st.session_state.conversations.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Record the Gemini response and store it into chat history
    st.session_state.conversations.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# Title the Model
st.title("Gemini Explorer")

# Create conversations variable to keep track of conversation history in session
if "conversations" not in st.session_state:
    st.session_state.conversations = []

# Create name variable for the session to get users name
if "name" not in st.session_state:
    st.session_state.name = ""

# Create area variable for the session to get the users area
if "area" not in st.session_state:
    st.session_state.area = ""

# Display all chat history to the user
for message in range(len(st.session_state.conversations)):
    # Ignore the first prompt that formats the initial prompt
    if message > 0:
        # Display chat history
        with st.chat_message(st.session_state.conversations[message]["role"]):
            st.markdown(st.session_state.conversations[message]["content"])

# Collect user's name and area before proceeding to chatbot
if st.session_state.name == "" or st.session_state.area == "":
    # Ask the user for their name and what area they are from
    with st.form(key='user_info_form'):
        st.session_state.name = st.text_input("What is your name?", key="name_input_rex")
        st.session_state.area = st.text_input("Where are you from?", key="area_input_rex")
        submitted = st.form_submit_button("Submit")

    # If any of the fields are left empty or the submit button is not pressed
    # The application will stay on the page and wait for users to complete input
    if not submitted or st.session_state.name == "" or st.session_state.area == "":
        st.stop()

# Create initial prompt for the user from Rex
if st.session_state.area and st.session_state.name and len(st.session_state.conversations) == 0:
    # Format the initial prompt to the user
    prompt = "Introduce your self as Rex, the user's assistant powered by " \
             "Google Gemini!. Form the introduction as a format in which you " \
             "sound like you are from " + st.session_state.area + " and you are introducing " \
                                                 "yourself to " + st.session_state.name
    # Display the initial prompt from the chatbot
    llm(chat, prompt)

# Getting the user input
user_input = st.chat_input("Enter your prompt: ")

# Display the user prompt to the model and get the Gemini response
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    llm(chat, user_input)
