import gradio as gr

import random

def random_response(message, history):
    print("###message###")
    print(message)
    print("###history###")
    print(history)
    return random.choice(["Yes", "No"])

gr.ChatInterface(
    fn=random_response, 
    chatbot=gr.Chatbot(label="简历筛选助手"),
    textbox=gr.Textbox(placeholder="请输入"),
    title="简历筛选助手",
    description="这是一个智能体工具"
).launch()