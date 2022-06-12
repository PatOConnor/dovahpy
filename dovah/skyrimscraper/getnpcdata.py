from email.mime import base
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen
import os
from rich import print
from .writetofile import write_to_file

def run(is_test=True):
    url = 'https://elderscrolls.fandom.com/wiki/Console_Commands_(Skyrim)/Characters'
    npcs = scrape_page(url)
    # print(npcs)
    write_to_file('npcs', npcs, is_test)

def scrape_page(url_string):
    npcs = []
    try:
        page = urlopen(url_string)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows[3:-7]:#remove infobars at top and bottom
        npc_name = row.contents[1].text
        npc_name = npc_name.replace('\n', '')
        ref_id = row.contents[3].text
        ref_id = ref_id.replace('\n', '')
        try:
            base_id = row.contents[5].text
            base_id = base_id.replace('\n', '')
        except: #Ri'saad is the only one that breaks it because there is no punctuation on his lack of a base ID
            base_id = '-'
        npcs.append({'NAME':npc_name, 'REF_ID':ref_id, 'BASE_ID':base_id})
    return npcs

if __name__=='__main__':
    run()