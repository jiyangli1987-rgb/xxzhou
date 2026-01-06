# -*- coding: utf-8 -*-
"""结构化输出示例的主入口文件"""
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
from agentscope.tool import Toolkit

load_dotenv()


class TableModel(BaseModel):
    """用于结构化输出的简易表格模型"""

    name: str = Field(description="人物姓名")
    age: int = Field(description="人物年龄", ge=0, le=120)
    intro: str = Field(description="人物的一句话简介")
    honors: list[str] = Field(
        description="该人物获得的荣誉列表",
    )


class ChoiceModel(BaseModel):
    """用于结构化输出的简易选择模型"""

    choice: Literal["apple", "banana", "orange"] = Field(
        description="你选择的水果（仅可选apple/banana/orange）",
    )


async def main() -> None:
    """结构化输出示例的主入口函数"""
    toolkit = Toolkit()
    agent = ReActAgent(
        name="星期五",  # 智能体名称（原Friday译为星期五）
        sys_prompt="你是一名名为星期五的得力助手。",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),  # 环境变量保留原命名
            model_name="qwen-max",  # 模型名称保留原标识符
            stream=True,            # 开启流式输出
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),    # 使用内存存储记忆
    )

    # 第一个查询：请求介绍爱因斯坦
    query_msg_1 = Msg(
        "user",  # 角色标识保留框架约定
        "请介绍一下爱因斯坦",
        "user",
    )
    res = await agent(query_msg_1, structured_model=TableModel)
    print(
        "结构化输出 1:\n"
        "```\n"
        f"{json.dumps(res.metadata, indent=4, ensure_ascii=False)}\n"  # 新增ensure_ascii=False保证中文正常显示
        "```",
    )

    # 第二个查询：请求选择喜欢的水果
    query_msg_2 = Msg(
        "user",
        "选择一种你最喜欢的水果",
        "user",
    )
    res = await agent(query_msg_2, structured_model=ChoiceModel)
    print(
        "结构化输出 2:\n"
        "```\n"
        f"{json.dumps(res.metadata, indent=4, ensure_ascii=False)}\n"  # 新增ensure_ascii=False保证中文正常显示
        "```",
    )


asyncio.run(main())