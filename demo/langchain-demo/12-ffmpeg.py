import whisper
import os

# --- 配置参数 ---
# 替换为您的本地 MP4 文件路径
video_file_path = "D:/test/123.mp4" 

# 选择模型，'base'是最快、资源消耗最小的选择
model_name = "base" 
# model_name = "medium" # 推荐在GPU环境下使用以获得更好效果

# 检查文件是否存在
if not os.path.exists(video_file_path):
    print(f"错误：找不到文件 '{video_file_path}'。请检查路径是否正确。")
else:
    try:
        # 1. 确定输出文件的路径和名称
        # 获取视频所在的目录
        video_dir = os.path.dirname(video_file_path)
        # 获取不带扩展名的文件名 (如 "your_video")
        video_name_base = os.path.splitext(os.path.basename(video_file_path))[0]
        # 构建输出的 TXT 文件完整路径
        output_txt_path = os.path.join(video_dir, f"{video_name_base}_transcript.txt")
        
        # 2. 加载 Whisper 模型
        print(f"正在加载 Whisper 模型: {model_name}...")
        model = whisper.load_model(model_name)
        
        # 3. 进行转录
        print(f"正在转录文件: {video_file_path}...")
        result = model.transcribe(video_file_path)
        
        # 4. 保存结果到 TXT 文件
        transcribed_text = result["text"]
        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)
        
        # 5. 输出确认信息
        print("\n--- 任务完成 ---")
        print(f"转录的文本已成功保存到：\n{output_txt_path}")
        print("-------------------\n")

        
    except Exception as e:
        print(f"转录过程中发生错误: {e}")