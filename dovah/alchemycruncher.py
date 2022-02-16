from skyrimdata.skyrimalchemy import ingredients, effects
import numpy as np
from alchemy_lists import test
from rich import print

def crunch(inventory):
    inventory = singlify(inventory)
    print(len(inventory))
    #convert the strings into their dictionary entries from skyrimalchemy.ingredients
    inventory = convert_to_dict(inventory)
    potions, inventory = make_2d_potions(inventory)
    #potions, inventory = stack_potions(potions, inventory)
    #round2, inventory = make_2d_potions(inventory)
    #round2, inventory = stack_potions(potions, inventory)
    #potions.extend(round2)
    potions = convert_to_strings(potions)
    #print(potions, inventory)
    return potions

#takes the quantity parameter and returns a 1d list of all the ingredient names
def singlify(inventory):
    stretched_list = []
    for item in inventory:
        while item[1] > 0:
            stretched_list.append(item[0].strip())
            item[1] -= 1
    return stretched_list

#inventory is a 2xn list where the first elem is a string
#and the second elem is an integer of count
def convert_to_dict(inventory):
    inv_dicts = []
    #goes through all alchemy ingredients
    for i in ingredients:
        for item in inventory:
            ingr_name = ingredients[i]['NAME']
            if ingr_name[-2:] in ['DG', 'HF', 'DB']:#dlc item
                ingr_name = ingr_name[:-2:]
            if ingr_name == item:
                inv_dicts.append(ingredients[i])
                continue
    return inv_dicts

def make_2d_potions(inventory):
    potion_list = []
    matches = []
    sorted_effects = effects_sorted_by_value()
    #effect = 1:{'NAME':Paralysis, 'INGR':['', '', ...], ... , 'VALUE':285}
    for effect in sorted_effects[3::]:
        possible_ingredients = effects[effect]['INGR']
        #deleting the DLC text
        for p in possible_ingredients:
            if p[-2:] in ['DG','HF','DB','CC']:
                p = p[:-2:]
        #select all the ingredients in pocket that will do the current effect:
        for ingr in inventory:
            ingr_name = ingr['NAME']
            if ingr_name in possible_ingredients:
                matches.append(ingr)
                inventory.remove(ingr)
        matches = sorted_by_value(matches, effects[effect]['NAME'])
        potion_group = []
        #pairing up the ingredients first-last, 2nd-2ndLast, etc.
        for i in range(len(matches)//2):

            # TODO: need to write a better algorithm for pairing up the potions
            #       right now it combines 2 of the same ingredient



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


def effects_sorted_by_value():
    return list(sorted(effects, key = lambda i: effects[i]['VALUE']))
    #returns copy of the effects dictionary but sorted by septim payout

def sorted_by_value(list_of_ingr, common_effect):
    #takes in a list of ingredients and the effect they have
    #returns the list of dictionaries sorted by how valuable they make the potion
    sorted_list = []
    for ingr in list_of_ingr:
        ingr_effect = []#grabbing and separating the common effect so it can get sorted by that
        for ef in ingr['EFFECTS']:
            if ef['NAME'] == common_effect:
                best_multiplier = max(ef['MAGNITUDEMULT'], ef['DURATIONMULT'], ef['VALUEMULT'],)
                ingr_effect.extend([ingr, best_multiplier])
                break
        sorted_list.append(ingr_effect)
    sorted_list.sort(key=lambda x:x[1])
    trimmed_list = [x[0] for x in sorted_list]
    return trimmed_list


def convert_to_strings(potions):
    #the fucking victory lap
    print(len(potions))
    for p in potions:
        print(p[0]['NAME'], p[1]['NAME'])

def run(inventory=test): #for testing from dovah main menu
    crunch(inventory)

if __name__=='__main__':
    run()
