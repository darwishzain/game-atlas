import json,os
data = {}
with open('../data/mmorpg/albiononline.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def generate():
    global data
    output = data
    output["resources"] = {}
    enchantment = data['setup']['enchantment']
    setup = data['setup']
    for raw in ["fiber","hide","log","ore","stone"]:
        for tier,name in enumerate(setup[raw]):
            if name != '':
                label = "T"+str(tier+1)+"_"+raw.upper()
                img = f"https://render.albiononline.com/v1/item/{name.replace(' ','%20')}.png?locale=en"
                output["resources"][label] = {
                    "name":name,
                    "tier":tier+1,
                    "enchantment":0,
                    "type":raw,
                    "img":img
                }
                if (tier)>3:
                    for e in range(0,4):
                        label = "T"+str(tier+1)+"_"+raw.upper()+"@"+str(e+1)
                        name_n = ''
                        name_n = enchantment[e] + " " + name
                        img = name_n.replace(" ","%20")
                        img = f"https://render.albiononline.com/v1/item/{name_n.replace(' ','%20')}.png?locale=en"
                        output["resources"][label] = {
                            "name":name_n,
                            "tier":tier+1,
                            "enchantment":e+1,
                            "type":raw,
                            "img":img
                        }
    for refined in ["brick","cloth","leather","metal","plank"]:
        for tier,name in enumerate(setup[refined]):
            if name != '':
                label = "T"+str(tier+1)+"_"+refined.upper()
                img = f"https://render.albiononline.com/v1/item/{name.replace(' ','%20')}.png?locale=en"
                output["resources"][label] = {
                    "name":name,
                    "tier":tier+1,
                    "enchantment":0,
                    "type":refined,
                    "img":img
                }
                if (tier)>3:
                    for e in range(0,4):
                        label = "T"+str(tier+1)+"_"+refined.upper()+"@"+str(e+1)
                        name_n = ''
                        name_n = enchantment[e] + " " + name
                        img = f"https://render.albiononline.com/v1/item/{name_n.replace(' ','%20')}.png?locale=en"
                        output["resources"][label] = {
                            "name":name_n,
                            "tier":tier+1,
                            "enchantment":e+1,
                            "type":refined,
                            "img":img
                        }
    
    with open('../data/mmorpg/albiononline.json','w') as file:
        json.dump(output,file,indent=4)