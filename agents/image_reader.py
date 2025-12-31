from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from llm import XXzhouModel

image_reader_agent = ReActAgent(
    name="image reader",
    sys_prompt="你可以识别图片上的内容，并用语言描述图片内容。",
    formatter=DashScopeChatFormatter(),
    toolkit=[],
    model=XXzhouModel().get_dashscope_chat_model(model_name="qwen3-vl-plus")
)

# image_reader_agent.set_console_output_enabled(False)


