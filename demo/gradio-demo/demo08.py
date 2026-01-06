# 实现流式输出

import gradio as gr
import asyncio
from json import load
from agentscope.agent import ReActAgent,UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    Toolkit, 
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_python_code,
    execute_shell_command
)
import os,asyncio
from dotenv import load_dotenv
from agentscope.message import Msg
from gradio import ChatMessage
import time
load_dotenv();

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    model = DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=True
    )

    async def get_response(message, history):

        res = await model(
            messages=[
                {"role":"user","content":message}
            ]
        )

        async for chunk in res:
            print("########")
            print(chunk);
            yield chunk.content[0]["text"]

    gr.ChatInterface(
        fn=get_response, 
        chatbot=gr.Chatbot(label="简历筛选助手",height=500),
        textbox=gr.Textbox(placeholder="请输入"),
        title="简历筛选助手",
    ).launch(
        css="""
            footer {
                display: none !important;
            }
        """
    )
if __name__ == '__main__':
    asyncio.run(main())



