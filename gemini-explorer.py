import vertexai
#import streamlit
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "gemini-explorer-424303"
vertexai.init(project=project)

config = generative_models.GenerationConfig(temperature=0.4)
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
chat=model.start_chat()

print('What do you want to say to Gemini?\n')
response = input("Please Type your prompt here: ")

while(response.lower() != 'no'):
    gem = chat.send_message(response)
    print("Gemini: " + gem.text + "\n")
    response = input("Please Type your prompt here: ")
