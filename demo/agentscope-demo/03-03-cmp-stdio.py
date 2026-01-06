"""
首先需要再本地启动tavily服务器，才能使用。
set TAVILY_API_KEY="tvly-你的实际API密钥" ; 
npx -y tavily-mcp@0.1.3
"""

import asyncio
import os

from agentscope.agent import ReActAgent,UserAgent

from agentscope import logger
from agentscope.formatter import DashScopeChatFormatter
from agentscope.message import Msg
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.mcp import StdIOStatefulClient
from dotenv import load_dotenv
load_dotenv()

from agentscope.tool import Toolkit

toolkit = Toolkit();


async def main():
    """The main entry point for the Deep Research agent example."""
    logger.setLevel("DEBUG")

    tavily_search_client = StdIOStatefulClient(
        name="my_search",
        command="npx",
        args=["-y", "tavily-mcp@latest"]
    )

    await tavily_search_client.connect()

    await toolkit.register_mcp_client(tavily_search_client)

    

    agent = ReActAgent(
        name="搜索助手",
        sys_prompt="你是一个AI搜索助手，帮我搜索网络上的消息。",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        memory=InMemoryMemory(),
        toolkit=toolkit
    )

    msg = Msg(
        name="晓舟",
        content="帮我搜索智能体开发工程师的岗位要求与薪资待遇，用一句话总结搜索结果。",
        role="user"
    )


    await agent(msg)

    await tavily_search_client.close();

asyncio.run(main())
