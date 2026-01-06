from collections import deque

# 初始化共享队列，所有模块导入的是同一个deque实例
shared_data = deque()