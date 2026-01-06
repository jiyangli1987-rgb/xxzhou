from agentscope.agent import ReActAgent,ReActAgentBase
from typing import Any
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.memory import InMemoryMemory
from agentscope.tool import (
    Toolkit,
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_python_code,
    execute_shell_command
)
import os
from dotenv import load_dotenv
from agentscope.message import Msg
from collections import deque  # 用于安全的异步数据传递

from tools import get_transcribed_text,download_video

load_dotenv()

toolkit = Toolkit()
toolkit.register_tool_function(write_text_file)
toolkit.register_tool_function(insert_text_file)
toolkit.register_tool_function(view_text_file)
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)
toolkit.register_tool_function(get_transcribed_text)
toolkit.register_tool_function(download_video)

from shared_resources import shared_data

agent = ReActAgent(
    name="晓舟助手",
    sys_prompt="""
        你的核心任务是根据用户提供的视频URL，下载视频或提取视频字幕，步骤如下：
        1. 首先调用 download_video 工具，传入用户提供的视频URL，下载视频。
        2. 如果用户需要提取字幕，则调用 get_transcribed_text 工具，传入视频完整路径。
        3. 接收 get_transcribed_text 返回的优化后字幕。
        4. 字幕可能没有标点符号，也可能存在识别错误，请根据你的理解，适当修改字幕，让字幕内容表达清晰，语义通顺。
    """,
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    memory=InMemoryMemory(),
    model=DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=True
    )
)

def instance_post_print_hook(
    self: ReActAgentBase,
    kwargs: dict[str, Any],
    output: Any
):
    shared_data.append(kwargs)
    return output

agent.register_instance_hook(
    hook_type="post_print",
    hook_name="test_post_print",
    hook=instance_post_print_hook
)