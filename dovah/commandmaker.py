from skyrimdata.skyrimcommands import skyrim_commands
from lookup import user_lookup, valuename_lookup
from rich import print
from rich.table import Table
from os import system, walk
MS_SKYPATH = 'C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition'
skypath = MS_SKYPATH
cmd_list = []

def run(args=None):
    if not args:
        run_text_ui()
    else:
        if args[0] =='load':
            if len(args) == 1:
                filename = input('Enter file to load: ')
            else: #the second one is the filename
                filename = args[1]
            load_cmds(filename)
            run_text_ui()
        else:
            #new keyword is used alongside arguments; py dovah cmd new
            if args[0] == 'new' and len(args) > 1:
                run_text_ui(args[1::])
            #py dovah cmd additem player 30
            elif args[0] != 'new':
                run_text_ui(args)
            #py dovah new
            else:
                run_text_ui()

def run_text_ui(args=None):
    def main_menu():
        return input('Main Menu: Save, Load, Add, Exit:  ').lower().split()
    while(True):
        system("cls")
        __show_cmds()
        if not args:
            choice = ['foo']
        else:
            choice = args
        while choice[0] not in ['add','save','load', 'exit']:
            choice = main_menu()

        if choice[0] == 'add':
            if len(choice) > 1:
                add_cmd(arg=choice[1::]) #further parsing happens by method
            else:
                add_cmd()

        if choice[0] == 'save':
            if len(choice) > 1:
                save_cmds(choice[1])#filename
            else:
                filename = input('What to name this file? ')
                save_cmds(filename)

        if choice[0] == 'load':
            if len(choice) > 1:
                load_cmds(choice[1])#filename
            else:
                load_cmds()

        if choice[0] == 'locate':
            locate_skyrim()

        if choice[0] == 'exit':
            break
        #after first loop, delete arguments and input from user
        choice.clear()
        if args: args.clear()

'''searches through folders to find skyrim and sets it to skypath'''
def locate_skyrim(start_folder='C:/'):
    for root, dirs, files in walk(start_folder):
        if 'SkyrimSE.exe' in files:
            skypath = root
            #print('located skyrim! heres the proof: ', files)
            return

'''Add Command to cmd_list'''
def add_cmd(arg=None):
    #first argument should be either key to command or name of command
    #if it is, then the command wizard proceeds and stops when input runs out
    #if it is not, them the command wizard regards input as garbage and
    #continues as if there were no arguments
    if arg:
        basearg = arg.pop(0)
        #check if the argument is the key corresponding to a command
        key = valuename_lookup(basearg, 'command')
        if key < 0:
            key = _ask_for_cmd_key()
        cmdbase = skyrim_commands[key][0]
    else:
        key = _ask_for_cmd_key()
        cmdbase = skyrim_commands[key][0]
    #next argument is the desired target if applicable
    target = None
    if key >= 10:
        if arg:
            target = arg.pop(0)  #e.g. add additem player
        else:
            target = _ask_for_target()

    #next is all remaining parameters get passed through ask_for_param
    other_params = skyrim_commands[key][1::]
    param_answers = []
    if arg:
        param_answers = arg  #e.g. add additem player f 20 => [f, 20]
    paramcount = len(param_answers)
    if len(other_params) > len(param_answers):
        param_answers.extend(_ask_for_param(other_params[paramcount::]))
    cmd_list.append(__form_cmd(cmdbase, target, param_answers))


'''Saves command as a list to folder designated as skyrim directory'''
def save_cmds(filename):
    #locate_skyrim()
    #writing file for this batch  to put in batches folder
    with open('/batches/'+filename+'.txt', "w") as f:
        for cmd in cmd_list:
            f.write(cmd+'\n')
        f.close()
    #writing file to put in skyrim directory
    with open(skypath+'/'+filename+'.txt', "w") as f:
        for cmd in cmd_list:
            f.write(cmd+'\n')
        f.close()

'''Loads commands from local folder in /batches'''
def load_cmds(filename):
    with open('/batches/'+filename+'.txt') as f:
        codes = f.readlines()
        for c in codes:
            cmd_list.append(c)

#Helper methods for the console command writer
def _ask_for_cmd_key():
    s = input('input name or id# of desired command: ')
    s_key = valuename_lookup(s, 'command')
    if s_key > 0:
        return s_key
    else:
        for i in skyrim_commands:
            print(str(i)+str(skyrim_commands[i]))
        while(s_key < 0):
            s = input('select key: ')
            s_key = valuename_lookup(s, 'command')
        return s_key

def _ask_for_target():
    if input('is the player the target? ').lower() == 'y':
        return 'player'
    else:
        return user_lookup('npc')

def _ask_for_param(paramIDs):
    params = []
    for p in paramIDs:
        if p == 'item_id':
            params.append(user_lookup('item')[1])
        elif p ==  'perk_id':
            params.append(user_lookup('perk')[1])
        elif p ==  'spell_id':
            params.append(user_lookup('spell')[1])
        elif p ==  'faction_id':
            params.append(user_lookup('faction')[1])
        elif p ==  'target_id':
            params.append(user_lookup('target')[1])
        elif p ==  'skill':
            params.append(user_lookup('skill')[0])
        elif p ==  'quest_id':
            params.append(user_lookup('quest')[1])
        elif p ==  'atribute':
            params.append(user_lookup('av')[0])
        elif p ==  '0':
            params.append('0')
        elif p ==  '1':
            params.append('1')
        else:
            word = input(p+'? ')
            params.append(word)
    return params

def __show_cmds():
    if len(cmd_list) < 1:
        print('No Commands Stored')
    else:
        print('Existing Commands: ')
        for cmd in cmd_list:
            print(cmd)

def __form_cmd(cmdbase, target=None, params=None):
    text = ''
    if target != None:
        text += target+'.'
    text += cmdbase+' '#space doesnt harm if theres no parameters after
    if params != None:
        text += ' '.join(params)
    return text
