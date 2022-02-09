from dovah.skyrimdata.skyrimcommands import skyrim_commands
from dovah.skyrimdata.skyrimavs import skyrim_avs
#from dovah.skyrimdata.skyrimenchantments import skyrim_enchantments
from dovah.skyrimdata.skyrimitems import skyrim_items
from dovah.skyrimdata.skyrimnpcs import skyrim_npcs
from dovah.skyrimdata.skyrimperks import skyrim_perks
from dovah.skyrimdata.skyrimquests import skyrim_quests
from dovah.skyrimdata.skyrimspells import skyrim_spells
from dovah.skyrimdata.skyrimweather import skyrim_weather
from dovah.skyrimdata.skyrimskills import skyrim_skills
#from dovah.skyrimdata.alchemy import ingredients


def catalog_reference(category):

    if category == 'command':
        targetdict = skyrim_commands
    elif category == 'av':
        targetdict = skyrim_avs
    elif category == 'enchantments':
        targetdict = skyrim_enchantments
    elif category == 'item':
        targetdict = skyrim_items
    elif category == 'npcs':
        targetdict = skyrim_npcs
    elif category == 'perk':
        targetdict = skyrim_perks
    elif category == 'quest':
        targetdict = skyrim_quests
    elif category == 'spell':
        targetdict = skyrim_spells
    elif category == 'weather':
        targetdict = skyrim_weather
    elif category == 'skill':
        targetdict = skyrim_skills
    else:
        raise ValueError
    return targetdict

#small user text interface
def user_lookup(category): #catagory is string
    catalog = catalog_reference(category)
    start_char = input("Enter the first letters of the desired "+category+": ")
    for i in catalog:
        if catalog[i][0] is None:
            print(i, catalog[i])
        elif catalog[i][0].lower().startswith(start_char):
            print(i, catalog[i])
    while (True):
        word = input('which one is being added? ')
        item_key = valuename_lookup(word,category)
        if item_key > 0:
            break
    return catalog[item_key]

#returns the key of the item that has the argument string in the first element
def valuename_lookup(lookupstr, category=None):
    catalog = catalog_reference(category)
    #first, check if it itself is a number and continue on if it is not
    try:
        lookupstr = int(lookupstr)
        if lookupstr in catalog:
            return lookupstr
        else:
            return -1
    except ValueError:
        pass
    #next, check if its the first entry of the value
    for k in catalog:
        if catalog[k][0].lower() == lookupstr.lower():
            return k
    return -1
