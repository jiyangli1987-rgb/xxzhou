# filesystem:生成html简历

import asyncio
from json import load
from agentscope.agent import ReActAgent,UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, write_text_file
import os,asyncio
from dotenv import load_dotenv
from agentscope.message import Msg
load_dotenv();

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)

    agent = ReActAgent(
        name="简历助手",
        sys_prompt="你是一个聊天助手",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    user = UserAgent(name="晓舟")

    msg = Msg(
        name="user",
        role="user",
        content="你好"
    )

    res = await agent.reply(msg)
    print(res)
asyncio.run(main())
