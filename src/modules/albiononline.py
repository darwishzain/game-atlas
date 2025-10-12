import json,os
data = {}
def init():
    global data
    with open('../data/mmorpg/albiononline.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

def ui():
    print('ui function in honorofkings module')