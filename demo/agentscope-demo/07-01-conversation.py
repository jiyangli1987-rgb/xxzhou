# -*- coding: utf-8 -*-
"""演示如何在AgentScope中使用消息中心（MsgHub）和
流水线（pipeline）构建多智能体对话的示例。"""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeMultiAgentFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.pipeline import MsgHub, sequential_pipeline


def create_participant_agent(
    name: str,
    age: int,
    career: str,
    character: str,
) -> ReActAgent:
    """创建一个具有指定姓名、年龄和性格特征的参与方智能体。"""
    return ReActAgent(
        name=name,
        sys_prompt=(
            f"你是一名{age}岁的{career}，名字叫{name}，性格{character}。"
        ),
        model=DashScopeChatModel(
            model_name="qwen-max",  # 模型名称保留原标识符，为通用命名
            api_key=os.getenv("QWEN_API_KEY"),  # 环境变量保留原命名
            stream=True,
        ),
        # 使用多智能体格式化器，因为大语言模型API调用的提示词中
        # 会出现多个实体
        formatter=DashScopeMultiAgentFormatter(),
    )


async def main() -> None:
    """运行多智能体对话工作流。"""

    # 创建多个具有不同特征的参与方智能体
    alice = create_participant_agent("爱丽丝", 30, "教师", "友善")
    bob = create_participant_agent("鲍勃", 14, "学生", "叛逆")
    charlie = create_participant_agent("查理", 28, "医生", "深思熟虑")

    # 创建一个对话场景，参与方在消息中心内进行自我介绍
    async with MsgHub(
        participants=[alice, bob, charlie],
        # 问候消息会在开始时发送给所有参与方
        announcement=Msg(
            "system",  # 角色标识保留原命名，为框架约定
            "现在你们初次见面，请做一个简短的自我介绍。",
            "system",
        ),
    ) as hub:
        # 快速构建流水线来运行对话流程
        await sequential_pipeline([alice, bob, charlie])
        # 也可以通过以下方式执行：
        # await alice()
        # await bob()
        # await charlie()

        # 从消息中心移除一个参与方智能体，并模拟一条广播消息
        print("##### 模拟鲍勃离开的场景 #####")
        hub.delete(bob)
        await hub.broadcast(
            Msg(
                "bob",  # 发送者标识保留原命名，与智能体名对应
                "我现在得去写作业了，回头见！",
                "assistant",  # 角色类型保留原命名，为框架约定
            ),
        )
        await alice()
        await charlie()

        # ...


asyncio.run(main())