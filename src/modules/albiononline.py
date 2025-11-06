import json,os
data = {}
with open('../data/mmorpg/albiononline.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def generate():
    global data
    output = data
    enchantment = data['setup']['enchantment']
    setup = data['setup']
    #* Resources
    output["resources"] = {}
    for resources in ["fiber","hide","log","ore","stone","brick","cloth","leather","metal","plank"]:
        for tier,name in enumerate(setup['resources'][resources]):
            if name != '':
                label = "T"+str(tier+1)+"_"+resources.upper()
                img = f"https://render.albiononline.com/v1/item/{name.replace(' ','%20')}.png?locale=en"
                output["resources"][label] = {
                    "name":name,
                    "tier":tier+1,
                    "enchantment":0,
                    "type":resources,
                    "img":img
                }
                if (tier)>=3:
                    for e in range(0,4):
                        label = "T"+str(tier+1)+"_"+resources.upper()+"@"+str(e+1)
                        name_n = ''
                        name_n = enchantment[e] + " " + name
                        img = name_n.replace(" ","%20")
                        img = f"https://render.albiononline.com/v1/item/{name_n.replace(' ','%20')}.png?locale=en"
                        output["resources"][label] = {
                            "name":name_n,
                            "tier":tier+1,
                            "enchantment":e+1,
                            "type":resources,
                            "img":img
                        }
    #* Tools
    output['tools'] = {}
    for tool in ["fiber","hide","log","ore","stone"]:
        for t in range(1,9):
            name = setup['tier'][t-1]+"'s "+setup['tools'][tool]
            label = "T"+str(t)+"_"+setup['tools'][tool].upper().replace(' ','_')
            img = name.replace("'", '%27')
            img = f"https://render.albiononline.com/v1/item/{img.replace(' ','%20')}.png?locale=en"
            output['tools'][label] = {
                "name":name,
                "tier":t,
                "type":tool,
                "img":img
            }
    #* Weapons
    output["weapons"] = {}
    output["weapons"]["warrior"] = {}
    output["weapons"]["hunter"] = {}
    output["weapons"]["mage"] = {}
    for type in ["warrior","hunter","mage"]:
        for weapons in list(setup['weapons'][type].keys()):
            for tier,weapon in enumerate(setup['weapons'][type][weapons]):
                if weapon != '':
                    if tier <= 2:
                        name = setup['tier'][tier]+"'s "+weapon
                        label = "T"+str(tier+1)+"_"+weapon.upper()
                        img = name.replace("'", '%27')
                        img = f"https://render.albiononline.com/v1/item/{img.replace(' ','%20')}.png?locale=en"
                        output['weapons'][type][label] = {
                                "name":name,
                                "tier":tier+1,
                                "type":type+' weapon',
                                "img":img
                            }
                    else:
                        for t in range(3,8):
                            for w in weapon:
                                name = setup['tier'][t]+"'s "+w
                                label = "T"+str(t+1)+"_"+w.upper().replace(" ","_")
                                img = name.replace("'", '%27')
                                img = f"https://render.albiononline.com/v1/item/{img.replace(' ','%20')}.png?locale=en"
                                output['weapons'][type][label] = {
                                    "name":name,
                                    "tier":t+1,
                                    "type":type+' weapon',
                                    "img":img
                                }
    print("albiononline data updated")
    with open('../data/mmorpg/albiononline.json','w') as file:
        json.dump(output,file,indent=4)