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
from tools.images_tool import create_images


toolkit = Toolkit()
toolkit.register_tool_function(write_text_file)
toolkit.register_tool_function(insert_text_file)
toolkit.register_tool_function(view_text_file)
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)
toolkit.register_tool_function(create_images)

agent = ReActAgent(
    name="晓舟助手",
    sys_prompt="""
    你可以调用create_images工具生成图片。
    注意：如果需要转换本地文件的地址，请按照下面的示例转换,
    "file://D:\\目录1\\目录2\\图片名.png",
    给用户返回的消息要包含生成的图片。
    """,
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    memory=InMemoryMemory(),
    model=dashcope_chat_model
)
