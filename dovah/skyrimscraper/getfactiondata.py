from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen
import os
from rich import print
from .writetofile import write_to_file

def run(is_test=False):
    url_base = 'https://en.uesp.net/wiki/Skyrim:Factions_'
    page_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                    'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W']
    factions = []
    for page in page_letters:
        factions.extend(scrape_page(url_base+page))
    write_to_file('factions', factions, is_test)



def scrape_page(url_string):
    factions = []

    try:
        page = urlopen(url_string)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div',  {'id':'mw-content-text'})
    
    #goes through the children of the content tag
    #skipping the first and second (table of contents and links)
    i = 0
    new_faction = None
    for tag in content:
        #skipping first three divs
        if i < 3:
            i += 1
            continue
        if tag.name == 'h2':
            #this one always comes first, so data gets added to the main list at this step
            if new_faction:
                factions.append(new_faction.copy())
            group_title = None
            new_faction = dict()
            new_faction['NAME'] = tag.text
            new_faction['NAME'] = new_faction['NAME'].replace('[edit]','')
        if tag.name == 'h3':
            # this happens when a group of factions are listed together
            # the move is to set the greater title as the details and 
            # store the smaller title as the name

            #its the first subgroup, so its time to set 
            if not group_title:
                group_title = new_faction['NAME']
                new_faction['NAME'] = tag.text
            #its a subsequent subgroup, so make a new dictionary to hold the new data
            else:
                factions.append(new_faction.copy())
                new_faction = dict()
                new_faction['NAME'] = tag.text
                new_faction['NAME'] = new_faction['NAME'].replace('[edit]','')
            new_faction['DETAILS'] = group_title
        if tag.name == 'p':
            #sometimes but not always there's a blurb of details
            new_faction['DETAILS'] = tag.text
        if tag.name == 'div':
            #each entry is comprised of 2 or 3 tables
            tables = tag.find_all('table', {'class':'wikitable'})
            for table in tables:
                firstrow = table.find('tr').text.lower().strip()
                if firstrow == "information":
                    new_faction['INFO'] = dict()
                    rows = table.find_all('tr')
                    rank_description = '' #a prefix that gets set to "rank " if the 
                                          #info table lists different faction ranks
                    for row in rows:
                        if len(row) == 3: #it is rank or ranks
                            if row.text.lower().strip() != 'information':
                                rank_description = "rank "
                        else: #key-value pair
                            row_title = rank_description+row.contents[1].text
                            row_title = row_title.replace('\xa0',' ')
                            row_content = row.contents[3].text
                            row_content = row_content.replace('\xa0',' ')#get rid of this
                            new_faction['INFO'][row_title] = row_content

                elif firstrow == "combat reactions":
                    new_faction['REACTIONS'] = dict()
                    rows = table.find_all('tr')
                    for row in rows:
                        #first row is row of headers that is ignored
                        cells = row.find_all('td')
                        if not cells: continue
                        related_faction = row.contents[1].text
                        combat_reaction = row.contents[3].text
                        new_faction['REACTIONS'][related_faction] = combat_reaction


                elif firstrow == "members":
                    new_faction['MEMBERS'] = list()
                    members = table.find('td')
                    for member in members.contents:
                        if type(member) == NavigableString: continue
                        if member.text.find(',') == -1:
                            new_faction['MEMBERS'].append(member.text)
                        else:
                            split_text = member.text.split(',')
                            for s in split_text:
                                if s.strip(): #prevent it from adding empty strings and whitespace
                                    new_faction['MEMBERS'].append(s)

                elif firstrow == "potential members":
                    new_faction['POTENTIAL'] = list()
                    members = table.find('td')
                    for member in members.contents:
                        if type(member) == NavigableString: continue
                        if member.text.find(',') == -1:
                            new_faction['POTENTIAL'].append(member.text)
                        else:
                            split_text = member.text.split(',')
                            for s in split_text:
                                if s.strip():
                                    new_faction['POTENTIAL'].append(s)

                else:
                    print(firstrow, type(firstrow), firstrow=="information")
                    print('unexpected table title at'+url_string)
    return factions

if __name__ == '__main__':
    run()
