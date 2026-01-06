# -*- coding: utf-8 -*-
"""视频下载与转录功能。"""
import argparse
import os
import subprocess
import whisper
from typing import Literal, Optional
from pydantic import BaseModel
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock
from dotenv import load_dotenv

load_dotenv()


class VideoTranscriberResult(BaseModel):
    """视频转录结果"""

    success: bool
    """操作是否成功"""
    message: str
    """结果消息"""
    video_path: Optional[str] = None
    """视频文件路径"""
    transcript: Optional[str] = None
    """转录文本"""


def download_video(url: str, save_dir: str = "d:/downloads") -> VideoTranscriberResult:
    """
    下载视频并返回具体的文件路径。

    参数:
        url (str): 视频地址（支持bilibili、youtube等yt-dlp支持的平台）
        save_dir (str): 保存目录，默认为 "d:/downloads"

    返回:
        VideoTranscriberResult: 下载结果
    """
    os.makedirs(save_dir, exist_ok=True)

    # 构造命令（-o 指定保存路径和文件名格式）
    output_path = os.path.join(save_dir, "temp.mp4")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        "-o", output_path,
        url
    ]

    try:
        subprocess.run(cmd, check=True, text=True, encoding="utf-8", capture_output=True)
        message = f"下载成功！文件保存至：{output_path}"
        print(message)
        return VideoTranscriberResult(
            success=True,
            message=message,
            video_path=output_path
        )
    except subprocess.CalledProcessError as e:
        error_msg = f"下载失败：{e.stderr[:500]}"  # 限制错误信息长度
        print(error_msg)
        return VideoTranscriberResult(
            success=False,
            message=error_msg
        )
    except Exception as e:
        error_msg = f"下载异常：{str(e)}"
        print(error_msg)
        return VideoTranscriberResult(
            success=False,
            message=error_msg
        )


def get_transcribed_text(video_path: str, model_name: str = "base") -> VideoTranscriberResult:
    """
    从本地视频文件提取字幕。

    参数:
        video_path (str): 视频文件路径
        model_name (str): Whisper 模型名称，默认为 "base"

    返回:
        VideoTranscriberResult: 转录结果
    """
    if not os.path.exists(video_path):
        error_msg = f"视频文件不存在：{video_path}"
        print(error_msg)
        return VideoTranscriberResult(
            success=False,
            message=error_msg
        )

    print(f"正在加载 Whisper 模型: {model_name}...")
    model = whisper.load_model(model_name)

    print(f"正在转录文件: {video_path}...")
    result = model.transcribe(video_path)
    transcribed_text = result["text"]
    print(f"转录完成。文本长度：{len(transcribed_text)} 字符")

    return VideoTranscriberResult(
        success=True,
        message="转录成功",
        video_path=video_path,
        transcript=transcribed_text
    )


def download_and_transcribe(url: str, save_dir: str = "d:/downloads", model_name: str = "base") -> VideoTranscriberResult:
    """
    下载视频并提取字幕的完整流程。

    参数:
        url (str): 视频地址
        save_dir (str): 保存目录，默认为 "d:/downloads"
        model_name (str): Whisper 模型名称，默认为 "base"

    返回:
        VideoTranscriberResult: 完整流程的结果
    """
    print("开始下载视频...")

    # 第一步：下载视频
    download_result = download_video(url, save_dir)
    if not download_result.success:
        return download_result

    print("\n开始转录字幕...")

    # 第二步：转录字幕
    transcribe_result = get_transcribed_text(download_result.video_path, model_name)
    if transcribe_result.success:
        return VideoTranscriberResult(
            success=True,
            message=f"{download_result.message}\n转录成功",
            video_path=download_result.video_path,
            transcript=transcribe_result.transcript
        )
    else:
        return transcribe_result


def download_video_tool(url: str) -> ToolResponse:
    """
    下载视频的工具函数，用于 AgentScope。

    参数:
        url (str): 视频地址

    返回:
        ToolResponse: 工具响应
    """
    result = download_video(url)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=result.message,
            ),
        ]
    )


def transcribe_video_tool(video_path: str) -> ToolResponse:
    """
    转录视频字幕的工具函数，用于 AgentScope。

    参数:
        video_path (str): 视频文件路径

    返回:
        ToolResponse: 工具响应
    """
    result = get_transcribed_text(video_path)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=result.transcript if result.success else result.message,
            ),
        ]
    )


def download_and_transcribe_tool(url: str) -> ToolResponse:
    """
    下载视频并转录字幕的完整工具函数，用于 AgentScope。

    参数:
        url (str): 视频地址

    返回:
        ToolResponse: 工具响应
    """
    result = download_and_transcribe(url)
    content = result.message
    if result.transcript:
        content += f"\n\n字幕内容：\n{result.transcript}"

    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=content,
            ),
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频下载与转录工具")
    parser.add_argument(
        "--action",
        type=str,
        choices=["download", "transcribe", "full"],
        required=True,
        help="执行的操作：download（下载）、transcribe（转录）、full（完整流程）"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="视频URL（用于download和full操作）"
    )
    parser.add_argument(
        "--path",
        type=str,
        help="视频文件路径（用于transcribe操作）"
    )
    parser.add_argument(
        "--save-dir",
        type=str,
        default="d:/downloads",
        help="保存目录（默认为d:/downloads）"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        help="Whisper模型名称（默认为base）"
    )

    args = parser.parse_args()

    if args.action == "download":
        if not args.url:
            print("错误：download 操作需要提供 --url 参数")
            exit(1)
        result = download_video(args.url, args.save_dir)

    elif args.action == "transcribe":
        if not args.path:
            print("错误：transcribe 操作需要提供 --path 参数")
            exit(1)
        result = get_transcribed_text(args.path, args.model)

    elif args.action == "full":
        if not args.url:
            print("错误：full 操作需要提供 --url 参数")
            exit(1)
        result = download_and_transcribe(args.url, args.save_dir, args.model)

    print(f"操作结果：{'成功' if result.success else '失败'}")
    print(f"消息：{result.message}")
    if result.video_path:
        print(f"视频路径：{result.video_path}")
    if result.transcript:
        print(f"字幕内容：\n{result.transcript}")
