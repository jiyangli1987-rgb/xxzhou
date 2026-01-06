import gradio as gr
import random

# 示例代码模板
example_code = """
以下是 Python  lambda 函数示例：

lambda x: x + {}

这是否正确？
"""

def chat(message, history):
    if message == "是的，这是正确的。":
        return "太棒了！"
    else:
        # 返回带预设选项的响应
        return gr.ChatMessage(
            content=example_code.format(random.randint(1, 100)),  # 随机填充数字
            options=[
                {"value": "是的，这是正确的。", "label": "正确"},  # 显示标签"正确"，实际发送值为完整文本
                {"value": "不正确"}  # 无标签时，显示值本身
            ]
        )

demo = gr.ChatInterface(
    chat,
    examples=["写一个 Python lambda 函数示例。"],
    api_name="chat",
)

demo.launch()