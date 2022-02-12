import commandmaker, alchemist, voiceattack, lookup
from skyrimdata import scraper_menu
from sys import argv
from rich import print

module_argument = '0'
if len(argv) > 1: #there are arguments present
    module_argument = argv[1].lower()
else:
    choice_input = True
    while(choice_input):
        choice_input = False #only runs once unless invalid input tells it to run again
        print('#'*10)
        print('Welcome to DovahPy. Which module would you like to access?')
        print('\n 1. Console Command Creator\n', '2. Best Alchemy\n', '3. Item Code Lookup\n', '4. Voice Attack Commands\n', '5. Data Scraper')
        module_argument = input('Enter Selection: ')
        if module_argument == '1':
            module_argument = 'c'
        elif module_argument == '2':
            module_argument = 'a'
        elif module_argument == '3':
            module_argument = 'l'
        elif module_argument == '4':
            module_argument = 'v'
        elif module_argument == '5':
            module_argument = 'd'
        else:
            choice_input = True
if module_argument in ['c', 'cmd', 'cmds', 'command', 'commands']:
    if len(argv) > 2:#additional arguments
        commandmaker.run(argv[2::])
    else:
        commandmaker.run()
elif module_argument in ['a', 'alch', 'alchemy', 'alchemist']:
    alchemist.run()
elif module_argument in ['l', 'look', 'lookup']:
    if len(argv) > 2:#string to look up
        lookup.run(argv[2])
    else:
        lookup.run()
elif module_argument in ['v', 'va', 'voice', 'voiceattack']:
    voiceattack.run()
elif module_argument in ['s', 'd', 'data', 'datascraper', 'scraper']:
    scraper_menu.run(argv[2::])
