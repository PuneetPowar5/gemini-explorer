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
chat = model.start_chat()


# Helper function to send messages between Gimini and User
def llm(chat: ChatSession, user_prompt):

    # Send prompt to Gemini
    gem = chat.send_message(user_prompt)

    # Convert the Gemini response to text
    response = gem.text

    # Display Gemini response to the model
    with st.chat_message("model"):
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
            "role": "model",
            "content": response
        }
    )


# Title the Model
st.title("Gemini Explorer")

# Check to see if there is a chat history initialized
if "conversations" not in st.session_state:
    st.session_state.conversations = []

# Display all chat history to the user
for message in st.session_state.conversations:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Getting the user input
user_input = st.chat_input("Enter your prompt: ")

# Display the user prompt to the model and get the Gemini response
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    llm(chat, user_input)
