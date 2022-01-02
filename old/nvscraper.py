from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

'''this program uses beautiful soup to scrape the fallout wiki'''
# TODO: identify dlcs in data

class NVScraper:
    def __init__(self, dm=0,hh=1,lr=2,owb=3,gra=4,cs=5):
        self.item_urls = {
            'ammo':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_ammunition',
            'armor':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_armor_and_clothing',
            'cards':'https://fallout.fandom.com/wiki/Caravan_card',
            'consumables':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_consumables',
            'crafting':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_crafting',
            'notes':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_notes',
            'holotapes':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_holotapes',
            'keys':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_keys',
            'skillbooks':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_skill_books',
            'magazines':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_skill_magazines',
            'snowglobes':'https://fallout.fandom.com/wiki/Snow_globe',
            'weapons':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_weapons',
            'mods':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_weapon_mods',
            'misc':'https://fallout.fandom.com/wiki/Fallout:_New_Vegas_miscellaneous_items'
        }
        self.datatable = []
        self.load_order = {
            'deadmoney':dm,
            'honesthearts':hh,
            'lonesomeroad':lr,
            'oldworldblues':owb,
            'gunrunners':gra,
            'couriersstash':cs,
        }

    def set_loadorder(self, dm,hh,lr,owb,gra,cs):
        self.load_order['deadmoney'] = dm
        self.load_order['honesthearts'] = hh
        self.load_order['lonesomeroad'] = lr
        self.load_order['oldworldblues'] = owb
        self.load_order['gunrunners'] = gra
        self.load_order['couriersstash'] = cs
        return


    def scrape_page(self,url):
        datarow = []
        try:
            page = urlopen(url)
        except:
            print('error opening url')
            return
        soup = BeautifulSoup(page,'html.parser')
        table = soup.find('table')
        tbody = table.find('tbody')
        rows = tbody.findAll('tr')
        for row in rows:
            for cell in row:
                datarow.append(cell.string)
            self.datatable.append(datarow)
        return

    def remove_newlines(string_val):
        regex = '(\\\n)$' #ends with \n
        new_str = re.sub(regex, '', string_val)
        return new_str

    def scrape_ammo(self):
        currentAmmo = ''
        idcode = ''
        datarow = []
        ammo_dict = {
            'ammo':0,
            'type':0,
            'id':'',
            'content':'base'
        }
        bigrow = False
        try:
            page = urlopen(self.item_urls['ammo'])
        except:
            print('error opening url')
            return
        soup = BeautifulSoup(page,'html.parser')
        tables = soup.findAll('table', {"class": "va-table va-table-full"})
        for table in tables:
            tbody = table.find('tbody')
            for row in tbody.findAll('tr'):
                try:
                    left = row.find('td') #first link in lefthand column
                    currentAmmo = left.find('a')['title']  #has a title
                    bigrow = True
                except:
                    bigrow = False
                if currentAmmo == '.30-30 round':
                    continue
                ammo_dict['ammo'] = currentAmmo
                for cell in row.findAll('td'):
                    datarow.append(cell.string)#this grabs the type, weight, value, etc
                for cell in datarow:
                    if cell == None:
                        datarow.pop(datarow.index(cell)) #clear out Nones
                try:
                    if bigrow:
                        ammo_dict['type'] = datarow[1]
                    else:
                        ammo_dict['type'] = datarow[0]
                except:
                    ammo_dict['type'] = ''
                datarow.clear()
                self.datatable.append(ammo_dict.copy())
            self.datatable.pop()#remove row from end of table

        #assigning base IDs
        self.datatable.pop(0)
        ids = soup.findAll('span',{'class':'va-formid'})
        for i in ids:
            try:
                dlchelplink = i.find('a',{'title':'Help:Form IDs'})
                datarow.append(dlchelplink.nextSibling)
            except:
                datarow.append(i.string)#cdatarow coming back for round 2
        for i in self.datatable:
            try:
                i['id'] = datarow[0]
                if len(datarow[0]) == 6:
                    i['content'] = 'dlc'
                datarow.pop(0)
            except:
                pass
        #hardcoding in the one that gets chopped off
        self.datatable.append({
        'ammo':'Ammo Box, Small Energy Cell, bulk',
        'type':'',
        'id':'00166654',
        'content':'fnv'
        })

    def write_to_file(self,filename):
        try:
            f = open('nvdata/'+filename+'.py','w')
        except:
            print('error opening file')
            return

        f.write(filename+' = {\n')
        for i in range(len(self.datatable)):
            vals = str(self.datatable[i].values())
            vals = vals[12:]
            vals = vals[:-1]
            f.write('\t'+str(i)+':'+vals+',\n')
        f.write('\t}')
        f.close()


if __name__=='__main__':
    scraper = NVScraper()
    #scraper.scrape_ammo()
    #scraper.write_to_file('ammo')
    scraper.datatable.clear()
    scraper.scrape_page(scraper.item_urls['armor'])
    for i in scraper.datatable:
        print(i)
