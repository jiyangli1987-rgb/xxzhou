from email import message
import asyncio,os
from dotenv import load_dotenv
from pyexpat import model
from agentscope.model import DashScopeChatModel,OpenAIChatModel
load_dotenv();
async def main():
    model = DashScopeChatModel(
        model_name="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        stream=True
    )

    res = await model(
        messages=[
            {"role":"user","content":"帮我写一篇200字作文，随便写就行。"}
        ]
    )
    async for chunk in res:
        print(chunk)


asyncio.run(main());