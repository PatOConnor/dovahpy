"""This module prints instructions and gets 
   user input on which module to access"""
import lookup, commandmaker
from alchemist import alchemist
# it won't identify the run module as being a 
# submodule of scraper when imported alongside the others
from skyrimscraper import run as run_scraper
from rich.layout import Layout
from rich.panel import Panel
from rich.columns import Columns
from rich import print
import os


sub_modules = {
    'scraper':run_scraper.run,
    'commands':commandmaker.run,
    'lookup':lookup.run,
    'alchemist':alchemist.run
}

def run():
    quit_words = ('q', 'quit')
    ui = generate_layout()
    while True:
        print(ui)
        word = input('Enter desired submodule or q/quit to exit: ')
        if word.lower().strip() in quit_words:
            break
        elif word in sub_modules:
            sub_modules[word]()
        input()

def generate_layout():
    terminal_size = os.get_terminal_size()
    # height = terminal_size.lines
    width = terminal_size.columns
    ui = Layout()
    ui.split_column(
        Layout(name="DovahPy is a free and open-source package", size=1),
        Layout(name="titlebox", size=3),
        Layout(name="content")
    )
    ui["content"].split_row(
        Layout(name="infobox", size=4*width//5),
        Layout(name="commands")
    )
    info_text = [
        'Welcome to DovahPy!',
        'In this package there are four modules for you to use to make playing Skyrim on PC easier.',
        'Skyrim Scraper accesses the internet to retrieve the item, npc, etc data for skyrim. It has already been ran, but it\'s there in case one needs to get a new copy.',
        'Lookup is used to quickly search for codes of items in the list of items',
        'Command Maker is used to create batch files of multiple console commands and saves them in the skyrim root folder.',
        'Alchemist takes a look at your skyrim inventory and gives you a list of the most valuable potions you can make with what you have.',
        'Notice: If you have not installed Tesseract, alchemist will not work. In addition, alchemist requires Skyrim to be currently in-game, and will input keypresses to access the inventory.',
        'Thank you for trying out DovahPy!'
    ]
    ui["titlebox"].update(Panel('DovahPy Skyrim Assistance Tool', expand=False))
    ui["infobox"].update(Panel('\n\n  '.join(info_text)))
    ui["commands"].update(Columns([Panel(x) for x in sub_modules]))
    return ui

if __name__ == '__main__':
    run()