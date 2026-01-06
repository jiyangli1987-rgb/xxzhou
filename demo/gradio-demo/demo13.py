import gradio as gr
import datetime

def get_response(message, history):
    return f"收到：{message}"

def python_timer_logic(history):
    # 这里写你的 Python 定时逻辑
    now = datetime.datetime.now().strftime("%H:%M:%S")
    history.append({"role": "assistant", "content": f"系统自动推送：当前时间是 {now}"})
    print(now)
    return history

with gr.Blocks() as demo:
    chat = gr.ChatInterface(
        fn=get_response,
        chatbot=gr.Chatbot(height=500)
    )
    
    # 这里的 600 就是你的计时器，由 Python 后端控制频率
    timer = gr.Timer(2) 
    timer.tick(python_timer_logic, inputs=[chat.chatbot], outputs=[chat.chatbot])

demo.launch()