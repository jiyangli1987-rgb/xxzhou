from agentscope.tool import ToolResponse
from agentscope.message import (
    Msg, 
    TextBlock,
    ImageBlock,
    Base64Source
)
from agents.image_reader import image_reader_agent
import asyncio

async def images_reader(prompt:str,image_dir:str):
    """
    根据用户的提示词，识别并分析图片的内容
    :param prompt: 用户的提示词
    :param image_dir:图片的本地位置
    """

    msg = Msg(
        name="user",
        role="user",
        content=[
            TextBlock(
                type="text",
                text=prompt
            ),
            ImageBlock(
                type="image",
                # 应该换成本地图片
                source=Base64Source(
                    type="url",
                    url=image_dir
                )
            )
        ]
        
    )

    res = await image_reader_agent(msg)
    print(res)
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=res.content[0]["text"]
            )
        ]
    )

