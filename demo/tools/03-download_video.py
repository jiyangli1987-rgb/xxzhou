import subprocess
import os

def download_video_with_path(url, save_dir="D:/downloads"):
    # 创建下载目录（不存在则创建）
    os.makedirs(save_dir, exist_ok=True)
    
    # 构造命令（-o 指定保存路径和文件名格式）
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]",
        "-o", os.path.join(save_dir, "%(title)s.%(ext)s"),  # 文件名：视频标题.mp4
        url
    ]
    
    try:
        subprocess.run(cmd, check=True, text=True, encoding="utf-8")
        print(f"下载成功！文件保存至：{save_dir}")
    except subprocess.CalledProcessError as e:
        print(f"下载失败：{e.stderr}")

# 调用函数
download_video_with_path("https://www.bilibili.com/video/BV1YWmgBeEFY", save_dir="D:/downloads")