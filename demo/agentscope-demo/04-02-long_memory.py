# pip install mem0ai
import os
import asyncio

from agentscope.message import Msg
from agentscope.memory import InMemoryMemory, Mem0LongTermMemory
from agentscope.agent import ReActAgent
from agentscope.embedding import DashScopeTextEmbedding
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit
from dotenv import load_dotenv
load_dotenv()

# 创建 mem0 长期记忆实例
long_term_memory = Mem0LongTermMemory(
    agent_name="Friday",
    user_name="user_123",
    model=DashScopeChatModel(
        model_name="qwen-max-latest",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=False,
    ),
    embedding_model=DashScopeTextEmbedding(
        model_name="text-embedding-v2",
        api_key=os.getenv("QWEN_API_KEY"),
    ),
    on_disk=False,
)


# 基本使用示例
async def basic_usage():
    """基本使用示例"""
    # 记录记忆
    await long_term_memory.record([Msg("user", "我喜欢住民宿", "user")])

    # 检索记忆
    results = await long_term_memory.retrieve(
        [Msg("user", "我的住宿偏好", "user")],
    )
    print(f"检索结果: {results}")


asyncio.run(basic_usage())