# filesystem:生成html简历

import asyncio
import subprocess
from json import load
from agentscope.agent import ReActAgent,UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    Toolkit, 
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_shell_command,
    execute_python_code,
    ToolResponse
)
import os,asyncio
from agentscope.message import Msg,TextBlock
from dotenv import load_dotenv
load_dotenv();

def download_video(url):
    """根据参数的url下载视频"""
    save_dir = "D:/downloads"
    os.makedirs(save_dir, exist_ok=True)
    
    # 构造命令（-o 指定保存路径和文件名格式）
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        "-o", os.path.join(save_dir, "%(title)s.%(ext)s"),  # 文件名：视频标题.mp4
        url
    ]
    
    try:
        subprocess.run(cmd, check=True, text=True, encoding="utf-8", capture_output=True)
        print(f"下载成功！文件保存至：{save_dir}")
        # 必须返回 ToolResponse 对象
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"下载成功！文件保存至：{save_dir}",
                ),
            ]
        )
    except subprocess.CalledProcessError as e:
        error_msg = f"下载失败：{e.stderr[:500]}"  # 限制错误信息长度
        print(error_msg)
        # 必须返回 ToolResponse 对象
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=error_msg,
                )
            ]
        )
    except Exception as e:
        # 捕获其他可能的异常（如yt-dlp未安装、路径权限等）
        error_msg = f"下载异常：{str(e)}"
        print(error_msg)
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=error_msg,
                )
            ]
        )


async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(download_video)

    agent = ReActAgent(
        name="简历助手",
        sys_prompt="你可以根据用户输入的视频地址，调用download_video工具下载视频。",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    msg = Msg(
        name="user",
        role="user",
        content="下载视频：https://www.bilibili.com/video/BV1YWmgBeEFY"
    )

    res = await agent(msg)
    print(res.content)

asyncio.run(main())
