# -*- coding: utf-8 -*-
"""中文 Agent Skill 示例的主入口点。"""
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
    Toolkit,
    execute_shell_command,
    execute_python_code,
    view_text_file,
)


async def main() -> None:
    """ReAct 代理中文示例的主入口点。"""
    toolkit = Toolkit()

    # 要使用代理技能，代理必须配备文本文件查看工具
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(view_text_file)

    # 注册代理技能
    toolkit.register_agent_skill(
        "./agentscope-demo/agent_skill_zh/skill/analyzing-agentscope-library-zh",
    )

    agent = ReActAgent(
        name="小智",
        sys_prompt="""你是一个名为小智的智能助手。

# 重要提示
- 不要做任何假设。你对 AgentScope 库的所有知识都必须来自你配备的技能。
""",  # noqa: E501
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen3-max",
            enable_thinking=False,
            stream=True,
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    # 首先，让我们看看代理的系统提示
    print("\033[1;32m代理系统提示：\033[0m")
    print(agent.sys_prompt)
    print("\n")

    print(
        "\033[1;32m对问题'你有什么技能？'的回答：\033[0m",
    )
    # 我们准备两个问题
    await agent(
        Msg("user", "你有什么技能？", "user"),
    )

    print(
        "\n\033[1;32m对问题'如何在 AgentScope 中为代理创建自定义工具函数？'的回答：\033[0m",
    )
    # 第二个问题
    await agent(
        Msg(
            "user",
            "如何在 AgentScope 中为代理创建自定义工具函数？",
            "user",
        ),
    )


asyncio.run(main())
