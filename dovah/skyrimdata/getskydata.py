from bs4 import BeautifulSoup
from urllib.request import urlopen

################################
# program uses beautiful soup to access website, get tables, format them into
# usable data and save to file. Redundant now but included inpackage for posterity
################################

def scrape_page(url_string):
    url = url_string
    my_table = []
    my_list = []

    try:
        page = urlopen(url)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div', {"class": "mobile-table"})

    for row in content.findAll('tr'):
        for item in row.children:
            if item != '\n':
                my_list.append(item.string)
        #escape apostraphes (sic?)
        for item in my_list:
            if item:
                if "'" in item:
                    item.replace("'","\\\'")
        my_table.append(tuple(my_list))
        my_list.clear()
    return my_table

#this writes the data to the file of the associated category
def write_to_file(category, data):
    file = open("skyrim"+category+".py", 'w', encoding="utf-8")
    i = 0
    file.write('skyrim_'+category+' = {\n')
    for item in data:  #this writes it in python dictionary syntax
        file.write('\t'+str(i)+':'+str(item)+',\n')
        i += 1
    file.write('\t}')
    file.close()

#returns massive dictionary of all the data of a given category
def scrape_all(category, bound=None):
    main_url = 'http://www.skyrimcommands.com/'+category+'/'
    value_table = list()
    value_table.append(scrape_page(main_url))
    print('added page 1')
    #items list has 88 pages
    #npcs has 28
    #enchantments 10
    #perks, quests, spells, avs, weather, is only 1
    if(bound):
        for i in range(2,bound):#88 is the max
            current_url = main_url+str(i)+'/'
            current_page = scrape_page(current_url)
            if current_page == None:
                pass
            else:
                value_table.append(current_page)
                print('added page '+str(i))
        print('pages added to table')
    #these few lines combine the pages into one list and convert to dictionary
    master_list = []
    for pages in value_table:
        master_list.extend(pages)
    write_to_file(category, master_list)
    print('file written')

def get_all_tables():
    print('items')
    scrape_all('items', 88)
    print('npcs')
    scrape_all('npcs', 28)
    print('enchantments')
    scrape_all('enchantments', 10)
    for c in ['perks', 'quests', 'spells', 'avs', 'weather']:
        print(c)
        scrape_all(c)

def run():
    print('######################################\n',
        '#\t\tSkyrim Data Scraper\n',
        '#\t\tFor use with Command Batcher\n',
        '#\tBy Pat O\'Connor\n',
        '#\tData Courtesy of skyrimcommands.com\n')
    running = True
    while running:
        print('categories are items, perks, npcs, spells, avs, quests, enchantments, weather')
        category = input('enter item type to gather: ')
        category = category.lower()
        if category == 'items':
            scrape_all(category, 88)
        elif category == 'npcs':
            scrape_all(category, 28)
        elif category == 'enchantments':
            scrape_all(category, 10)
        elif category in ('perks', 'quests', 'spells', 'avs', 'weather'):
            scrape_all(category)
        elif category == 'all':
            print('items')
            scrape_all('items', 88)
            print('npcs')
            scrape_all('npcs', 28)
            print('enchantments')
            scrape_all('enchantments', 10)
            for c in ['perks', 'quests', 'spells', 'avs', 'weather']:
                print(c)
                scrape_all(c)
            running = False
        elif category == 'quit':
            running = False



if __name__=="__main__":
    run()
