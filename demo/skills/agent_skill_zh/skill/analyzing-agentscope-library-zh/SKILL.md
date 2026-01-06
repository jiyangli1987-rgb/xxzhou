---
name: 分析 AgentScope 库
description: 此技能提供了一种从 AgentScope 库中检索信息以进行分析和决策的方法。
---

# 分析 AgentScope 库

## 概述

本指南涵盖了从 AgentScope 库检索和回答问题的重要操作。
如果您需要回答关于 AgentScope 库的问题，或查找特定信息、函数/类、示例或指导，此技能将帮助您实现这一目标。

## 快速开始

该技能提供以下关键脚本：

- 在 AgentScope 教程中搜索指导。
- 搜索 AgentScope 提供的官方示例和推荐实现。
- 通过给定模块名称（例如 agentscope）快速查看 AgentScope 的 Python 库界面，并返回该模块的子模块、类和函数。

当被问到 AgentScope 相关问题时，您可以按照以下步骤查找相关信息：

首先根据用户的问题决定使用三个脚本中的哪一个。
- 如果用户询问"如何使用"类型的问题，使用"搜索指导"脚本查找相关教程
- 如果用户询问"如何实现/构建"类型的问题，首先搜索相关示例。如果未找到，则考虑需要哪些函数并在指南/教程中搜索
- 如果用户询问"如何初始化"类型的问题，首先搜索相关教程。如果未找到，则考虑在库中搜索相应的模块、类或函数。

### 搜索示例

首先请求用户允许克隆 agentscope GitHub 仓库（如果尚未这样做）：

```bash
git clone -b main https://github.com/agentscope-ai/agentscope
```

在这个仓库中，`examples` 文件夹包含各种示例，演示如何使用 AgentScope 库的不同功能。
它们按不同功能组织在树状结构中。您应该使用 `ls` 或 `cat` 等 shell 命令导航和查看示例。避免使用 `find` 命令搜索示例，因为示例文件的名称可能与正在搜索的功能没有直接关系。

### 搜索指导

同样，首先确保您已克隆 agentscope GitHub 仓库。

AgentScope 教程的源代码位于 agentscope GitHub 仓库的 `docs/tutorials` 文件夹中。它按不同部分组织。要搜索指导，请转到 `docs/tutorials` 文件夹并使用 `ls` 或 `cat` 等 shell 命令查看教程文件。

### 搜索目标模块

首先，确保您的环境中已安装 agentscope 库：

```bash
pip list | grep agentscope
```

如果未安装，请请求用户允许通过以下命令安装：

```bash
pip install agentscope
```

然后，运行以下脚本来搜索特定模块、类或函数。建议从 `agentscope` 作为根模块名称开始，然后指定要搜索的子模块名称。

```bash
python view_agentscope_module_zh.py --module agentscope
```

关于详细用法，请参考位于此 SKILL.md 文件同一文件夹中的 `./view_agentscope_module_zh.py` 脚本。
