import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    ToolResponse,
    Toolkit,
    execute_python_code,
)


# 创建子智能体的工具函数
async def create_worker(
    task_description: str,
) -> ToolResponse:
    """创建一个子智能体来完成给定的任务。子智能体配备了 Python 执行工具。

    Args:
        task_description (``str``):
            子智能体要完成的任务描述。
    """
    # 为子智能体智能体配备一些工具
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    # 创建子智能体智能体
    worker = ReActAgent(
        name="Worker",
        sys_prompt="你是一个智能体。你的目标是完成给定的任务。",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=False,
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
    )
    # 让子智能体完成任务
    res = await worker(Msg("user", task_description, "user"))
    return ToolResponse(
        content=res.get_content_blocks("text"),
    )


async def run_handoffs() -> None:
    """交接工作流示例。"""
    # 初始化协调者智能体
    toolkit = Toolkit()
    toolkit.register_tool_function(create_worker)

    orchestrator = ReActAgent(
        name="Orchestrator",
        sys_prompt="你是一个协调者智能体。你的目标是通过将任务分解为更小的任务并创建子智能体来完成它们，从而完成给定的任务。",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=False,
        ),
        memory=InMemoryMemory(),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
    )

    # 任务描述
    task_description = "在 Python 中执行 hello world"

    # 创建子智能体来完成任务
    await orchestrator(Msg("user", task_description, "user"))


asyncio.run(run_handoffs())