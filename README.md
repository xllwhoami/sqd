dict-like sqlite wrapper

`pip install sqd`


```python
from sqd import SQD
from random import randint

config = SQD('config.db')
config.create_section('bot')


del config.bot

config.create_section('bot')

bot = config.bot

bot['token'] = '123456:ABCDEFG'

print(bot['token']) # 123456:ABCDEFG

bot['token'] = '1234:ABCDE'

print(bot['token']) # 1234:ABCDE

del bot['token']

print(bot['token']) # None


for _ in range(10):
    x = 'x'+str(randint(1, 10))
    y = 'y'+str(randint(1, 10))
    
    bot[x] = y
    


print(list(bot.items())) # [('x7', 'y8'), ('x4', 'y5'), ('x6', 'y2'), ('x10', 'y8'), ('x1', 'y7'), ('x3', 'y8'), ('x8', 'y8')]
print(list(bot.values())) # ['y8', 'y5', 'y2', 'y8', 'y7', 'y8', 'y8']
print(list(bot.keys())) # ['x1', 'x10', 'x3', 'x4', 'x6', 'x7', 'x8']
print(len(bot)) # 7


bot.update(x11 = 'y11', x12 = 'y12')
print(bot['x11'], bot['x12']) # y11 y12


for x in bot:
    print(x)
    
# x1
# x10
# x3
# x4
# x6
# x7
# x8
# x11
# x12
```
