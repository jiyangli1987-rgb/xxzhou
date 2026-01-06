# AgentScope 中的代理技能

[Agent Skill](https://claude.com/blog/skills) 是 Anthropic 提出的一种方法，用于改善代理在特定任务上的能力。

在这个示例中，我们演示了如何通过 `toolkit.register_agent_skill` API 将 Agent Skills 集成到 AgentScope 的 ReAct 代理中。

具体来说，我们在 `skill` 目录中准备了一个演示技能，帮助代理学习 AgentScope 框架本身。在 `main.py` 中，我们将这个技能注册到代理的工具包中，并让它回答关于 AgentScope 的问题。

## 快速开始

安装最新版本的 AgentScope 来运行此示例：

```bash
pip install agentscope --upgrade
```

然后使用以下命令运行示例：

```bash
python main.py
```

> 注意：
> - 此示例使用 DashScope 聊天模型构建。如果您想更改此示例中使用的模型，请不要忘记同时更改格式化器！内置模型和格式化器之间的对应关系在[我们的教程](https://doc.agentscope.io/tutorial/task_prompt.html#id1)中列出
> - 对于本地模型，请确保模型服务（如 Ollama）在启动代理之前正在运行。
