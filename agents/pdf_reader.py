from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from llm import XXzhouModel

pdf_reader_agent = ReActAgent(
    name="pdf reader",
    sys_prompt="你可以读取PDF文件内容，提取其中的文本、表格和图片信息，并用语言描述PDF的内容。对于扫描件PDF，你可以识别其中的文字内容。",
    formatter=DashScopeChatFormatter(),
    toolkit=[],
    model=XXzhouModel().get_dashscope_chat_model(model_name="qwen3-vl-plus")
)

# pdf_reader_agent.set_console_output_enabled(False)
