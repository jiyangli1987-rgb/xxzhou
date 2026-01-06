import sqlite3
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse
import base64
import mimetypes
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath,Path
import dashscope
import requests
from dashscope import ImageSynthesis
import os
from dotenv import load_dotenv

def create_images(prompt:str,images:list):
    """
    create_images可以工具用户的提示词和参考图片生成新的图片
    
    :param prompt: 用户的提示词
    :type prompt: str
    :param images: 本地图片的访问路径组成的列表
    :type images: list
    """

    print("!!!!!!!!!!")
    print(images)
    load_dotenv()
    dashscope.api_key = os.getenv("QWEN_API_KEY")


    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'


    api_key = os.getenv("QWEN_API_KEY")

    # --- 输入图片：使用 Base64 编码 ---
    # base64编码格式为 data:{MIME_type};base64,{base64_data}
    def encode_file(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith("image/"):
            raise ValueError("不支持或无法识别的图像格式")
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded_string}"

    """
    图像输入方式说明：
    以下提供了三种图片输入方式，三选一即可

    1. 使用公网URL - 适合已有公开可访问的图片
    2. 使用本地文件 - 适合本地开发测试
    3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
    """

    # # 【方式一】使用公网图片 URL
    # image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
    # image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

    # 【方式二】使用本地文件（支持绝对路径和相对路径）
    # 格式要求：file:// + 文件路径
    # 示例（绝对路径）：
    # image_url_1 = "file://" + "D:/中视频/封面/3.png"     # Linux/macOS
    # image_url_2 = "file://" + "D:/中视频/封面/2.png"  # Windows
    # 示例（相对路径）：
    # image_url_1 = "file://" + "./image_1.png"                 # 以实际路径为准
    # image_url_2 = "file://" + "./image_1.png"                # 以实际路径为准

    # 【方式三】使用Base64编码的图片
    # image_url_1 = encode_file("./image_1.png")               # 以实际路径为准
    # image_url_2 = encode_file("./image_2.png")              # 以实际路径为准

    print('----sync call, please wait a moment----')
    rsp = ImageSynthesis.call(api_key=api_key,
                            model="wan2.5-i2i-preview",
                              prompt=prompt,
                            #   images=[image_url_1, image_url_2],
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
            local_path = Path(os.path.abspath(file_name)).resolve()
            # 保存图片
            with open(local_path, 'wb+') as f:
                f.write(requests.get(result.url).content)
            print("@@@@@@@@@@@@")
            print(local_path)
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

