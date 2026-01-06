import gradio as gr
from gradio import ChatMessage
import asyncio
from dotenv import load_dotenv
import mimetypes
import base64
from agentscope.message import (
    Msg,
    Base64Source,
    TextBlock,
    ImageBlock
)
from collections import deque  # 用于安全的异步数据传递
from agents.agent import agent
from agentscope.pipeline import stream_printing_messages

def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

async def main():

    async def get_response(message, history):
        msg = Msg(
            name="user",
            role="user",
            content=f"""
            提示词：{message["text"]}。图片列表：
            """
        )
        for img_path in message["files"]: 
            msg.content += f"file:// + {img_path}；" 

        print("#########")
        print(msg);

        thinking_msg = ChatMessage(
            content="",
            metadata={
                "title": "_思考中_ 逐步操作...",  # 中间过程标题
                "id": 0,
                "status": "pending"  # 状态：待完成
            }
        )

        # 禁用终端默认打印，避免输出内容混乱
        agent.set_console_output_enabled(False)

        # 以流式方式获取智能体的输出消息
        async for msg, last in stream_printing_messages(
            agents=[agent],
            coroutine_task=agent(msg),
        ):
            # print(msg)
            if msg.content[0]["type"]=="tool_use":
                thinking_msg.content = "调用工具:" + msg.content[0]["name"]
                yield thinking_msg
            if msg.content[0]["type"]=="text":
                thinking_msg.metadata["status"] = "done"
                # yield msg.content[0].get("text")
                yield msg.content[0].get("text")
                if last:
                    yield msg.content[0].get("text")

    title="封面生成器"

    gr.ChatInterface(
        fn=get_response,
        chatbot=gr.Chatbot(label=title, height=500),
        # textbox=gr.Textbox(placeholder="请输入"),
        title=title,
        multimodal=True,
        textbox=gr.MultimodalTextbox(
            file_count="multiple",  # 支持多文件上传
            file_types=["image"],  # 仅允许上传图片
            sources=["upload"]  # 支持上传和麦克风输入（麦克风用于语音转文字）
        )
    ).launch(
        css="""
            footer {
                display: none !important;
            }
        """
    )