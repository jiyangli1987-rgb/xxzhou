from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath,Path
import dashscope
import requests
from dashscope import ImageSynthesis
import os
from dotenv import load_dotenv
load_dotenv()

def create_images(prompt:str,images:list,save_dir:str):
    """
    create_images可以工具用户的提示词和参考图片生成新的图片
    
    :param prompt: 用户的提示词
    :type prompt: str
    :param images: 本地图片的访问路径组成的列表
    :type images: list
    :save_dir: 生成图片保存的位置
    :type save_dir: str
    """
    
    dashscope.api_key = os.getenv("QWEN_API_KEY")
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    api_key = os.getenv("QWEN_API_KEY")

    print('----开始生成图片----')
    rsp = ImageSynthesis.call(api_key=api_key,
                            model="wan2.5-i2i-preview",
                              prompt=prompt,
                            images=images,
                            negative_prompt="",
                            n=1,
                            #   size="720*1280",#竖屏 9:16
                            # size="1280*960",#横屏：4:3
                            #   size="1280*720", #横屏：16:9
                            size="768*768",
                            prompt_extend=True,
                            watermark=False,
                            seed=12345)
    print('response: %s' % rsp)
    if rsp.status_code == HTTPStatus.OK:
        # 在当前目录下保存图片
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            # local_path = Path(os.path.abspath(file_name)).resolve()
            local_path = Path(save_dir).joinpath(file_name).resolve()
            # 保存图片
            with open(local_path, 'wb+') as f:
                f.write(requests.get(result.url).content)
            return ToolResponse(
                content=[
                    TextBlock(
                        type="text",
                        text=f"任务完成。图片已保存至：{str(local_path)}",
                    ),
                ]
            )
    else:
        print('sync_call Failed, status_code: %s, code: %s, message: %s' %
            (rsp.status_code, rsp.code, rsp.message))
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"任务失败：{rsp.message}",
                ),
            ]
        )

