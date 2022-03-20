import random

a = random.randint(1,6)

pic = {
    1:"g",
    2:"gg",
    3:"ggg",
    4:"gggg",
    5:"ggggg",
    6:"gggggg",
}

if a in pic:
    print(pic[a])
