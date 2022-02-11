from skyrimdata.skyrimalchemy import ingredients, effects
import np as numpy


def crunch(inventory):
    inventory = singlify(inventory)
    #convert the strings into their dictionary entries from skyrimalchemy.ingredients
    inventory = convert_to_dict(inventory)
    #separate inventory into ingredients with value multipliers and ingredients without
    #the value multiplier overrides any boost from the magnitude multiplier, so
    #the magnitude multipliers shouldn't be wasted by pairing them with valmults


    inventory = convert_to_array(inventory)
    potions_array = make_potions(inventory)
    potions = convert_to_string(potions_array)
    return potions

#takes the quantity parameter and returns a 1d list of all the ingredient names
def singlify(inventory):
    stretched_list = []
    for item in inventory:
        while item[1] > 0:
            stretched_list.append(item[0])
            item[1] -= 1

#inventory is a 2xn list where the first elem is a string
#and the second elem is an integer of count
def convert_to_dict(inventory):
    inv_dicts = []
    #goes through all alchemy ingredients
    for ingr in ingredients:
        for item in inventory:
            ingr_name = ingr['NAME']
            if ingr_name[-2:] in ['DG', 'HF', 'DB']:#dlc item
                ingr_name = ingr_name[:-2:]
            if ingr_name == item:
                inv_dicts.append(ingr)
                continue
    return inv_dicts


def convert_to_array(inventory):
    
