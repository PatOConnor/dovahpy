from bs4 import BeautifulSoup
from urllib.request import urlopen
from .writetofile import write_to_file
from rich.panel import Panel
from rich import print
import os

################################
# program uses beautiful soup to access website, get tables, format them into
# usable data and save to file. Redundant now but included inpackage for posterity
################################
is_test = False
def run(category=None, testing=False):
    while(True):
        if category == 'items':
            scrape_all(category, 88)#second parameter is how many pages of data to scrape
            break
        elif category == 'enchantments':
            scrape_all(category, 10)
            break
        elif category in ('perks', 'quests', 'spells', 'avs', 'weather'):
            scrape_all(category)
            break
        elif category == 'all':
            get_all_tables()
            break
        else:
            category = main_menu()

def main_menu():
    print(Panel( '\t\tSkyrim Data Scraper\n\t\tFor use with Command Batcher\n\tBy Roshi\'s Pizza\n\tData sourced from skyrimcommands.com\n'))
    print(Panel('categories are items, perks, spells, avs, quests, enchantments, weather, all'))
    return input('enter item type to gather: ').lower().strip()

def get_all_tables():
    print('items')
    scrape_all('items', 88)
    print('enchantments')
    scrape_all('enchantments', 10)
    for c in ['perks', 'quests', 'spells', 'avs', 'weather']:
        print(c)
        scrape_all(c)

#returns massive dictionary of all the data of a given category
def scrape_all(category, bound=None):
    main_url = 'http://www.skyrimcommands.com/'+category+'/'
    value_table_list = list()
    value_table_list.append(scrape_page(main_url))
    print('added page 1')

    #take the first row and make values for keys
    dict_keys = value_table_list[0].pop(0)
    dict_keys = list(dict_keys)
    dict_keys[0] = 'NAME'
    dict_keys = [x.strip().upper().replace(' ','_') for x in dict_keys] 

    if(bound):
        #bounds: items list has 88 pages, npcs has 28
        #        enchantments has 10, the rest have 1
        for i in range(2,bound):#88 is the max
            current_url = main_url+str(i)+'/'
            current_page = scrape_page(current_url)
            if current_page != None:
                value_table_list.append(current_page)
                print('added page '+str(i))
        print('pages added to table')
   
    #these few lines combine the separate pages into one long page
    master_list = []
    for page in value_table_list:
        master_list.extend(page)
    
    final_list_of_dicts = []
    for row in master_list:
        new_entry = dict()
        for k,cell in zip(dict_keys, row):
            new_entry[k] = cell
        final_list_of_dicts.append(new_entry)

    write_to_file(category, master_list, is_test)
    print('file written')


def scrape_page(url_string):
    content_table = []
    content_row = []
    try:
        page = urlopen(url_string)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div', {"class": "mobile-table"})




    for row in content.findAll('tr')[1:]:
        
        row_content = dict()
        row_content['NAME'] = row.contents[1].text
        code = row.contents[3].text
        #DLC/creation club codes
        if len(code) > 8: 
            code = code.split()[-1]
            if len(code) == 5: code = 'xxx'+code
            if len(code) == 6: code = 'xx'+code
        row_content['CODE'] = code
        for item in row.contents[4:]:
            if item != '\n': content_row.append(item.string)
        #escape apostraphes (sic?)
        for item in content_row:
            if item and "'" in item:
                item.replace("'","\\\'")
        
        
        content_table.append(row_content.copy())





    return content_table





if __name__=="__main__":
    run()
