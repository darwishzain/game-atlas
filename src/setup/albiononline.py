import json,os
data = {}
source = ('../../data/mmorpg/albiononline.json' if os.path.exists('../../data/mmorpg/albiononline.json') else '../data/mmorpg/albiononline.json')
with open(source, 'r', encoding='utf-8') as file:
    data = json.load(file)

def image(name):
    name = name.replace("'", '%27')
    return f"https://render.albiononline.com/v1/item/{name.replace(' ','%20')}.png?locale=en"
def labeling(tier,name,enhancement):
    label = "T"+str(tier)+"_"+name.upper().replace(' ','_')
    if enhancement > 0:
        label += "@"+str(enhancement)
    return label
output = data
enhancement = data['setup']['enchantment']
setup = data['setup']
#* Resources
output["resources"] = {}
for type in setup['resources']:
    for tier,name in enumerate(setup['resources'][type]):
        if name != '':
            label = labeling(tier+1,name,0)
            img = image(name)
            output['resources'][label] = {
                "name":name,
                "tier":tier+1,
                "enchantment":0,
                "type":type,
                "img":img
            }
            if tier>=3:
                for e in range(0,4):
                    label = labeling(tier+1,name,e+1)
                    name_n = enhancement[e] + " " + name
                    img = image(name_n)
                    output['resources'][label] = {
                        "name":name_n,
                        "tier":tier+1,
                        "enchantment":e+1,
                        "type":type,
                        "img":img
                    }
#*Tools
output['tools'] = {}
for type in setup['tools']:
    for t in range(1,9):
        name = setup['tier'][t-1]+"'s "+setup['tools'][type]
        label = labeling(t,setup['tools'][type],0)
        img = image(name)
        output['tools'][label] = {
            "name":name,
            "tier":t,
            "type":type,
            "img":img
        }
#* Weapons
output["weapons"] = {}
output["weapons"]["warrior"] = {}
output["weapons"]["hunter"] = {}
output["weapons"]["mage"] = {}
for role in setup['weapons']:
    for type in setup['weapons'][role]:
        for tier,name in enumerate(setup['weapons'][role][type]):
            if name != '':
                if tier <= 2:
                    named = setup['tier'][tier]+"'s "+name
                    label = labeling(tier+1,name,0)
                    img = image(named)
                    output['weapons'][role][label] = {
                            "name":named,
                            "tier":tier+1,
                            "type":role+' weapon',
                            "img":img
                        }
                else:
                    for t in range(3,8):
                        for w in name:
                            for e in range(0,4):
                                named = enhancement[e]+" "+setup['tier'][t]+"'s "+w
                                label = labeling(t+1,w,e+1)
                                img = image(named)
                                output['weapons'][role][label] = {
                                    "name":named,
                                    "tier":t+1,
                                    "enhancement":e+1,
                                    "type":role+' weapon',
                                    "img":img
                                }
    #for tier,name in enumerate(setup['weapons'][role]):
    #    print(str(tier+1)+name)
#* ARMOR
#! Research
#*JOURNAL
output["journals"] = {}
for type in setup["journal"]:
    for laborer in setup["journal"][type]:
        if type == "gathering":
            output["journals"][laborer.upper()+" JOURNAL"] = {
                "laborer":laborer.capitalize()+" Laborer",
                "type":type,
                "yield":setup["journal"][type][laborer][0]
            }
            output["journals"][laborer.upper()+" TROPHY JOURNAL"] = {
                "laborer":laborer.capitalize()+" Laborer",
                "type":"trophy",
                "yield":setup["journal"][type][laborer][1]
            }
        elif type == "crafting":
            output["journals"][laborer.upper()+" CRAFTING JOURNAL"] = {
                "laborer":laborer.capitalize()+" Laborer",
                "type":type,
                "yield":setup["journal"][type][laborer]
            }

        #name = laborer[0]
with open(source, 'w', encoding='utf-8') as outfile:
    json.dump(output, outfile, ensure_ascii=False, indent=4)