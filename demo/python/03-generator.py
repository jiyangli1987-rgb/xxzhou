# yield的作用是暂停函数执行并返回中间结果。

"""
生成器是一种可迭代的对象（Iterable）,但它不会一次性生成所有元素并存储在内存中，而是在每次迭代时（比如 next() 调用或 for 循环）才 “按需生成” 一个元素，生成后暂停，等待下一次调用。

有yield的函数叫做生成器函数
"""

def test_generator():
    yield 1
    yield 2
    yield 3

gen = test_generator()

print(type(gen))

# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen)) #报错