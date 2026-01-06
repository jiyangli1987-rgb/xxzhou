# -*- coding: utf-8 -*-

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
from agentscope.tool import Toolkit

# 创建一个知识库
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


async def main() -> None:

    # 向知识库中存储一些内容用于演示
    # 实际应用中，向量数据库会预先填充相关数据
    
    reader = TextReader(chunk_size=1024, split_by="sentence")
    documents = await reader(
        text=(
            # 用于演示的虚构个人资料
            "我是张三，28岁。我最好的朋友是李四。我住在上海市。我在字节跳动担任软件工程师。"
            "我喜欢徒步旅行和摄影。我的父亲是张建国，是一名医生。我为他感到非常骄傲。"
            "我的母亲是王丽，是一名教师。她非常善良，总是帮助我学习。\n"
            "我现在是清华大学的博士生，专业是计算机科学。我的导师是李教授，她是人工智能领域的顶尖专家。"
            "我已经在NeurIPS和ICML等顶级会议上发表了多篇论文。"
        ),
    )
    await knowledge.add_documents(documents)

    # 创建工具包并注册RAG工具函数
    toolkit = Toolkit()
    toolkit.register_tool_function(
        knowledge.retrieve_knowledge,
        func_description=(  
            "从知识库中检索相关文档，这些文档与张三的个人资料相关。注意`query`参数对检索质量至关重要，"
            "你可以尝试多种不同的查询语句以获得最佳结果。可以调整`limit`和`score_threshold`参数"
            "获取更多或更少的结果。"
        ),
    )

    # 创建智能体和用户角色
    agent = ReActAgent(
        name="星期五",
        sys_prompt=(
            "你是一个名为星期五的乐于助人的助手。"
            "你配备了'retrieve_knowledge'工具，可帮助你了解名为张三的用户的相关信息。"
            "注意：当你无法获取相关结果时，请调整`score_threshold`参数。"
        ),
        toolkit=toolkit,
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen3-max-preview",
        ),
        formatter=DashScopeChatFormatter(),
    )
    user = UserAgent(name="用户")

    # 一个简单的对话循环，以预设问题开始
    msg = Msg(
        "user",
        "我是张三。你知道我父亲的情况吗？",
        "user",
    )
    while True:
        msg = await agent(msg)
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break


asyncio.run(main())