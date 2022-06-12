from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen
import os
from rich import print
from .writetofile import write_to_file

def run(is_test=False):
    url = 'https://en.uesp.net/wiki/Skyrim:Console'
    commands = scrape_page(url)
    write_to_file('commands', commands, is_test)

def scrape_page(url_string):
    commands = []
    try:
        page = urlopen(url_string)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('div', {'id':'mw-content-text'})
    table = content.find('table',  {'class':'wikitable centered'})
    rows = table.find_all('tr')
    #skip first row
    for row in rows[1::]:
        #not a header row
        if len(row) == 7:
            command = row.contents[1].text
            #known rows to not include
            if not (len(command) > 50 or command.startswith('000') or 
                command.startswith('xx0') or 
                command in ['Faction ID', 'Whiterun', 'Solitude', 'Windhelm', 
                            'Markarth', 'Riften', 'Morthal', 'Dawnstar',
                            'Winterhold', 'Falkreath', 'High Hrothgar']):           
                details = row.contents[3].text
                command_dict = parse_command(command, details)
                commands.append(command_dict)
    return commands


def parse_command(command, details):
    new_command = dict()
    if command.find('<') == -1:
        new_command['NAME'] = command
        new_command['PARAMS'] = None
    else:
        cmd_parts = command.split('<') #foo <bar> <baz> -> [foo, bar>, baz>]
        new_command['NAME'] = cmd_parts.pop(0)
        cmd_parts = ['<'+x for x in cmd_parts]
        cmd_parts = [x.replace('\xa0', ' ') for x in cmd_parts]
        new_command['PARAMS'] = cmd_parts
        if new_command['PARAMS'] == '<container/NPC refID>':
            # there's no way to get refIDs of containers, so 
            # the duplicateallitems command is being considered 
            # a command that targets NPCs
            new_command['PARAMS'] = '<target>'
    new_command['DETAILS'] = details.replace('\xa0', ' ')
    return new_command
            
if __name__ == '__main__':
    run()
