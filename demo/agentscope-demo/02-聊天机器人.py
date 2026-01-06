import asyncio,os,json
from dotenv import load_dotenv
from turtle import mode
from agentscope.agent import ReActAgent, UserAgent
from agentscope.memory import InMemoryMemory
from agentscope.formatter import DashScopeChatFormatter,DashScopeMultiAgentFormatter
from agentscope.model import DashScopeChatModel
from agentscope.message import Msg
from agentscope.pipeline import MsgHub
from agentscope.tool import Toolkit

load_dotenv()

agent = ReActAgent(
    name="晓舟助手",
    sys_prompt="你是一个聊天机器人",
    formatter=DashScopeChatFormatter(),
    memory=InMemoryMemory(),
    toolkit=Toolkit(),
    model=DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=True
    )
)

user = UserAgent(name="晓舟")

async def main():
    msg = None;
    while True:
        msg = await agent(msg)
        msg = await user(msg)

asyncio.run(main())
