# def coroutine():
#     print("协程启动，等待接收数据……")
#     while True:
#         # yield作为表达式，接收send传递的数据
#         data = yield
#         print(f"协程接到的数据{data}")
#         if data == "quit":
#             print("退出协程")
#             break

# co = coroutine()

# next(co)

# co.send("你好")
# co.send("hello")
# co.send("quit")

######################################

def coroutor(start = 0):
    count = start
    while True:
        new_start = yield count
        if new_start is not None:
            count = new_start
        count += 1

c = coroutor(5)
print(next(c))
print(c.send(10))
print(next(c))
print(c.send(20))