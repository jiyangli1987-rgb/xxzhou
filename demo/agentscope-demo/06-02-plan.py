# -*- coding: utf-8 -*-
"""规划示例的主入口文件"""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.plan import PlanNotebook
from agentscope.tool import (
    Toolkit,
    execute_shell_command,  # 执行shell命令
    execute_python_code,     # 执行Python代码
    write_text_file,         # 写入文本文件
    insert_text_file,        # 向文件插入文本
    view_text_file,          # 查看文本文件内容
)


async def main() -> None:
    """规划示例的主入口函数"""
    # 创建工具包并注册基础工具
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(view_text_file)

    # 创建ReAct智能体，集成规划能力
    agent = ReActAgent(
        name="星期五",
        sys_prompt="""你是一位名为星期五的得力助手。

# 目标
你的核心目标是通过严谨的规划完成指定任务。

# 注意事项
- 你可以使用规划相关的工具，辅助自己完成任务的规划与执行。
- 搜索引擎获取的信息并非绝对准确，你需要从多个信息源收集内容，并经过审慎核实后给出最终答案。
""",  # noqa
        model=DashScopeChatModel(
            model_name="qwen3-max-preview",
            api_key=os.getenv("QWEN_API_KEY"),
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,          # 绑定已注册的工具包
        enable_meta_tool=True,    # 启用元工具（支持规划相关的工具调用）
        plan_notebook=PlanNotebook(),  # 绑定规划笔记本，用于管理任务规划
    )
    # 创建用户智能体（用于与助手智能体交互）
    user = UserAgent(name="用户")

    # 初始化用户消息，下达核心任务
    msg = Msg(
        "user",
        "查看 AgentScope GitHub 代码仓库过去一个月内的近期变更内容。",
        "user",
    )
    # 启动对话循环：智能体执行任务 → 用户交互 → 输入exit退出
    while True:
        msg = await agent(msg)
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break


asyncio.run(main())