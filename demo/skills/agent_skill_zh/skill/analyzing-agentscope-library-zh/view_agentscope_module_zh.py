# -*- coding: utf-8 -*-
# pylint: skip-file
"""获取 agentscope 库中函数和类的签名。"""
from typing import Literal, Callable

import agentscope
import inspect
from pydantic import BaseModel


def get_class_signature(cls: type) -> str:
    """获取类的签名。

    参数:
        cls (`type`):
            类对象。

    返回:
        str: 类的签名。
    """
    # 获取类名和文档字符串
    class_name = cls.__name__
    class_docstring = cls.__doc__ or ""

    # 构造类字符串
    class_str = f"class {class_name}:\n"
    if class_docstring:
        class_str += f'    """{class_docstring}"""\n'

    # 获取类的方法
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # 跳过不属于此类的方法
        if method.__qualname__.split(".")[0] != class_name:
            continue

        if name.startswith("_") and name not in ["__init__", "__call__"]:
            continue

        # 获取方法的签名
        sig = inspect.signature(method)

        # 构造方法字符串
        method_str = f"    def {name}{sig}:\n"

        # 如果存在，添加方法的文档字符串
        method_docstring = method.__doc__ or ""
        if method_docstring:
            method_str += f'        """{method_docstring}"""\n'

        methods.append(method_str)

    class_str += "\n".join(methods)
    return class_str


def get_function_signature(func: Callable) -> str:
    """获取函数的签名。"""
    sig = inspect.signature(func)
    method_str = f"def {func.__name__}{sig}:\n"

    method_docstring = func.__doc__ or ""
    if method_docstring:
        method_str += f'   """{method_docstring}"""\n'

    return method_str


class FuncOrCls(BaseModel):
    """此类记录模块、签名、文档字符串、引用和类型"""

    module: str
    """函数或类的模块。"""
    signature: str
    """函数或类的签名。"""
    docstring: str
    """函数或类的文档字符串。"""
    reference: str
    """函数或类的源代码引用"""
    type: Literal["function", "class"]
    """函数或类的类型，'function' 或 'class'。"""

    def __init__(
        self,
        module: str,
        signature: str,
        docstring: str,
        reference: str,
        # pylint: disable=redefined-builtin
        type: Literal["function", "class"],
    ) -> None:
        """初始化 FuncOrCls 实例。"""
        super().__init__(
            module=module,
            signature=signature.strip(),
            docstring=docstring.strip(),
            reference=reference,
            type=type,
        )


def _truncate_docstring(docstring: str, max_length: int = 200) -> str:
    """将文档字符串截断为最大长度。

    参数:
        docstring (`str`):
            要截断的文档字符串。
        max_length (`int`, *可选*, 默认为 200):
            文档字符串的最大长度。

    返回:
        `str`:
            截断后的文档字符串。
    """
    if len(docstring) > max_length:
        return docstring[:max_length] + "..."
    return docstring


