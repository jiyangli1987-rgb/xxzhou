import asyncio
import json
import os
from dotenv import load_dotenv

from typing import Literal

from pydantic import BaseModel, Field

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, ToolResponse

load_dotenv();

router = ReActAgent(
    name="Router",
    sys_prompt="你是一个路由智能体。你的目标是将用户查询路由到正确的后续任务，注意你不需要回答用户的问题。",
    model=DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=False,
    ),
    formatter=DashScopeChatFormatter(),
)


# 使用结构化输出指定路由任务
class RoutingChoice(BaseModel):
    your_choice: Literal[
        "Content Generation",
        "Programming",
        "Information Retrieval",
        None,
    ] = Field(
        description="选择正确的后续任务，如果任务太简单或没有合适的任务，则选择 ``None``",
    )
    task_description: str | None = Field(
        description="任务描述",
        default=None,
    )


async def example_router_explicit() -> None:
    """使用结构化输出进行显式路由的示例。"""
    msg_user = Msg(
        "user",
        "帮我写一首诗",
        "user",
    )

    # 路由查询
    msg_res = await router(
        msg_user,
        structured_model=RoutingChoice,
    )

    # 结构化输出存储在 metadata 字段中
    print("结构化输出：")
    print(json.dumps(msg_res.metadata, indent=4, ensure_ascii=False))


asyncio.run(example_router_explicit())