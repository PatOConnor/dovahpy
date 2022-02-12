from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen

def excess_strip(s):
    s2 = ''
    for c in s:
        if c.isnumeric() or c=='.':
            s2 += c
    return s2

def get_effect_data(effect_cell):
    new_effect = {}
    if len(effect_cell) == 3:#normal cell
        name = effect_cell.text
        name = name[1::]
        new_effect['NAME'] = name
        new_effect['MAGNITUDEMULT'] = 1
        new_effect['DURATIONMULT'] = 1
        new_effect['VALUEMULT'] = 1
    else:
        magnitudemult = 1
        durationmult = 1
        valuemult = 1
        effect_counter = 0
        for elem in effect_cell:
            if effect_counter == 0:
                effect_counter += 1
                continue#ignore the icon
            if not isinstance(elem, NavigableString):
                #print(effect_counter, elem,'\n', elem.text)
                if effect_counter == 2:
                    name = elem.text
                elif elem.has_attr('style'):#multiplier values
                    if elem.string != None:
                        current_multiplier = elem.string
                        current_multiplier = excess_strip(current_multiplier)
                    else:
                        #some cells have <span><a></a></span> instead of side-by-side
                        current_multiplier = elem.find('b').string
                        current_multiplier = excess_strip(current_multiplier)
                        linkelem = elem.find('a')
                        if linkelem['title'] == 'Magnitude':
                            magnitudemult = float(current_multiplier)
                        elif linkelem['title'] == 'Duration':
                            durationmult = float(current_multiplier)
                        elif linkelem['title'] == 'Value':
                            valuemult = float(current_multiplier)
                elif elem['title'] == 'Magnitude':
                    magnitudemult = float(current_multiplier)
                elif elem['title'] == 'Duration':
                    durationmult = float(current_multiplier)
                elif elem['title'] == 'Value':
                    valuemult = float(current_multiplier)
            effect_counter += 1
        new_effect = {}
        new_effect['NAME'] = name
        new_effect['MAGNITUDEMULT'] = magnitudemult
        new_effect['DURATIONMULT'] = durationmult
        new_effect['VALUEMULT'] = valuemult
    return new_effect.copy()

def clean_xx_codes(alchemy_list):
    for entry in alchemy_list:
        name = entry['NAME']
        try:
            code = entry['CODE']
        except:
            code = ''#that egg with no code
        if code.find('xxx') >= 0:
            continue#creation club stuff
        elif code.find('xx') >= 0:
            if 'DG' in name:
                code = code.replace('xx','02')
            elif 'HF' in name:
                code = code.replace('xx','03')
            elif 'DB' in name:
                code = code.replace('xx','04')
    return alchemy_list


def get_table(table):
    ingredients_list = []
    tr_tags = table.findAll('tr')
    #the entries are split between two rows, so they're getting pushed together
    #with the column indicator row being left behind
    rows = [[tr_tags[x], tr_tags[x+1]] for x in range(1, len(tr_tags)-1, 2)]

    for row in rows:
        new_ingredient = {}
        inforow = row[0]
        effectrow = row[1]
        infocells = inforow.findAll('td')
        for i in range(len(infocells)):
            if i == 1:
                ingr_info = infocells[i].text
                #print(ingr_info)
                ingr_info = ingr_info.split('\n') #ingr_info is [name, idcode]
                new_ingredient['NAME'] = ingr_info[0]
                if len(ingr_info) > 1:#some don't have codes on the website
                    new_ingredient['CODE'] = ingr_info[1]
            elif i == 2:
                ingr_desc = infocells[i].text
                new_ingredient['DESC'] = ingr_desc
        effectcells = effectrow.findAll('td')
        ingr_effects = []
        for i in range(len(effectcells)):
            if 0 <= i <= 3: #effects
                new_effect = get_effect_data(effectcells[i])
                ingr_effects.append(new_effect)
            elif i==4:#value
                new_ingredient['EFFECTS'] = ingr_effects
                new_ingredient['VALUE'] = int(effectcells[i].text)
            elif i==5:#weight
                new_ingredient['WEIGHT'] = float(effectcells[i].text)
            elif i==6:#rarity
                new_ingredient['RARITY'] = effectcells[i].text
            elif i==7:#cropyield
                new_ingredient['CROPYIELD'] = effectcells[i].text
        ingredients_list.append(new_ingredient.copy())
    return ingredients_list

def run():
    alchemy_list = []
    url = 'https://en.uesp.net/wiki/Skyrim:Ingredients'
    try:
        page = urlopen(url)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.findAll('table')
    for t in tables:
        alchemy_list.extend(get_table(t))

    alchemy_list = clean_xx_codes(alchemy_list)
    #print(alchemy_list)
    write_to_file(alchemy_list)

#this is the same one i wrote for skydata
def write_to_file(data):
    file = open("skyrimalchemy.py", 'w', encoding="utf-8")
    i = 0
    file.write('skyrim_alchemy = {\n')
    for item in data:  #this writes it in python dictionary syntax
        file.write('\t'+str(i)+':'+str(item)+',\n')
        i += 1
    file.write('\t}')
    file.close()

if __name__=='__main__':
    run()
