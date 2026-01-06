#展示AI思考的中间过程
import gradio as gr
from gradio import ChatMessage
import time

sleep_time = 3  # 每步思考的延迟时间

def simulate_thinking_chat(message, history):
    start_time = time.time()
    # 初始化思考过程消息（状态为"pending"）
    thinking_msg = ChatMessage(
        content="",
        metadata={
            "title": "_思考中_ 逐步分析...",  # 中间过程标题
            "id": 0,
            "status": "pending"  # 状态：待完成
        }
    )
    yield thinking_msg

    # 模拟思考步骤
    thoughts = [
        "首先，我需要理解用户查询的核心需求...",
        "接下来，结合上下文分析可能的回答方向...",
        "然后，梳理关键信息并组织回答结构...",
        "最后，确保回答清晰、准确且完整..."
    ]

    accumulated_thoughts = ""
    for thought in thoughts:
        time.sleep(sleep_time)
        accumulated_thoughts += f"- {thought}\n\n"
        thinking_msg.content = accumulated_thoughts.strip()
        yield thinking_msg  # 流式更新思考过程

    # 更新思考完成状态和耗时
    thinking_msg.metadata["status"] = "done"  # 状态：已完成
    thinking_msg.metadata["duration"] = round(time.time() - start_time, 2)  # 耗时
    yield thinking_msg

    # 发送最终回答
    final_response = ChatMessage(
        content="基于以上思考分析，我的最终回答是：本示例展示了如何在返回最终答案前，逐步显示 LLM 的思考过程。"
    )
    yield [thinking_msg, final_response]  # 同时返回思考过程和最终答案

demo = gr.ChatInterface(
    simulate_thinking_chat,
    title="带思考过程的 LLM 聊天界面 🤔",
)

demo.launch()