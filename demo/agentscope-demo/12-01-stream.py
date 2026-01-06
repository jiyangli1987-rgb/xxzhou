# -*- coding: utf-8 -*-
"""演示如何以流式方式获取智能体输出消息的示例"""
import asyncio
import os
from dotenv import load_dotenv

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.pipeline import stream_printing_messages
from agentscope.tool import (
    Toolkit,
    execute_shell_command,
    view_text_file,
    execute_python_code,
)

load_dotenv();

async def main() -> None:
    """主函数"""
    # 初始化工具集并注册工具函数
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_shell_command)  # 执行Shell命令
    toolkit.register_tool_function(execute_python_code)     # 执行Python代码
    toolkit.register_tool_function(view_text_file)          # 查看文本文件

    # 创建ReAct智能体
    agent = ReActAgent(
        name="星期五",  # 智能体名称（原Friday译为星期五）
        sys_prompt="你是一名名为星期五的得力助手。",
        # 若要更换其他模型，请同步修改model和formatter参数
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),  # 环境变量保留原命名
            model_name="qwen-max",  # 模型名称保留原标识符
            enable_thinking=False,  # 关闭思考过程输出
            stream=True,            # 开启流式输出
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),    # 使用内存存储记忆
    )

    # 构造用户消息
    user_msg = Msg(
        "user",  # 角色标识保留框架约定
        "你好！你是谁？",
        "user",
    )

    # 禁用终端默认打印，避免输出内容混乱
    agent.set_console_output_enabled(False)

    # 以流式方式获取智能体的输出消息
    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(user_msg),
    ):
        print(msg, last)


asyncio.run(main())