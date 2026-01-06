import whisper
import os

video_file_path = "D:/视频下载/轻松学会！高手都在用的AI编程大法！ [BV1ZqmmBJEmP].mp4" 

# 选择模型，'base'是最快、资源消耗最小的选择
model_name = "base" 
# model_name = "medium" # 推荐在GPU环境下使用以获得更好效果

# video_dir = os.path.dirname(video_file_path)
# # 获取不带扩展名的文件名 (如 "your_video")
# video_name_base = os.path.splitext(os.path.basename(video_file_path))[0]

print(f"正在加载 Whisper 模型: {model_name}...")
model = whisper.load_model(model_name)

print(f"正在转录文件: {video_file_path}...")
result = model.transcribe(video_file_path)
transcribed_text = result["text"]
print(transcribed_text)