from agentscope.model import DashScopeChatModel
import os,json
import asyncio
from dotenv import load_dotenv
from agentscope.formatter import DashScopeMultiAgentFormatter
from agentscope.agent import ReActAgent
from agentscope.pipeline import MsgHub
from agentscope.message import Msg

load_dotenv();

model = DashScopeChatModel(
    model_name="qwen-max",
    api_key=os.getenv("QWEN_API_KEY")
)

formatter = DashScopeMultiAgentFormatter();

alice = ReActAgent(
    name = "alice",
    formatter=formatter,
    model=model,
    sys_prompt="你是一个名为Alice的学生"
)

bob = ReActAgent(
    name = "bob",
    formatter=formatter,
    model=model,
    sys_prompt="你是一个名为Bob的学生"
)

charlie = ReActAgent(
    name = "charlie",
    formatter=formatter,
    model=model,
    sys_prompt="你是一个名为Charlie的学生"
)

async def example_msghub():
    async with MsgHub(
        [alice,bob,charlie],
        announcement=Msg(
            "system",
            "现在大家互相认识一下，随便聊点什么",
            "system"
        )
    ):
        await alice()
        await bob()
        await charlie()

asyncio.run(example_msghub())

async def example_memory():
    print("Alice的记忆：")
    for msg in await alice.memory.get_memory():
        print(
            f"{msg.name}: {json.dumps(msg.content, indent=4, ensure_ascii=False)}",
        )
        print("#"*20)

asyncio.run(example_memory())