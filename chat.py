from chatbot.model import start_chatbot, start_chat, shutdown_chatbot

model = start_chatbot()

start_chat(model)

shutdown_chatbot(model)