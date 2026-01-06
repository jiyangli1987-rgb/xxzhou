from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv

load_dotenv()

tool = TavilySearch(
    max_results=5,  # 最多返回5条结果
    topic="news"    # 限定搜索新闻类
)

result = tool.invoke({"query": "今天天气怎么样？"})
print(result)