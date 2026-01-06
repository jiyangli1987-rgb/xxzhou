---
name: 视频下载与转录
description: 此技能提供下载视频并提取字幕的功能，支持多种视频平台。
---

# 视频下载与转录

## 概述

本指南涵盖了下载视频并提取字幕的重要操作。
如果您需要从视频中提取音频字幕，或下载并转录视频内容，此技能将帮助您实现这一目标。

## 快速开始

该技能提供以下关键脚本：

- 下载视频：支持从 bilibili、youtube 等 yt-dlp 支持的平台下载视频
- 提取字幕：使用 Whisper 模型从视频中提取中文/英文字幕
- 完整流程：下载视频并自动提取字幕

## 使用方法

### 下载视频

首先请求用户允许安装必要的依赖（如 yt-dlp）：

```bash
pip install yt-dlp
```

然后运行下载脚本，指定视频 URL：

```python
python video_transcriber_zh.py --action download --url "https://www.bilibili.com/video/..."
```

### 提取字幕

确保已安装 Whisper：

```bash
pip install openai-whisper
```

然后运行字幕提取脚本：

```python
python video_transcriber_zh.py --action transcribe --path "d:/downloads/temp.mp4"
```

### 完整流程

直接运行完整流程：

```python
python video_transcriber_zh.py --action full --url "https://www.bilibili.com/video/..."
```

关于详细用法，请参考位于此 SKILL.md 文件同一文件夹中的 `./video_transcriber_zh.py` 脚本。
