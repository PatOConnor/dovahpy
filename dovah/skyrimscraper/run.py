"""Cli display to pick which piece of data to download."""
"""There is a lot of overlap with the main method"""
from rich.panel import Panel
from rich.columns import Columns
from rich.layout import Layout
from rich import print
from . import getskydata, getingredients, getalcheffects, getfactiondata,\
              getnpcdata, getlocationdata, getcommands


def run():
    scraper_menu = ( ('0','all'), ('1','ingredients'), ('2','effects'),
                     ('3','commands'), ('4','factions'), ('5','locations'), ('6','npcs'), 
                     ('7','avs'), ('8','items'), ('9','enchantments'), ('10','perks'),
                     ('11','quests'), ('12','spells'), ('13','weather'), )
    pretty_strings = [f'[b][yellow]{x[0]}[/yellow][/b] : {x[1]}' for x in scraper_menu]
    panels = [Panel(x) for x in pretty_strings]
    
    while(True):
        quit = ('q', 'quit')
        print(Panel("Skyrim Scraper", expand=False))
        print(Columns(panels, expand=False))
        all_data = False
        choice = input("Which data would you like to download? q or quit to exit. ")
        if choice in quit:
            break
        elif choice in scraper_menu[0]:
            all_data = True
        if choice in scraper_menu[1] or all_data:
            getingredients.run()
        if choice in scraper_menu[2] or all_data:
            getalcheffects.run()
        if choice in scraper_menu[3] or all_data:
            getcommands.run()
        if choice in scraper_menu[4] or all_data:
            getfactiondata.run()
        if choice in scraper_menu[5] or all_data:
            getlocationdata.run()
        if choice in scraper_menu[6] or all_data:
            getnpcdata.run()
        if choice in scraper_menu[7] or all_data:
            getskydata.run('avs')
        if choice in scraper_menu[8] or all_data:
            print('The items list is 81 pages long. this will take some time.')
            getskydata.run('items')
        if choice in scraper_menu[9] or all_data:
            getskydata.run('enchantments')
        if choice in scraper_menu[10] or all_data:
            getskydata.run('perks')
        if choice in scraper_menu[11] or all_data:
            getskydata.run('quests')
        if choice in scraper_menu[12] or all_data:
            getskydata.run('spells')
        if choice in scraper_menu[13] or all_data:
            getskydata.run('weather')



if __name__=="__main__":
    run()