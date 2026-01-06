import os
from dotenv import load_dotenv
from agentscope.model import DashScopeChatModel

load_dotenv()

dashcope_chat_model=DashScopeChatModel(
    model_name="qwen-max",
    api_key=os.getenv("QWEN_API_KEY"),
    stream=True
)