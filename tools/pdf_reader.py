import fitz  # PyMuPDF
import base64
import os
from agentscope.tool import ToolResponse
from agentscope.message import (
    Msg,
    TextBlock,
    ImageBlock,
    Base64Source
)
from agents.pdf_reader import pdf_reader_agent
import asyncio


async def pdf_reader(prompt: str, pdf_path: str):
    """
    根据用户的提示词，读取和分析PDF文件内容
    :param prompt: 用户的提示词
    :param pdf_path: PDF文件的本地路径
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(pdf_path):
            return ToolResponse(
                content=[TextBlock(type="text", text=f"错误：找不到PDF文件 {pdf_path}")]
            )

        # 检查文件扩展名
        if not pdf_path.lower().endswith('.pdf'):
            return ToolResponse(
                content=[TextBlock(type="text", text=f"错误：文件 {pdf_path} 不是PDF格式")]
            )

        # 提取PDF内容
        pdf_content = extract_pdf_content(pdf_path)

        # 构建消息内容
        message_content = [
            TextBlock(
                type="text",
                text=f"{prompt}\n\nPDF文件：{os.path.basename(pdf_path)}\n\n{pdf_content['text']}"
            )
        ]

        # 如果有图片，也添加到消息中（可选，最多处理前3张图片）
        for i, img_data in enumerate(pdf_content['images'][:3]):
            try:
                message_content.append(
                    ImageBlock(
                        type="image",
                        source=Base64Source(
                            type="base64",
                            data=img_data['data']
                        )
                    )
                )
            except Exception as e:
                print(f"处理第{i+1}张图片时出错：{e}")
                continue

        msg = Msg(
            name="user",
            role="user",
            content=message_content
        )

        res = await pdf_reader_agent(msg)
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=res.content[0]["text"]
                )
            ]
        )

    except Exception as e:
        return ToolResponse(
            content=[TextBlock(type="text", text=f"PDF读取失败：{str(e)}")]
        )


def extract_pdf_content(pdf_path: str) -> dict:
    """提取PDF中的文本和图片"""
    doc = fitz.open(pdf_path)
    content = {"text": "", "images": []}

    try:
        for page_num in range(min(len(doc), 50)):  # 限制最多处理50页
            page = doc.load_page(page_num)

            # 提取文本
            page_text = page.get_text()
            if page_text.strip():  # 只添加非空页面
                content["text"] += f"\n--- 第{page_num+1}页 ---\n"
                content["text"] += page_text

            # 提取图片
            images = page.get_images(full=True)
            for img_index, img in enumerate(images[:5]):  # 每页最多提取5张图片
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    # 转换为base64
                    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
                    content["images"].append({
                        "page": page_num + 1,
                        "data": img_base64,
                        "format": base_image["ext"]
                    })
                except Exception as e:
                    print(f"提取第{page_num+1}页第{img_index+1}张图片时出错：{e}")
                    continue

    finally:
        doc.close()

    return content
