# filesystem:生成html简历

import asyncio
from json import load
from agentscope.agent import ReActAgent,UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, write_text_file
import os,asyncio
from dotenv import load_dotenv
load_dotenv();

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)

    agent = ReActAgent(
        name="AI助手",
        sys_prompt="你可以帮我生成图片",
        model=DashScopeChatModel(
            model_name="qwen-vl-image",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    user = UserAgent(name="晓舟")

    msg = None

    while True:
        msg = await agent(msg)
        msg = await user(msg)

asyncio.run(main())
