# python langlchain

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.agent_toolkits import FileManagementToolkit

load_dotenv()

model = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

@tool
def check_doc(doc_content: str) -> str:
    """
    接收一篇文案内容，对其进行自媒体文案质量评分（0-100分），
    并提供具体的修改建议。
    
    Args:
        doc_content: 待检查的自媒体文案内容。
        
    Returns:
        一个包含评分和修改建议的结构化字符串，格式为：
        "SCORE: [分数]\nSUGGESTIONS: [修改建议]"
    """
    prompt_template = f"""
    请作为一名资深的自媒体文案编辑，对以下文案进行专业评估：
    
    文案内容：
    ---
    {doc_content}
    ---
    
    评估要求：
    1. **评分**：根据标题吸引力、内容结构、可读性、信息价值和自媒体传播潜力等方面，给出0到100分的总分。
    2. **修改建议**：如果分数低于90分，请提供具体的、可操作的修改建议，用于提升文案质量。如果没有建议，则回复“无”。
    3. **格式化输出**：请严格按照以下格式输出结果，不要包含任何额外的说明或寒暄：
    
    SCORE: [分数]
    SUGGESTIONS: [修改建议或“无”]
    
    示例：
    SCORE: 55
    SUGGESTIONS: 标题不够吸引人，可以改成提问式；第一段缺乏钩子，需要增加一个痛点描述。
    """
    
    # 调用模型进行评估
    try:
        response = model.invoke(prompt_template)
        # 返回模型的纯文本响应
        print("#####评价######")
        print(response.content)
        return response.content
    except Exception as e:
        # 错误处理，防止工具调用失败导致Agent崩溃
        return f"评估工具调用失败，错误信息：{e}"

agent = create_agent(
    model=model,
    tools=[check_doc], # 确保这里使用了新的 check_doc
    checkpointer=InMemorySaver(),
    system_prompt="""
你是一位专业的自媒体文案生成与优化专家。
**你的核心能力是直接生成文案内容。**

你的工作流程如下：
1. **生成初稿（无工具）**：首先，你**必须**直接根据用户的请求，利用你的知识和创造力生成一篇自媒体文案的初稿。
2. **评估（使用工具）**：然后，使用`check_doc`工具对你生成的文案进行质量评估。
3. **优化循环**：
    * 如果`check_doc`返回的分数低于60分，你必须根据`SUGGESTIONS`的内容对文案进行优化，并再次使用`check_doc`工具检查。
    * 整个过程最多优化三次。
4. **输出结果**：输出最终文案和得分。如果优化三次仍未达到60分，则输出最后一次的文案和分数。
"""
)

config = {
    "configurable":{
        "thread_id":"1"
    }
}

while True:
    prompt = input("用户：")
    response = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":prompt
            }
        ]
    },config);
    print("AI:" + response["messages"][-1].content)
    print("#"*60)