# 重写relay方法实现流式输出

# 实现智能体的流式输出

import gradio as gr
import asyncio
from json import load
from typing import Any, Type, Optional
from agentscope.agent import ReActAgent, UserAgent, ReActAgentBase
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.memory import InMemoryMemory
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

shared_data = deque()

toolkit = Toolkit()
toolkit.register_tool_function(write_text_file)
toolkit.register_tool_function(insert_text_file)
toolkit.register_tool_function(view_text_file)
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)

class TestAgent(ReActAgentBase):
    def __init__(self):
        super().__init__()
        self.name = "晓舟助手"
        self.sys_prompt = "你是一个聊天机器人"
        self.formatter=DashScopeChatFormatter()
        self.memory=InMemoryMemory()
        self.toolkit = toolkit
        self.model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        )

    async def reply(self, msg: Msg | list[Msg] | None) -> Msg:
        """直接调用大模型，产生回复消息。"""
        await self.memory.add(msg)

        # 准备提示
        prompt = await self.formatter.format(
            [
                Msg("system", self.sys_prompt, "system"),
                *await self.memory.get_memory(),
            ],
        )

        # 调用模型
        response = await self.model(prompt)

        last_chunk = None
        async for chunk in response:
            print(chunk)
            shared_data.append(chunk)
            last_chunk = chunk;

        msg = Msg(
            name=self.name,
            content=last_chunk.content,
            role="assistant",
        )

        # 在记忆中记录响应
        await self.memory.add(msg)

        # 打印消息
        await self.print(msg)
        return msg

async def main():

    agent = TestAgent()

    async def get_response(message, history):
        shared_data.clear()
        msg = Msg(
            name="user",
            role="user",
            content=message
        )

        agent_task = asyncio.create_task(agent(msg))
        while not agent_task.done():
            # 检查是否有新的共享数据
            while shared_data:
                data = shared_data.popleft()
                if data.content[0].get("text"):
                    yield data.content[0]["text"]

            # 短暂休眠，避免CPU空转
            await asyncio.sleep(0.1)

        if len(shared_data)>0:
            final = shared_data[-1].content[0]["text"]
            yield final

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