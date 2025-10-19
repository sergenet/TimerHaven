import os
os.makedirs('output', exist_ok=True)
with open('output/test.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, TimerHaven!')
print('Test file created in output/')