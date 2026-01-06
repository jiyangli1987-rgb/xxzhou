import gradio as gr

def count_images(message, history):
    # 统计当前上传的图片数
    print(message)
    current_images = len(message["files"])
    # 统计历史对话中的图片总数
    total_history_images = 0
    for msg in history:
        for content in msg["content"]:
            if content["type"] == "file":
                total_history_images += 1
    # 返回统计结果
    return f"本次上传 {current_images} 张图片，累计上传：{total_history_images + current_images} 张"

with gr.Blocks() as demo:
    chat = gr.ChatInterface(
        fn=count_images,
        examples=[{"text": "无文件!!!", "files": []}],  # 示例：无文件上传
        multimodal=True,  # 启用多模态
        textbox=gr.MultimodalTextbox(
            file_count="multiple",  # 支持多文件上传
            file_types=["image"],  # 仅允许上传图片
            sources=["upload"]  # 支持上传和麦克风输入（麦克风用于语音转文字）
        )
    )

demo.launch()