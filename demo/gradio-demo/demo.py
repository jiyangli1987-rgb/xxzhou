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

    agent = ReActAgent(
        name="简历助手",
        sys_prompt="你将D盘temp_data目录作为你的可操作目录，所有关于文件的创建，修改，浏览，都在此目录下进行。",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    async def get_response(message, history):
        thinking_msg = ChatMessage(
            content="",
            metadata={
                "title":"思考中",
                "id":0,
                "status":"pending"
            }
        )

        yield thinking_msg

        msg1 = "思考1\n"
        await asyncio.sleep(3)
        thinking_msg.content += msg1

        yield thinking_msg

        msg2 = "思考2\n"
        await asyncio.sleep(3)
        thinking_msg.content += msg2

        yield thinking_msg

        msg3 = "思考3\n"
        await asyncio.sleep(3)
        thinking_msg.content += msg3

        yield thinking_msg

        thinking_msg.metadata["status"]="done"

        yield thinking_msg

        msg = Msg(
            name="user",
            content=message,
            role="user"
        )
        res = await agent(msg)

        final_response = ChatMessage(
            content=res.content
        )

        yield [thinking_msg,final_response]

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



