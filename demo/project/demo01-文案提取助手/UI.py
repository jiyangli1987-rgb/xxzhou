import gradio as gr
import asyncio
from dotenv import load_dotenv
from agentscope.message import Msg
from collections import deque  # 用于安全的异步数据传递
from agent import agent
from shared_resources import shared_data

async def main():

    async def get_response(message, history):
        shared_data.clear()
        msg = Msg(
            name="user",
            role="user",
            content=message
        )

        agent_task = asyncio.create_task(agent(msg))
        while not agent_task.done():
            # 检查是否有新的共享数据
            while shared_data:
                data = shared_data.popleft()
                if data["msg"].content[0].get("text"):
                    yield data["msg"].content[0]["text"]

            # 短暂休眠，避免CPU空转
            await asyncio.sleep(0.1)

        if len(shared_data)>0:
            final = shared_data[-1]["msg"].content[0]["text"]
            yield final

    gr.ChatInterface(
        fn=get_response,
        chatbot=gr.Chatbot(label="文案提取助手", height=500),
        textbox=gr.Textbox(placeholder="请输入"),
        title="文案提取助手"
    ).launch(
        css="""
            footer {
                display: none !important;
            }
        """
    )