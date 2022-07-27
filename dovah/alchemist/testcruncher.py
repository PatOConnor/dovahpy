from alchemycruncher import Cruncher
from sample_inventory import test, smallinv
from rich import print

current_inv = smallinv

#ignore inv assignment, going to be passing functions params
c = Cruncher(current_inv)




c.unroll_inventory()
#unroll inventory works

#print(sum(x[1] for x in current_inv) == len(c.unrolled_inventory))
#print(current_inv)
#print(c.unrolled_inventory)

c.fetch_dict_inventory()
#fetch dictionary works

# print(sum(x[1] for x in current_inv) == len(c.inventory))
# print(len(c.inventory), len(c.unrolled_inventory))
#print(c.inventory)



c.initial_size = len(c.inventory)
c.find_matches(['Crimson Nirnroot', 'Nirnroot'])
#find matches works

# print(len(c.inventory) + len(c.matches) == len(c.unrolled_inventory))
# print(len(c.inventory), len(c.unrolled_inventory))
# print(len(c.matches))


c.sort_matches_by_value('Damage Health')
# print(c.matches[0]['NAME'] == 'Nirnroot')
# works

#
c.matching_should_continue()


#seems to be losing some ingredients along the way
c.make_2d_potions()
input('\n\n\n')
c.print_data()

total_amt = 2 *len(c.potions) + len(c.inventory)

print( total_amt == len(c.unrolled_inventory))
print( total_amt, len(c.unrolled_inventory))
#print(c.inventory)