# -*- coding: utf-8 -*-
"""ReAct智能体集成RAG的示例"""
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from agentscope.agent import ReActAgent, UserAgent
from agentscope.embedding import DashScopeTextEmbedding
from agentscope.formatter import DashScopeChatFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.rag import SimpleKnowledge, QdrantStore, TextReader


async def main() -> None:
    """ReAct智能体集成RAG示例的主入口函数"""

    # 创建内存中的知识库实例
    print("正在创建知识库...")
    knowledge = SimpleKnowledge(
        embedding_store=QdrantStore(
            location=":memory:",
            collection_name="test_collection",
            dimensions=1024,  # 嵌入向量的维度
        ),
        embedding_model=DashScopeTextEmbedding(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="text-embedding-v4",
        ),
    )

    # 向知识库中插入一些文档
    # 这一步可以离线完成，且只需执行一次
    print("正在向知识库中插入文档...")
    reader = TextReader(chunk_size=100, split_by="char")
    documents = await reader(
        # 用于演示的虚构个人资料
        "我是张三，28岁。我最好的朋友是李四。我住在上海市。我在字节跳动担任软件工程师。"
        "我喜欢徒步旅行和摄影。我的父亲是张建国，是一名医生。我为他感到非常骄傲。"
        "我的母亲是王丽，是一名教师。她非常善良，总是帮助我学习。\n"
        "我现在是清华大学的博士生，专业是计算机科学。我的导师是李教授，她是人工智能领域的顶尖专家。"
        "我已经在NeurIPS和ICML等顶级会议上发表了多篇论文。",
    )

    print("正在将文档插入知识库...")
    await knowledge.add_documents(documents)

    # 通过`knowledge`参数将知识库集成到ReActAgent中
    print("正在创建智能体...")
    agent = ReActAgent(
        name="星期五",
        sys_prompt="你是一个名为星期五的乐于助人的助手。",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen-max",
        ),
        formatter=DashScopeChatFormatter(),
        # 为智能体配备知识库
        knowledge=knowledge,
        print_hint_msg=True,
    )
    user = UserAgent(name="用户")

    # 开始对话
    print("开始对话...")
    msg = Msg("user", "你知道我最好的朋友是谁吗？", "user")
    while True:
        msg = await agent(msg)
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break


asyncio.run(main())