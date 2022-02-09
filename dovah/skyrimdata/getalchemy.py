from bs4 import BeautifulSoup
from urllib.request import urlopen

#todo: item codes for dlc items


class Effect:
    def __init__(self, effect, magnitudemult=1, durationmult=1, valuemult=1):
        self.effect = effect
        self.magnitudemult = magnitudemult
        self.durationmult = durationmult
        self.valuemult = valuemult

def get_effect_data(effect_cell):
    if len(effect_cell) == 3:#normal cell
        return Effect(effect_cell.text)
    else:
        magnitudemult = 1
        durationmult = 1
        valuemult = 1
        effect_counter = 0
        for elem in effect_cell:
            if effect_counter < 2:
                pass
            elif effect_counter == 2:
                name = elem.text
            else: #check if the cell is one that contains a picture

                #the issue im working on is getting the multipliers for the data

                if effect_counter in [4,8,12]:
                    if elem.string:
                        effect_mult = float(elem.string)
                    else:
                        #this case is for when the x is colored and the
                        #tags are structured differently
                        print(elem)

                if effect_counter in [6,10,14]:
                    if elem['title'] == 'Magnitude':
                        magnitudemult = effect_mult
                    elif elem['title'] == 'Duration':
                        durationmult = effect_mult
                    elif elem['title'] == 'Value':
                        valuemult = effect_mult
            effect_counter += 1
        #print(name, magnitudemult, durationmult, valuemult)
        return Effect(name, magnitudemult, durationmult, valuemult)



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
        for i in range(len(effectcells)):
            new_ingredient['EFFECTS'] = []
            if 0 <= i <= 3: #effects
                new_ingredient['EFFECTS'].append(get_effect_data(effectcells[i]))
            elif i==4:#value
                new_ingredient['VALUE'] = int(effectcells[i].text)
            elif i==5:#weight
                new_ingredient['WEIGHT'] = float(effectcells[i].text)
            elif i==6:#rarity
                new_ingredient['RARITY'] = effectcells[i].text
            elif i==7:#cropyield
                new_ingredient['CROPYIELD'] = effectcells[i].text
        ingredients_list.append(new_ingredient.copy())
    print(ingredients_list[0])
    return ingredients_list

def run():
    alchemy_table = []
    url = 'https://en.uesp.net/wiki/Skyrim:Ingredients'
    try:
        page = urlopen(url)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.findAll('table')
    for t in tables:
        alchemy_table.extend(get_table(t))
        input()





if __name__=='__main__':
    run()
