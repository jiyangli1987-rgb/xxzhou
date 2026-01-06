from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量（包含API密钥等配置信息）
load_dotenv()

# 使用环境变量中的配置信息初始化大模型
model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),  
    api_key=os.getenv("DEEPSEEK_API_KEY"),  
    base_url=os.getenv("DEEPSEEK_API_BASE") 
)

# 传入提示词，调用invoke方法获取大模型响应内容
response = model.invoke("今天天气怎么样？")

# 输出模型回复内容
print(response.content)