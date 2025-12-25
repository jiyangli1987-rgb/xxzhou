import os
from dotenv import load_dotenv
from agentscope.model import DashScopeChatModel

load_dotenv()

class XXzhouModel():
    def __init__(self):
        self.dashcope_api_key = os.getenv("QWEN_API_KEY")

    # qwen-max qwen3-vl-plus
    def get_dashscope_chat_model(self, model_name="qwen-max"):
        return DashScopeChatModel(
            model_name=model_name,
            api_key=self.dashcope_api_key,
            stream=True
        )
