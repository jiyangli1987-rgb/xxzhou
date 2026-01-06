from email import message
import asyncio,os
from dotenv import load_dotenv
from pyexpat import model
from agentscope.model import DashScopeChatModel,OpenAIChatModel
load_dotenv();
async def main():
    # model = DashScopeChatModel(
    #     model_name="qwen-max",
    #     api_key=os.getenv("QWEN_API_KEY"),
    #     stream=False
    # )
    #接入deepseek
    model = OpenAIChatModel(
        client_args={"base_url":"https://api.deepseek.com"},
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        model_name="deepseek-chat",
        stream=False
    )

    res = await model(
        messages=[
            {"role":"user","content":"你好"}
        ]
    )

    print(res)

asyncio.run(main());