from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen



def run():
    alchemy_list = []
    url = 'https://en.uesp.net/wiki/Skyrim:Alchemy_Effects'
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