def get_agentscope_module_signatures() -> list[FuncOrCls]:
    """获取 agentscope 库中函数和类的签名。

    返回:
        `list[FuncOrCls]`:
            表示 agentscope 库中函数和类的 FuncOrCls 实例列表。
    """
    signatures = []
    for module in agentscope.__all__:
        as_module = getattr(agentscope, module)
        path_module = ".".join(["agentscope", module])

        # 函数
        if inspect.isfunction(as_module):
            file = inspect.getfile(as_module)
            source_lines, start_line = inspect.getsourcelines(as_module)
            signatures.append(
                FuncOrCls(
                    module=path_module,
                    signature=get_function_signature(as_module),
                    docstring=_truncate_docstring(as_module.__doc__ or ""),
                    reference=f"{file}: {start_line}-"
                    f"{start_line + len(source_lines)}",
                    type="function",
                ),
            )

        else:
            if not hasattr(as_module, "__all__"):
                continue

            # 具有 __all__ 属性的模块
            for name in as_module.__all__:
                func_or_cls = getattr(as_module, name)
                path_func_or_cls = ".".join([path_module, name])

                if inspect.isclass(func_or_cls):
                    file = inspect.getfile(func_or_cls)
                    source_lines, start_line = inspect.getsourcelines(
                        func_or_cls,
                    )
                    signatures.append(
                        FuncOrCls(
                            module=path_func_or_cls,
                            signature=get_class_signature(func_or_cls),
                            docstring=_truncate_docstring(
                                func_or_cls.__doc__ or "",
                            ),
                            reference=(
                                f"{file}: {start_line}-"
                                f"{start_line + len(source_lines)}"
                            ),
                            type="class",
                        ),
                    )

                elif inspect.isfunction(func_or_cls):
                    file = inspect.getfile(func_or_cls)
                    source_lines, start_line = inspect.getsourcelines(
                        func_or_cls,
                    )
                    signatures.append(
                        FuncOrCls(
                            module=path_func_or_cls,
                            signature=get_function_signature(func_or_cls),
                            docstring=_truncate_docstring(
                                func_or_cls.__doc__ or "",
                            ),
                            reference=(
                                f"{file}: {start_line}-"
                                f"{start_line + len(source_lines)}"
                            ),
                            type="function",
                        ),
                    )

    return signatures


def view_agentscope_library(
    module: str,
) -> str:
    """通过给定的模块名称查看 AgentScope 的 Python 库
    （例如 agentscope），并返回该模块的子模块、类和函数。通过类名，返回该类的文档、方法及其签名。
    通过函数名，返回该函数的文档和签名。如果您对 AgentScope 库没有任何信息，请尝试使用 "agentscope" 查看可用的顶级模块。

    注意，此函数仅提供模块的简要信息。如需更多信息，您应该查看源代码。

    参数:
        module (`str`):
            要查看的模块名称，应为以点分隔的模块路径（例如 "agentscope.models"）。它可以指代模块、类或函数。
    """
    if not module.startswith("agentscope"):
        return (
            f"模块 '{module}' 无效。输入的模块应为 "
            f"'agentscope' 或 agentscope 的子模块 'agentscope.xxx.xxx' "
            f"（以点分隔）。"
        )

    agentscope_top_modules = {}
    for as_module in agentscope.__all__:
        if as_module in ["__version__", "logger"]:
            continue
        agentscope_top_modules[as_module] = getattr(
            agentscope,
            as_module,
        ).__doc__

    # 顶级模块
    if module == "agentscope":
        top_modules_description = (
            [
                "AgentScope 库中的顶级模块：",
            ]
            + [
                f"- agentscope.{k}: {v}"
                for k, v in agentscope_top_modules.items()
            ]
            + [
                "您可以通过使用上述模块名称调用此函数来进一步查看上述模块中的类/函数。",
            ]
        )
        return "\n".join(top_modules_description)

    # 类、函数
    modules = get_agentscope_module_signatures()
    for as_module in modules:
        if as_module.module == module:
            return f"""- '{module}' 的签名：
```python
{as_module.signature}
```

- 源代码引用：{as_module.reference}"""

    # 两级模块
    collected_modules = []
    for as_module in modules:
        if as_module.module.startswith(module):
            collected_modules.append(as_module)

    if len(collected_modules) > 0:
        collected_modules_content = (
            [
                f"'{module}' 模块中的类/函数及其截断的文档字符串：",
            ]
            + [f"- {_.module}: {repr(_.docstring)}" for _ in collected_modules]
            + [
                "文档字符串因上下文限制而被截断。如需详细的签名和方法，请使用上述模块名称调用此函数",
            ]
        )

        return "\n".join(collected_modules_content)

    return (
        f"未找到模块 '{module}'。使用 'agentscope' 查看顶级模块以确保给定的模块有效。"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--module",
        type=str,
        default="agentscope",
        help="要查看的模块名称，例如 'agentscope'",
    )
    args = parser.parse_args()

    res = view_agentscope_library(module=args.module)
    print(res)
