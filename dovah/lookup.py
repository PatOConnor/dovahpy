from skyrimdata.skyrimcommands import skyrim_commands
from skyrimdata.skyrimavs import skyrim_avs
from skyrimdata.skyrimenchantments import skyrim_enchantments
from skyrimdata.skyrimitems import skyrim_items
from skyrimdata.skyrimnpcs import skyrim_npcs
from skyrimdata.skyrimfactions import skyrim_factions
from skyrimdata.skyrimperks import skyrim_perks
from skyrimdata.skyrimquests import skyrim_quests
from skyrimdata.skyrimspells import skyrim_spells
from skyrimdata.skyrimweather import skyrim_weather
from skyrimdata.skyrimskills import skyrim_skills
from skyrimdata.skyrimingredients import skyrim_ingredients
from skyrimdata.skyrimalcheffects import skyrim_alcheffects
from skyrimdata.skyrimlocations import skyrim_locations
from rich.panel import Panel
from rich.columns import Columns
from rich.layout import Layout
from rich import print
import os

data_dict = {
    'avs':skyrim_avs,
    'commands':skyrim_commands,
    'effects':skyrim_alcheffects,
    'enchantments':skyrim_enchantments,
    'factions':skyrim_factions,
    'ingredients':skyrim_ingredients,
    'items':skyrim_items,
    'locations':skyrim_locations,
    'npcs':skyrim_npcs,
    'perks':skyrim_perks,
    'quests':skyrim_quests,
    'skills':skyrim_skills,
    'spells':skyrim_spells,
    'weather':skyrim_weather,
}

"""loops user_lookup method"""
def run():
    lookup_results = []
    quit = ('q', 'quit')
    ui = ui_layout()
    while True:
        ui = update_lookup_list(ui, lookup_results)
        print(ui)
        choice = input('category: ').lower().strip()
        if choice in data_dict:
            lookup_results.append(user_lookup(choice))
        elif choice in quit:
            break

#small user text interface
def user_lookup(category)->str: 
    #grabs dictionary to pick through
    catalog = data_dict[category]
    while True:
        search_str = input("Enter the first letters of the desired "+category+": ")
        search_data = get_filtered_catalog(search_str, catalog)
        print(rich_table_output(search_data, category))
        #this is effectively a "while(True)" that only runs if there is search data
        while len(search_data) > 0:
            print('Enter the [green]local ID[/green] of your desired item')
            word = input('\t:')
            try: 
                word = int(word)
                if word < len(search_data):
                    name = search_data[word]['NAME']
                    code = get_relevant_data_of(search_data[word], category)
                    return (name, code)
            #value error is caused by being unable to cast to int
            except ValueError: continue


def get_relevant_data_of(dict_entry, category)->str:
    if category == 'factions':
        return dict_entry['INFO']['Form ID']
    elif category == 'npcs':
        return dict_entry['REF_ID']
    else:
        return dict_entry['CODE']

#returns the key of the item that has the argument string in the first element
def catalog_lookup(lookupstr, category)->int:
    catalog = data_dict[category]
    #first, check if it itself is a number and continue on if it is not
    try:
        lookupstr = int(lookupstr)
        if lookupstr in skyrim_commands:
            return lookupstr
        else:
            return -1
    except ValueError:
        pass
    #nif not a number, check if it matches the name of a catalog entry
    for k in catalog:
        if catalog[k]['NAME'].lower().strip() == lookupstr.lower().strip():
            return k
    return -1

def get_filtered_catalog(search_str, catalog)->list[dict]:
    filtered_catalog = []
    for i in catalog:
        catalog_item_str = catalog[i]['NAME']
        if search_str.lower().strip() in catalog_item_str.lower().strip():
            filtered_catalog.append(catalog[i])
    return filtered_catalog


def rich_table_output(table_data, category)->Columns:
    markupstr = '{}\n[green]{}[/green]\t[yellow]{}[/yellow]'
    return Columns([Panel(markupstr.format(x['NAME'], table_data.index(x),
                    get_relevant_data_of(x, category))) for x in table_data])

def ui_layout()->Layout:
    terminal_size = os.get_terminal_size()
    height = terminal_size.lines
    width = terminal_size.columns
    ui = Layout()
    ui.split_column(
        Layout(name='DovahPy is a Free and Open Source Tool', size=1),
        Layout(name="titlebox", size=3),
        Layout(name="contentbox", size=height-4)
    )
    ui["contentbox"].split_row(
        Layout(name="infobox", size=3*width//5),
        Layout(name="lookupbox")
    )
    ui['titlebox'].update(Panel("Skyrim Lookup Tool", expand=False))
    infostr = '  Welcome to skyrim data lookup tool.\n\n  Use this software to easily source the correct reference codes to use in skyrim without having to scour wikis and open tabs.\n\n  Input the piece of data you would like to download or all to download all.\n\n  The different categories are '
    for keys in data_dict:
        if keys != 'weather': #last item 
            infostr += keys+', ' 
        else:
            infostr += 'and weather.\n\n  In addition, input "show" to see the list you\'ve gathered, "save" to save your list as a file, and "q" or "quit" to exit the program. \n\n  Thank you for using DovahPy!'
    ui["infobox"].update(Panel(infostr, expand=False))
    return ui

def update_lookup_list(ui, lookup_results):
    markdown = "{}\n[yellow]{}[yellow]"
    panels = [Panel(markdown.format(x[0], x[1])) for x in lookup_results]
    ui['lookupbox'].update(Columns(panels))
    return ui


if __name__=="__main__":
    run()