
    # 1. 定义图纸 (Class)
class Cat:
    
    # 2. 出厂设置 (__init__)
    # 每次你根据图纸造猫的时候，这个函数会自动运行
    def __init__(self, name, color):
        self.name = name    # 把传入的名字，贴到这只猫身上
        self.color = color  # 把传入的颜色，涂到这只猫身上
        self.mood = "开心"  # 默认出厂心情都是开心

    # 3. 行为 (Method)
    # 猫能做的动作
    def meow(self):
        # self.name 指的是“我自己的名字”
        print(f"{self.name} ({self.color}) 喵喵叫！")

    def get_angry(self):
        self.mood = "生气"
        print(f"{self.name} 现在很 {self.mood}！")
