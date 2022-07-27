"""This main method takes in shell arguments and 
    fires up the request subpackage. if there are 
    no arguments, the run() module is called to 
    get user input on where to go.            """
from sys import argv
import argparse
# it won't identify the run module as being a 
# submodule of scraper when imported alongside the others
from skyrimscraper import run as run_scraper
import run, lookup, commandmaker
from alchemist import alchemist as al



parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scraper", action="store_true", help="launch data scraper")
parser.add_argument("-l", "--lookup", action="store_true", help="launch lookup engine")
parser.add_argument("-a", "--alchemist", action="store_true", help="launch optimal alchemy")
parser.add_argument("-c", "--commands", action="store_true", help= "launch command maker")

args = parser.parse_args()
if args.scraper:
    run_scraper.run()
elif args.lookup:
    lookup.run()
elif args.alchemist:
    al.run()
elif args.commands:
    commandmaker.run()
else:
    run.run()