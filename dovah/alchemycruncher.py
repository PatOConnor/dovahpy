from skyrimdata.skyrimalchemy import ingredients, effects
import numpy as np

def crunch(inventory):
    inventory = singlify(inventory)
    #convert the strings into their dictionary entries from skyrimalchemy.ingredients
    inventory = convert_to_dict(inventory)
    potions, inventory = make_2d_potions(inventory)
    potions, inventory = stack_potions(potions, inventory)
    round2, inventory = make_2d_potions(inventory)
    round2, inventory = stack_potions(potions, inventory)
    potions.extend(round2)
    potions = convert_to_strings(potions)
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

def make_2d_potions(inventory):
    potion_list = []
    matches = []
    sorted_effects = effects_sorted_by_value(effects)
    #effect = 1:{'NAME':Paralysis, 'INGR':['', '', ...],  'VALUE':285}
    for effect in sorted_effects:
        possible_ingredients = effect['INGR']
        #deleting the DLC text
        for p in possible_ingredients:
            if p[-2:] in ['DG','HF','DB','CC']:
                p = p[:-2:]
        #select all the ingredients in pocket that will do the current effect:
        for i in range(len(inventory)):
            ingr_name = inventory[i]['NAME']
            if ingr_name in possible_ingredients:
                matches.append(inventory.pop(i))
        matches = sorted_by_value(matches)
        potion_group = []
        #pairing up the ingredients first-last, 2nd-2ndLast, etc.
        for i in range(len(matches)//2):
            first_ingr = matches.pop(0)
            second_ingr = matches.pop(-1)
            potion_group.append([first_ingr, second_ingr])
        if matches:#if there is one element left, it goes back into inventory
            inventory.append(matches.pop())
        #now there is a 2xN list of ingredients of the current examined effect
        potion_list.extend(potion_group)
    return potion_list, inventory

def stack_potions(potion_list, inventory):
    #go through each potion and find a way to supe it up

    #look for ingredients with the valued ingredient first in the inventory,
    #if none are found, take one from the shittiest potion available of that effect
    #the other ingredient gets added into the inventory

    #return the stacked list and the loose inventory
    pass


def effects_sorted_by_value(list_of_dicts):
    return effects
    #returns copy of the effects dictionary but sorted by septim payout

def sorted_by_value(list_of_dicts):
    #takes in a list of dictionary entries which each have MAGNITUDEMULT, DURATIONMULT, and VALUEMULT
    #returns a list, sorted by the largest of those three values
    return list_of_dicts


def convert_to_strings(potions):
    #the fucking victory lap
    pass

if __name__=='__main__':
    for test in test_lists:
        crunch(test)
