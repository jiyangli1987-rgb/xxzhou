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
from llm import dashcope_chat_model


toolkit = Toolkit()
toolkit.register_tool_function(write_text_file)
toolkit.register_tool_function(insert_text_file)
toolkit.register_tool_function(view_text_file)
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)

agent = ReActAgent(
    name="晓舟助手",
    sys_prompt="""
        你是一个聊天机器人
    """,
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    memory=InMemoryMemory(),
    model=dashcope_chat_model
)
