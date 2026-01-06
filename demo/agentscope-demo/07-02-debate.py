# -*- coding: utf-8 -*-
"""AgentScope中多智能体辩论工作流示例"""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import (
    BaseModel,
    Field,
)

from agentscope.agent import ReActAgent
from agentscope.formatter import (
    DashScopeChatFormatter,
    DashScopeMultiAgentFormatter,
)
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.pipeline import MsgHub

# 辩论题目（数学问题）
topic = (
    "两个圆外切且无相对滑动。圆A的半径是圆B半径的1/3，圆A绕圆B滚动一周回到起始点，"
    "请问圆A总共自转了多少圈？"
)


# 创建两个辩论智能体（爱丽丝和鲍勃），用于围绕该议题展开讨论
def create_solver_agent(name: str) -> ReActAgent:
    """创建解题/辩论智能体"""
    return ReActAgent(
        name=name,
        sys_prompt=f"你是一名名为{name}的辩手。欢迎参加本次辩论比赛，你无需完全认同对方的观点，"
        f"我们的目标是找出正确答案。本次辩论的题目如下：{topic}。请使用中文回答问题。",
        model=DashScopeChatModel(
            model_name="qwen-max",  # 模型名称保留原标识符
            api_key=os.getenv("QWEN_API_KEY"),  # 环境变量保留原命名
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
    )


# 实例化两名辩论智能体
alice, bob = [create_solver_agent(name) for name in ["爱丽丝", "鲍勃"]]

# 创建主持智能体（汇总/裁判角色）
moderator = ReActAgent(
    name="主持人",
    sys_prompt=(
        "你是本次辩论的主持人。将有两名辩手参与辩论比赛，他们会针对以下议题阐述答案和观点：\n"
        "```\n"
        "{topic}\n"
        "```\n"
        "每一轮辩论结束后，你需要评估双方的答案，并判定哪一个是正确的。"
    ),
    model=DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=True,
    ),
    formatter=DashScopeMultiAgentFormatter(),
)


# 主持智能体的结构化输出模型（用于标准化裁判结果）
class JudgeModel(BaseModel):
    """主持智能体的结构化输出模型"""

    finished: bool = Field(
        description="辩论是否已结束",
    )
    correct_answer: str | None = Field(
        description="辩论题目的正确答案（仅当辩论结束时填写，否则为None）",
        default=None,
    )


async def run_multiagent_debate() -> None:
    """运行多智能体辩论工作流"""
    while True:
        # 消息中心（MsgHub）中参与方的回复消息会广播给所有参与方
        async with MsgHub(participants=[alice, bob, moderator]):
            # 向正方（爱丽丝）发送辩论指令
            await alice(
                Msg(
                    "user",  # 角色标识保留原框架约定
                    "你是正方，请阐述你的观点和答案。",
                    "user",
                ),
            )
            # 向反方（鲍勃）发送辩论指令
            await bob(
                Msg(
                    "user",
                    "你是反方，你不认同正方的观点，请给出你的理由和答案。",
                    "user",
                ),
            )

        # 爱丽丝和鲍勃无需知晓主持人的评判结果，因此在消息中心外调用主持智能体
        msg_judge = await moderator(
            Msg(
                "user",
                "现在你已经听取了双方的答案，辩论是否可以结束？你是否能确定正确答案？",
                "user",
            ),
            structured_model=JudgeModel,
        )

        print("【结构化输出】: ", msg_judge.metadata)

        if msg_judge.metadata.get("finished"):
            print(
                "辩论结束，本次题目的正确答案是：",
                msg_judge.metadata.get("correct_answer"),
            )
            break


asyncio.run(run_multiagent_debate())