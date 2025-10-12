
import json,os
data = {}
def init():
    game = os.listdir('../data/mmorpg/')
    for f in game:
        if f.endswith('.json'):
            with open(f'../data/mmorpg/{f}', 'r', encoding='utf-8') as file:
                data[f[:-5]] = json.load(file)
    #print(data['albiononline']['resources']['raw']['stone']['T2'])

