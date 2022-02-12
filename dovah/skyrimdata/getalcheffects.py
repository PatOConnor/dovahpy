from bs4 import BeautifulSoup
#from bs4.element import NavigableString
from urllib.request import urlopen
from rich import print

def run():
    effect_list = []
    url = 'https://en.uesp.net/wiki/Skyrim:Alchemy_Effects'
    try:
        page = urlopen(url)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.findAll('table')
    effect_table = tables[-1]
    effect_rows = effect_table.findAll('tr')
    for effect in effect_rows[1::]:
        i = 0
        for cell in effect:
            if i==1: #name of the effect, ID code
                [name, code] = cell.text.split('\n')
                code = code.lstrip('(').rstrip(')')
            elif i==3: #ingredients that provide the effect
                links = cell.findAll('a')
                ingr = []
                for link in links:
                    if link.string and link.string not in ['DG', 'HF', 'DB', 'CC']:
                        ingr.append(link.string)
            elif i==5: #Description of the effect
                desc = cell.string
            elif i==7:
                base_cost = cell.string
                if base_cost == '(?)':
                    base_cost = 0#no data currently
            elif i==9:
                base_mag = cell.string
                if base_mag == '(?)':
                    base_mag = 0#no data currently
            elif i==11:
                base_dur = cell.string
                if base_dur == '(?)':
                    base_dur = 0#no data currently
            elif i==13:
                value = cell.string
            i+=1
        effect_entry = {'NAME':name, 'CODE':code, 'INGR':ingr, 'BASE_COST':float(base_cost), 'BASE_MAG':float(base_mag), 'BASE_DUR':float(base_dur), 'VALUE':float(value)}
        effect_list.append(effect_entry)
    write_to_file(effect_list)

#this block down here keeps getting updated over and over
def write_to_file(data):
    file = open("skyrimalchemy.py", 'a', encoding="utf-8")
    i = 0
    file.write('\neffects = {\n')
    for item in data:  #this writes it in python dictionary syntax
        file.write('\t'+str(i)+':'+str(item)+',\n')
        i += 1
    file.write('\t}')
    file.close()

if __name__=='__main__':
    run()
