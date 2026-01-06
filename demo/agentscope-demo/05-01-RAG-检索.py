#pip install nltk
#pip install Qdrant-client
#pip install pypdf

# -*- coding: utf-8 -*-
"""The main entry point of the RAG example."""
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from agentscope.embedding import DashScopeTextEmbedding
from agentscope.rag import (
    TextReader,
    PDFReader,
    QdrantStore,
    SimpleKnowledge,
)


async def main() -> None:
    """流程：
    1.初始化读取器 
    2.读取文本/PDF文档 
    3.构建知识库 
    4.插入文档 
    5.检索查询"""

    # 初始化文本读取器，分块大小为1024个字符
    reader = TextReader(chunk_size=1024)

    # PDF读取器，分块大小同样为1024个字符
    # split_by参数可选：sentence（按句子）/paragraph（按段落）/char（按字符）
    pdf_reader = PDFReader(chunk_size=1024, split_by="sentence")

    # 读取纯文本内容，生成可入库的文档对象列表
    documents = await reader(
        text="晓舟是一名智能体开发工程师。"
        "晓舟今年39岁"
        "晓舟喜欢打游戏",
    )

    # 读取本地PDF文件（示例文件）
    # pdf_path = os.path.join(
    #     os.path.abspath(os.path.dirname(__file__)),
    #     "test.pdf",
    # )
    pdf_documents = await pdf_reader(pdf_path="D:\\AIagent\\test.pdf")

    # 初始化简易知识库，核心配置：
    # 1. 嵌入存储：使用Qdrant向量库（内存模式，不持久化）
    # 2. 嵌入模型：使用通义千问文本嵌入模型
    knowledge = SimpleKnowledge(
        embedding_store=QdrantStore(
            location=":memory:",# 存储位置：内存模式（仅运行时有效，重启丢失）
            collection_name="test_collection",
            dimensions=1024,  # 嵌入向量维度（需与嵌入模型输出维度一致，text-embedding-v4输出1024维）
        ),
        embedding_model=DashScopeTextEmbedding(
            api_key=os.getenv("QWEN_API_KEY"),
            model_name="text-embedding-v4",
        ),
    )

    # 将纯文本文档和PDF文档合并后插入知识库
    # 插入过程：自动将文档分块→生成嵌入向量→存储到Qdrant向量库
    await knowledge.add_documents(documents + pdf_documents)

    # 检索参数：limit（返回最多3条）、score_threshold（相似度阈值返回大于0.7）
    docs = await knowledge.retrieve(
        query="晓舟是谁？",
        limit=3,
        score_threshold=0.7,
    )
    print("Q1: 晓舟是谁？")
    for doc in docs:
        print(
            f"Document ID: {doc.id}, Score: {doc.score}, "
            f"Content: {doc.metadata.content['text']}",
        )

    # Retrieve documents from the PDF file based on a query
    docs = await knowledge.retrieve(
        query="晓舟的爱好是什么？",
        limit=3,
        score_threshold=0.2,
    )
    print("\n\nQ2: 晓舟的爱好是什么？")
    for doc in docs:
        print(
            f"Document ID: {doc.id}, Score: {doc.score}, "
            f"Content: {repr(doc.metadata.content['text'])}",
        )


asyncio.run(main())
