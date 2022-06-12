import getskydata, getingredients, getalcheffects, getfactiondata,\
       getnpcdata, getlocationdata, getcommands, run
import argparse
from sys import argv


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', action="store_true", help="gather full dataset")
#these have their own scrapers
parser.add_argument('-ai', '--ingredients', action="store_true", help="get alchemy ingredients")
parser.add_argument('-ae', '--effects', action="store_true", help="get alchemy effects")
parser.add_argument('-c', '--commands', action="store_true", help="get dict of console commands")
parser.add_argument('-f', '--factions', action="store_true", help='get dict of factions')
parser.add_argument('-l', '--locations', action="store_true", help='get dict of locations')
parser.add_argument('-n', '--npcs', action="store_true", help="get NPCs data")
#these all are different arguments on the skyrimcommands.com scraper
parser.add_argument('-av', '--actorvalues', action="store_true", help='')
parser.add_argument('-i', '--items', action="store_true", help='')
parser.add_argument('-e', '--enchantments', action="store_true", help='')
parser.add_argument('-p', '--perks', action="store_true", help= '')
parser.add_argument('-q', '--quests', action="store_true", help= '')
parser.add_argument('-sp', '--spells', action="store_true", help='')
parser.add_argument('-sh', '--shouts', action="store_true", help='')
parser.add_argument('-w', '--weather', action="store_true", help='')

args = parser.parse_args()
all_data = False
if args.all:
    all_data = True
if args.ingredients or all_data:
    getingredients.run()
if args.effectsor or all_data:
    getalcheffects.run()
if args.commandsor or all_data:
    getcommands.run()
if args.factions or all_data:
    getfactiondata.run()
if args.locations or all_data:
    getlocationdata.run()
if args.npcs or all_data:
    getnpcdata.run()
if args.actorvalues or all_data:
    getskydata.run('avs')
if args.items or all_data:
    getskydata.run('items')
if args.enchantments or all_data:
    getskydata.run('enchantments')
if args.perks or all_data:
    getskydata.run('perks')
if args.quests or all_data:
    getskydata.run('quests')
if args.spells or all_data:
    getskydata.run('spells')
if args.weather or all_data:
    getskydata.run('weather')
else:
    run()

