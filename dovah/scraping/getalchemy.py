from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_alchemy():
    alchemy_table = []

    url = 'https://en.uesp.net/wiki/Skyrim:Ingredients'
    try:
        page = urlopen(url)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.findAll('table', _class='wikitable')
    for t in tables:
        rows = t.findAll('tr')
        counter = 0
        for r in rows:
            if counter == 0:
                pass #ignore first one
            elif counter%2:#every odd row has name and description
                ingr = {}
                cells = r.findAll()
                ingr['NAME'] = cells[1].get_text()
                ingr['LOCATION'] = cells[2].get_text()
                ingr['ID'] = cells.find(_class='idcase').get_text()
            else: #every even has effect data
                cells = r.findAll()
                effects = {}
                for i in range(4):
                    e = cells[i]
                    if e._class == 'EffectNeg':
                        ingr['QUALITY'] = 'BAD'
                    else:
                        ingr['QUALITY'] = 'GOOD'
                    effects[i]['EFFECT'] = e[1].get_text()
                    effects[i]['VALUEMULT'] = 1 #default values
                    effects[i]['MAGMULT'] = 1
                    #look for modifiers
                    mods = e.findAll('span')
                    if len(mods) > 0:#there are span tags that indicate modifiers
                        for m in mods:
                            if m.next_sibling()._title == 'Magnitude':
                                ingr['MAGMULT'] = m.get_text()
                            elif m.next_sibling()._title == 'Value':
                                ingr['VALUEMULT'] = m.get_text()
                ingr['EFFECTS'] = effects
                #get remaining values
                ingr['VALUE'] = cells[4].get_text()
                ingr['WEIGHT'] = cells[5].get_text()
                ingr['RARITY'] = cells[6].get_text()
                ingr['GARDEN'] = cells[7].get_text()
                alchemy_table.append(ingr.copy())
            counter += 1
    print(alchemy_table)

get_alchemy()
