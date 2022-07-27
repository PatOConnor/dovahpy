from .skyrimingredients import skyrim_ingredients as ingredients
from .skyrimalcheffects import skyrim_alcheffects as effects
from .sample_inventory import test
import numpy as np
from rich import print
from rich.panel import Panel
from rich.columns import Columns

DLC_TEXT = ['DG','HF','DB','CC']

class Cruncher:
    def __init__(self, inventory:list[list]=test):
        # takes list of strings and converts it to list 
        # of dictionary entries from 
        self.initial_inventory = inventory
        self.unrolled_inventory = []
        self.unroll_inventory()
        self.inventory = []
        self.fetch_dict_inventory()
        self.initial_size = len(self.inventory)
        self.potions = []
        self.matches = []

    #unrolls the item:quantity pair and returns [item1 ,item1, item2, [...]]
    def unroll_inventory(self):
        for item in self.initial_inventory:
            self.unrolled_inventory.extend([item[0].strip()] * item[1])

    # searches dictionary for corresponding entries to 
    # the strings in unrolled_inventory
    def fetch_dict_inventory(self):
        for i in range(len(self.unrolled_inventory)):
            #check if ingredient is the same as the previous one
            item = self.unrolled_inventory[i]
            # print(item); input()
            if i > 0:
                prev_item = self.unrolled_inventory[i-1]
                if item == prev_item:
                    # print(self.inventory, i); input()
                    self.inventory.append(self.inventory[-1])
                    continue
            #linear search thru ingredients; ptimary key is already an integer
            for j in ingredients: 
                ingr_name = ingredients[j]['NAME']
                if ingr_name[-2:] in ['DG', 'HF', 'DB']:#dlc item
                    ingr_name = ingr_name[:-2:]
                if ingr_name == item:
                    self.inventory.append(ingredients[j])
                    continue

    def roll_inventory(self):
        rolled_potions = {}
        for potion in self.potions:
            potion_name = potion[0]['NAME'] + ' x ' + potion[1]['NAME']
            if potion_name not in rolled_potions:
                rolled_potions[potion_name] = 1
            else:
                rolled_potions[potion_name] += 1
        return rolled_potions

    def print_data(self):
        item_panels = []
        pot = self.roll_inventory()

        for potion in pot:
            item_panels.append(Panel(f'{pot[potion]} of {potion}'))
        print(Columns(item_panels))
        print('Leftover: ')
        for item in self.inventory:
            print(item['NAME'])
        print(f'{len(self.potions)} made, {len(self.inventory)} items leftover')
        quit_words = ('q', 'quit')
        word = ''
        while(word not in quit_words):
            word = input('enter q to quit').lower().strip()

    """ MAIN METHOD AND FUNCTIONS HERE"""
    def run(self):
        #make 2d potions from the ingredients in the inventory
        self.make_2d_potions()


    def make_2d_potions(self):
        #effects dictionary but sorted by septim payout
        sorted_effects = list(sorted(effects, reverse=True, 
                              key = lambda i: effects[i]['VALUE']))
        # goes through effects from most valuable to least 
        # valuable, starting at invisibility
        for effect in sorted_effects[3::]:
            #list of strings
            possible_ingredients = effects[effect]['INGR']

            self.find_matches(possible_ingredients)
            effect_name = effects[effect]['NAME']

            # print(f'about to create potions of: {effect_name}')
            if len(self.matches) == 0: continue
            self.sort_matches_by_value(effect_name)

            #PAIR UP INGREDIENTS TO MAKE POTIONS
            while (self.matching_should_continue()):
                first_ingr = self.matches.pop(0)
                i = 0
                while i < len(self.matches):
                    if self.matches[i]['NAME'] != first_ingr['NAME']:
                        second_ingr = self.matches.pop(i)
                        self.potions.append([first_ingr, second_ingr])
                        #unsetting the first ingredient to check for hop-ons
                        first_ingr = None
                        break
                    else:
                        i += 1

            if len(self.matches) > 0:
                self.inventory.extend(self.matches)
                self.matches.clear()
# TODO TODO TODO 
    def make_3d_matches(self): pass
# -- go thru potions from high to low value
#     -- find most valuable efffect

#     -- given a potion with two ingredients:

#         what are the effects that could be added to the potion?

#         what are the ingredients on tap that have the most valuable effect?

#         add ingr if taking that ingredient for the potion cause a net increase in output value
        

    def find_matches(self, possible_ingredients:list[str]):
        i = 0
        while i < len(self.inventory):
            ingr = self.inventory[i]
            ingr_name = ingr['NAME']
            if ingr_name in possible_ingredients:
                self.matches.append(self.inventory.pop(i))
            else: i += 1


    def sort_matches_by_value(self, common_effect):
        #takes in a list of ingredients and the effect they have
        #returns the list of dictionaries sorted by how valuable they make the potion
        def best_multiplier(ingr, common_effect=common_effect):
            for ef in ingr['EFFECTS']:
                if ef['NAME'] == common_effect:
                    return max(ef['MAGNITUDEMULT'], ef['DURATIONMULT'], ef['VALUEMULT'])  
        self.matches = list(sorted(
            self.matches,
            reverse=True,
            key=lambda x: best_multiplier(x)
        ))

    def matching_should_continue(self):
        if len(self.matches) == 0: 
            return False
        first_item = self.matches[0]
        for item in self.matches[1:]:
            if item != first_item:
                return True
        return False

def run(inventory=test):
    c = Cruncher(inventory)
    c.run()
    c.print_data()

if __name__=='__main__':
    run()
