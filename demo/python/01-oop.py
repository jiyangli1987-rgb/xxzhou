class Cat:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    # 位置参数和关键字参数
    def __call__(self, *args, **kwds):
        if args:
            print(args)
        if kwds:
            print(kwds)

    def sayHi(self):
        print(f"我今年{self.age}岁了")

cat = Cat(
    name="喵喵",
    age=2
)

cat.sayHi()

cat(1,2,3,4,5,a=1,b=2)



