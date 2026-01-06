import asyncio,os,json
from dotenv import load_dotenv
from turtle import mode
from agentscope.agent import ReActAgent, UserAgent,ReActAgentBase
from agentscope.memory import InMemoryMemory
from agentscope.formatter import DashScopeChatFormatter,DashScopeMultiAgentFormatter
from agentscope.model import DashScopeChatModel
from agentscope.message import Msg
from agentscope.pipeline import MsgHub
from agentscope.tool import Toolkit

load_dotenv()

class TestAgent(ReActAgentBase):
    def __init__(self):
        super().__init__()
        self.name = "晓舟助手"
        self.sys_prompt = "你是一个聊天机器人"
        self.formatter=DashScopeChatFormatter()
        self.memory=InMemoryMemory()
        self.toolkit = Toolkit()
        self.model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        )

    async def reply(self, msg: Msg | list[Msg] | None) -> Msg:
        """直接调用大模型，产生回复消息。"""
        await self.memory.add(msg)

        # 准备提示
        prompt = await self.formatter.format(
            [
                Msg("system", self.sys_prompt, "system"),
                *await self.memory.get_memory(),
            ],
        )

        # 调用模型
        response = await self.model(prompt)

        last_chunk = None
        async for chunk in response:
            print(chunk)
            last_chunk = chunk;

        msg = Msg(
            name=self.name,
            content=last_chunk.content,
            role="assistant",
        )

        # 在记忆中记录响应
        await self.memory.add(msg)

        # 打印消息
        await self.print(msg)
        return msg

agent = TestAgent()

user = UserAgent(name="晓舟")

async def main():
    msg = Msg(
        name="user",
        role="user",
        content="帮我写一篇200字的作文，内容随意。"
    )
    res = await agent(msg)

asyncio.run(main())
