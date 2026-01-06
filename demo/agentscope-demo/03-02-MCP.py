"""
$env:tavily_api_key="tvly-你的实际API密钥" ; 
npx -y tavily-mcp@0.1.3

pip install mcp-tavily
"""

import asyncio
import os

from agentscope.agent import ReActAgent,UserAgent

from agentscope import logger
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.message import Msg
from agentscope.mcp import StdIOStatefulClient,HttpStatelessClient
from dotenv import load_dotenv
from agentscope.tool import (
    Toolkit,
    write_text_file,
    execute_python_code,
    execute_shell_command,
    view_text_file,
    insert_text_file
)
load_dotenv()


async def main() -> None:

    toolkit = Toolkit();    

    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(insert_text_file)

    tavily_search_client = HttpStatelessClient(
        name="tavily_mcp",
        # command="npx",
        # args=["-y", "tavily-mcp@latest"],
        # env={"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")},
        transport="streamable_http",
        url=f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv("TAVILY_API_KEY")}"
    )

    await toolkit.register_mcp_client(tavily_search_client)

    agent = ReActAgent(
        name="搜索助手",
        sys_prompt="你是一个AI搜索助手，帮我搜索网络上的图片，并下载到d盘temp_data目录中。",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen-max",
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        memory=InMemoryMemory(),
        toolkit=toolkit
    )
    
    user = UserAgent(name="晓舟")

    msg = None

    while True:
        msg = await agent(msg)
        msg = await user(msg)

asyncio.run(main())
