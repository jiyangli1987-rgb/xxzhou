# 视频下载与转录技能

这个项目实现了基于 AgentScope 的视频下载与转录技能，模仿了 `agent_skill_zh` 的代码结构。

## 功能特性

- **视频下载**：支持从 bilibili、youtube 等 yt-dlp 支持的平台下载视频
- **字幕提取**：使用 Whisper 模型从视频中提取中文/英文字幕
- **智能代理**：基于 AgentScope 的 ReAct 代理，可以智能处理用户请求

## 目录结构

```
video_transcriber/
├── main.py                          # 主入口文件，运行智能代理
├── README.md                        # 使用说明
└── skill/
    └── video-transcription-zh/      # 技能目录
        ├── SKILL.md                 # 技能描述文档
        └── video_transcriber_zh.py  # 核心功能实现
```

## 安装依赖

```bash
pip install agentscope openai-whisper yt-dlp python-dotenv
```

## 使用方法

### 1. 运行智能代理

```bash
cd agentscope-demo/video_transcriber
python main.py
```

代理会自动加载视频转录技能，并可以回答关于视频处理的问题。

### 2. 直接使用脚本

#### 下载视频
```bash
python skill/video-transcription-zh/video_transcriber_zh.py --action download --url "https://www.bilibili.com/video/..."
```

#### 提取字幕
```bash
python skill/video-transcription-zh/video_transcriber_zh.py --action transcribe --path "d:/downloads/temp.mp4"
```

#### 完整流程（下载+转录）
```bash
python skill/video-transcription-zh/video_transcriber_zh.py --action full --url "https://www.bilibili.com/video/..."
```

## 配置

确保在项目根目录下有 `.env` 文件，并设置必要的 API 密钥：

```env
QWEN_API_KEY=your_api_key_here
```

## 技术实现

- **AgentScope**：提供智能代理框架
- **yt-dlp**：强大的视频下载工具
- **OpenAI Whisper**：先进的语音识别模型
- **ReAct Agent**：基于推理和行动的智能代理

## 参考

- 原项目参考：`./project/demo01-文案提取助手/tools.py`
- 技能结构参考：`./agentscope-demo/agent_skill_zh/`
