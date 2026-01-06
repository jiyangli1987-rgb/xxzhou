# -*- coding: utf-8 -*-
"""收集多个智能体输出消息的示例"""
import asyncio
import os

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeMultiAgentFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.pipeline import MsgHub, stream_printing_messages


def create_agent(name: str) -> ReActAgent:
    """创建指定名称的智能体"""
    return ReActAgent(
        name=name,
        sys_prompt=f"你是一名名为{name}的学生。",
        model=DashScopeChatModel(
            api_key=os.environ["DASHSCOPE_API_KEY"],  # 环境变量保留原命名
            model_name="qwen-max",  # 模型名称保留原标识符
            stream=False,  # 为简化演示关闭流式输出
        ),
        formatter=DashScopeMultiAgentFormatter(),
    )


async def workflow(
    alice: ReActAgent,
    bob: ReActAgent,
    charlie: ReActAgent,
) -> None:
    """多智能体交互的示例工作流"""
    async with MsgHub(
        participants=[alice, bob, charlie],
        announcement=Msg(
            "user",  # 角色标识保留框架约定
            "爱丽丝、鲍勃、查理，欢迎参加本次会议！首先请大家互相认识一下。",
            "user",
        ),
    ):
        # 智能体依次发言
        await alice()
        await bob()
        await charlie()


async def main() -> None:
    """示例程序的主入口"""
    # 创建智能体实例
    alice, bob, charlie = [
        create_agent(_) for _ in ["爱丽丝", "鲍勃", "查理"]
    ]

    # 流式收集并打印多个智能体的输出消息
    async for msg, last in stream_printing_messages(
        agents=[alice, bob, charlie],
        coroutine_task=workflow(alice, bob, charlie),
    ):
        print(msg, last)


asyncio.run(main())