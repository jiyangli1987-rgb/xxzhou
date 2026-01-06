import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from agentscope.agent import ReActAgent , UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.memory import InMemoryMemory
from agentscope.message import (
    Msg,
    ImageBlock,
    TextBlock,
    Base64Source
)
from agentscope.tool import (
    Toolkit,
    view_text_file,
    write_text_file,
    insert_text_file,
    execute_python_code,
    execute_shell_command,
    ToolResponse
)

async def view_image_file(file_path: str) -> ToolResponse:
    """
    根据图片路径读取图片，并返回图片消息。

    Args:
        file_path: 图片文件的绝对路径（如"D:/temp_data/resume.png"）
    """

    image_viewer = ReActAgent(
        name="图片浏览员",
        sys_prompt="你来帮我浏览图片内容",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen3-vl-plus",  # 通义千问多模态模型
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
    )

    msg = Msg(
        name="user",
        role="user",
        content=[
            TextBlock(
            type="text",
            text="这张图片的内容是什么？",
        ),
        ImageBlock(
            type="image",
            source=Base64Source(
                type="url",
                url=file_path
            ),
        )
        ]
    )

    res = await image_viewer(msg)

    return ToolResponse(
        content=res.content
    )

async def main() -> None:

    toolkit = Toolkit()

    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(view_image_file)

    # 创建配备多模态RAG的ReAct智能体
    agent = ReActAgent(
        name="星期五",
        sys_prompt="你是一个名为星期五的乐于助人的助手。",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen3-vl-plus",  # 通义千问多模态模型
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        memory=InMemoryMemory(),
        toolkit=toolkit
    )

    user = UserAgent(name="晓舟")

    msg = None

    while True:
        msg = await user(msg)    
        msg = await agent(msg)


asyncio.run(main())