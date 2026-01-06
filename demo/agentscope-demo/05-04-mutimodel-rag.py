# -*- coding: utf-8 -*-
# 安装 matplotlib 库：pip install matplotlib
"""AgentScope中多模态RAG的使用示例"""
import asyncio
import json
import os

from dotenv import load_dotenv
load_dotenv()

from matplotlib import pyplot as plt

from agentscope.agent import ReActAgent
from agentscope.embedding import DashScopeMultiModalEmbedding
from agentscope.formatter import DashScopeChatFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel
from agentscope.rag import ImageReader, SimpleKnowledge, QdrantStore


# 生成示例图片的路径
path_image = "./123.jpg"
# 创建示例图片（包含中文姓名文本）
# plt.figure(figsize=(8, 3))
# plt.text(0.5, 0.5, "My name is Ming Li", ha="center", va="center", fontsize=30)
# plt.axis("off")  # 关闭坐标轴显示
# plt.savefig(path_image, bbox_inches="tight", pad_inches=0.1)
# plt.close()


async def example_multimodal_rag() -> None:
    """多模态RAG使用示例"""
    # 读取图片并将其转换为文档格式
    reader = ImageReader()
    docs = await reader(image_url=path_image)

    # 创建知识库并添加文档
    knowledge = SimpleKnowledge(
        embedding_model=DashScopeMultiModalEmbedding(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="multimodal-embedding-v1",
            dimensions=1024,  # 多模态嵌入向量的维度
        ),
        embedding_store=QdrantStore(
            location=":memory:",  # 内存模式运行（不持久化）
            collection_name="test_collection",  # 向量集合名称
            dimensions=1024,  # 嵌入向量维度需与模型输出一致
        ),
    )

    # 将图片转换后的文档添加到知识库
    await knowledge.add_documents(docs)

    # 创建配备多模态RAG的ReAct智能体
    agent = ReActAgent(
        name="星期五",
        sys_prompt="你是一个名为星期五的乐于助人的助手。",
        model=DashScopeChatModel(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="qwen3-vl-plus",  # 通义千问多模态模型
        ),
        formatter=DashScopeChatFormatter(),
        knowledge=knowledge,  # 为智能体绑定多模态知识库
    )

    # 向智能体发起提问：查询图片信息
    await agent(
        Msg(
            "user",
            "图片上是什么？",
            "user",
        ),
    )

    # 查看智能体是否将检索到的文档存储在内存中
    print("\n智能体内存中存储的检索文档：")
    content = (await agent.memory.get_memory())[-4].content
    print(json.dumps(content, indent=2, ensure_ascii=False))


# 运行多模态RAG示例
asyncio.run(example_multimodal_rag())