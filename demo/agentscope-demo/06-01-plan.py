# -*- coding: utf-8 -*-
"""手动指定规划示例"""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv();

from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.plan import PlanNotebook, SubTask
from agentscope.tool import (
    Toolkit,
    execute_shell_command,  # 执行shell命令
    execute_python_code,     # 执行Python代码
    write_text_file,         # 写入文本文件
    insert_text_file,        # 插入文本到文件
    view_text_file,          # 查看文本文件内容
)

# 规划笔记本（用于管理规划和子任务）
plan_notebook = PlanNotebook()


async def main() -> None:
    """手动指定规划示例的主入口函数"""

    # 手动创建规划
    await plan_notebook.create_plan(
        name="AgentScope 框架综合分析报告",
        description="研究 AgentScope 的源代码，并撰写一份关于该框架的综合分析报告。",
        expected_outcome="一份Markdown格式的报告，总结AgentScope的功能特性、"
        "架构设计、优缺点以及潜在的优化方向。",
        subtasks=[
            SubTask(
                name="克隆代码仓库",
                description="从 GitHub 上的 agentscope-ai/agentscope 仓库克隆 "
                "AgentScope 代码库，克隆位置是d盘的test目录，并确保获取的是最新版本。",
                expected_outcome="本地拥有一份 AgentScope 代码仓库的完整副本。",
            ),
            SubTask(
                name="查阅文档资料",
                description="查阅代码仓库中 AgentScope 的官方文档，了解框架的核心信息。",
                expected_outcome="全面理解 AgentScope 的功能特性和使用方法。",
            ),
            SubTask(
                name="研究源代码",
                description="深入研究 AgentScope 的源代码，重点分析核心模块及其交互逻辑。",
                expected_outcome="深度理解 AgentScope 的架构设计和具体实现方式。",
            ),
            SubTask(
                name="总结研究成果",
                description="汇总文档查阅和代码研究的成果，撰写一份Markdown格式的综合分析报告。",
                expected_outcome="一份Markdown格式的分析报告。",
            ),
        ],
    )

    # 添加基础工具集
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(view_text_file)

    # 创建智能体
    agent = ReActAgent(
        name="星期五",
        sys_prompt="你是一个名为星期五的得力助手。你的目标是通过严谨的规划完成指定任务。",
        model=DashScopeChatModel(
            model_name="qwen3-max-preview",
            api_key=os.getenv("QWEN_API_KEY"),
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,          # 绑定工具集
        plan_notebook=plan_notebook,  # 绑定规划笔记本
    )
    user = UserAgent(name="用户")

    # 初始化对话消息，启动任务执行
    msg = Msg(
        "user",
        "现在开始按照给定的规划完成任务",
        "user",
    )
    # 对话循环：智能体执行任务 → 用户交互 → 输入exit退出
    while True:
        msg = await agent(msg)
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break


asyncio.run(main())