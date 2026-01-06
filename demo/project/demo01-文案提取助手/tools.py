import whisper,subprocess
from agentscope.tool import ToolResponse
import os
from agentscope.message import TextBlock
from dotenv import load_dotenv
load_dotenv();

def get_transcribed_text():
    """
    从本地视频d:/downloads/temp.mp4文件提取字幕
    :return: 优化后的字幕文本
    """
    path = "d:/downloads/temp.mp4"
    model_name = "base" 
    # model_name = "medium" # 推荐在GPU环境下使用以获得更好效果

    print(f"正在加载 Whisper 模型: {model_name}...")
    model = whisper.load_model(model_name)

    print(f"正在转录文件: {path}...")
    result = model.transcribe(path)
    transcribed_text = result["text"]
    print(transcribed_text)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=transcribed_text,
            ),
        ]
    )


def download_video(url):
    """
    下载视频并返回具体的文件路径（关键优化：返回完整路径）
    :param url: 视频地址（支持bilibili、youtube等yt-dlp支持的平台）
    :return: 下载成功的提示
    """
    save_dir = "D:/downloads"
    os.makedirs(save_dir, exist_ok=True)
    
    # 构造命令（-o 指定保存路径和文件名格式）
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        "-o", os.path.join(save_dir, "temp.mp4"),  # 文件名：视频标题.mp4
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

