# pip install mcp

from mcp.server import FastMCP

mcp = FastMCP("add",port=8081)

@mcp.tool()
def add(a:int,b:int):
    """计算两个数的加和"""
    return a + b

mcp.run(transport="sse")