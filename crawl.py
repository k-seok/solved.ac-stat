import requests
from bs4 import BeautifulSoup as BS
import json
import threading


def getData(tier, p):
    val = requests.get(f'https://api.solved.ac/problem_level.php?id={p.text}').text
    d = json.loads(val)
    tier[d['level']] = tier.get(d['level'], 0) + 1

user = input('user: ')
res = requests.get(f'https://www.acmicpc.net/user/{user}').text

soup = BS(res, 'lxml')

problems = soup.select('body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div:nth-child(3) > div.col-md-9 > div:nth-child(1) > div.panel-body > span')[::2]

tier = {}

for p in problems:
    t = threading.Thread(target=getData, args=[tier, p])
    t.start()

header = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']

for thread in threading.enumerate():
        if thread.daemon:
            continue
        try:
            thread.join()
        except RuntimeError as err:
            if 'cannot join current thread' in err.args[0]:
                # catchs main thread
                continue
            else:
                raise

print('Unranked', tier.get(0, 0))
for i in range(1, 30, 5):
    print(header[(i-1)//5], sum([tier.get(j, 0) for j in range(i, i+5)]))
print('Total', sum(tier.values()))


