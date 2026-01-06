import gradio as gr

def prefill_chatbot(choice):
    # 根据选择预填充不同的对话历史
    if choice == "问候":
        return [
            {"role": "user", "content": "你好！"},
            {"role": "assistant", "content": "你好！有什么可以帮你的吗？"}
        ]
    elif choice == "投诉":
        return [
            {"role": "user", "content": "我对服务不满意。"},
            {"role": "assistant", "content": "很抱歉给你带来不好的体验。能详细说说具体问题吗？"}
        ]
    else:
        return []  # 清空聊天记录

def random_response(message, history):
    return random.choice(["是", "否"])

with gr.Blocks() as demo:
    # 单选框：选择预填充的对话类型
    radio = gr.Radio(["问候", "投诉", "清空"], label="预填充对话")
    # 创建聊天界面
    chat = gr.ChatInterface(random_response, api_name="chat")
    # 绑定单选框变化事件：修改聊天面板内容
    radio.change(prefill_chatbot, inputs=radio, outputs=chat.chatbot_value)

demo.launch()