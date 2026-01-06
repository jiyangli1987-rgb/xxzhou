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
    execute_shell_command,
    execute_python_code
)
import os,asyncio
from agentscope.message import Msg
from dotenv import load_dotenv
load_dotenv();

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="简历助手",
        sys_prompt="你是一个生成图片的机器人。",
        model=DashScopeChatModel(
            model_name="qwen-image-plus",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    msg = Msg(
        name="user",
        role="user",
        content="随机生成一张图片"
    )

    await agent(msg)

asyncio.run(main())
