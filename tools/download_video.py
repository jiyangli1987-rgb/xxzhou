import subprocess,os
from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

def download_video(url,save_dir):
    """
    下载视频并返回具体的文件路径（关键优化：返回完整路径）
    :param url: 视频地址（支持bilibili、youtube等yt-dlp支持的平台）
    :param save_dir: 视频保存的本地路径
    :return: 下载成功的提示
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # 构造命令（-o 指定保存路径和文件名格式）
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        # 使用 %(title)s 获取标题，%(ext)s 自动获取后缀名
        "-o", os.path.join(save_dir, "%(title)s.%(ext)s"),
        url
    ]
        
    subprocess.run(cmd, check=True, text=True, encoding="utf-8", capture_output=True)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=f"下载成功！文件保存至：{save_dir}",
            ),
        ]
    )
    