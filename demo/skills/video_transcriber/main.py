# -*- coding: utf-8 -*-
"""视频转录器智能助手的主入口点。"""
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
    """视频转录器智能助手的主入口点。"""
    toolkit = Toolkit()

    # 要使用代理技能，代理必须配备文本文件查看工具
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(view_text_file)

    # 注册视频转录器技能
    toolkit.register_agent_skill(
        "./agentscope-demo/video_transcriber/skill/video-transcription-zh",
    )

    agent = ReActAgent(
        name="视频助手",
        sys_prompt="""你是一个专业的视频处理智能助手。

# 能力介绍
- 能够下载来自各种平台的视频（B站、YouTube等）
- 可以使用Whisper模型提取视频中的字幕
- 支持中英文视频的字幕转录

# 重要提示
- 你对视频处理的所有知识都必须来自你配备的技能。
- 在处理视频时，请先确认用户是否已安装必要的依赖（如yt-dlp、whisper）。
- 处理大型视频文件时，请提醒用户耐心等待。

# 使用说明
用户可以要求你：
1. 下载指定URL的视频
2. 从本地视频文件提取字幕
3. 下载视频并同时提取字幕的完整流程""",  # noqa: E501
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
        "\033[1;32m对问题'你能帮我做什么？'的回答：\033[0m",
    )
    # 准备两个问题
    await agent(
        Msg("user", "你能帮我做什么？", "user"),
    )

    print(
        "\n\033[1;32m对问题'如何下载B站视频并提取字幕？'的回答：\033[0m",
    )
    # 第二个问题
    await agent(
        Msg(
            "user",
            "下载视频：https://www.bilibili.com/video/BV1fFiwBoEAw",
            "user",
        ),
    )


asyncio.run(main())
