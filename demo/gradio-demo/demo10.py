# 实现智能体的流式输出

import gradio as gr
import asyncio
from json import load
from typing import Any, Type, Optional
from agentscope.agent import ReActAgent, UserAgent, ReActAgentBase
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    Toolkit,
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_python_code,
    execute_shell_command
)
import os
from dotenv import load_dotenv
from agentscope.message import Msg
from gradio import ChatMessage
import time
from collections import deque  # 用于安全的异步数据传递

load_dotenv()

async def main():
    # 1. 创建共享数据容器（使用deque保证异步安全）
    shared_data = deque()

    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    agent = ReActAgent(
        name="简历助手",
        sys_prompt="你是一个聊天助手",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    def instance_post_print_hook(
        self: ReActAgentBase,
        kwargs: dict[str, Any],
        output: Any
    ):
        print("~~~~post_print~~~~~")
        print(kwargs)  # 需要传递的kwargs
        print("~~~~end~~~~~")
        # 2. 将kwargs存入共享容器（供get_response读取）
        shared_data.append(("hook_kwargs", kwargs))
        return output

    agent.register_instance_hook(
        hook_type="post_print",
        hook_name="test_post_print",
        hook=instance_post_print_hook
    )

    # 3. 修改get_response为生成器（支持yield流式输出）
    async def get_response(message, history):
        # 重置共享容器（避免历史数据干扰）
        shared_data.clear()

        msg = Msg(
            name="user",
            role="user",
            content=message
        )

        # 启动agent异步任务（不阻塞，同时监听共享容器）
        agent_task = asyncio.create_task(agent(msg))

        # 4. 循环监听共享容器，实时yield钩子传递的kwargs
        while not agent_task.done():
            # 检查是否有新的共享数据
            while shared_data:
                data_type, data = shared_data.popleft()
                if data_type == "hook_kwargs":
                    if data["msg"].content[0].get("text"):
                        yield data["msg"].content[0]["text"]
                    else :
                        data["msg"].content[0]["input"]["content"]

            # 短暂休眠，避免CPU空转
            await asyncio.sleep(0.1)

        # 5. agent任务完成后，获取最终响应并yield
        # res = await agent_task
        # final_history = history + [(message, res.content)]
        # yield final_history

    # 6. Gradio配置：启用流式响应（默认支持生成器）
    gr.ChatInterface(
        fn=get_response,
        chatbot=gr.Chatbot(label="简历筛选助手", height=500),
        textbox=gr.Textbox(placeholder="请输入"),
        title="简历筛选助手"
    ).launch(
        css="""
            footer {
                display: none !important;
            }
        """
    )

if __name__ == '__main__':
    asyncio.run(main())