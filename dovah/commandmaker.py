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
import os

MS_SKYPATH = 'C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition'

def run(args=None):
    command_maker = CommandMaker()
    if args:
        if args[0] =='load':
            if len(args) == 1:
                filename = input('Enter file to load: ')
            else: #the second one is the filename
                filename = args[1]
            command_maker.load_cmds(filename)
    command_maker.run_text_ui()


class CommandMaker:
    def __init__(self, skypath=MS_SKYPATH):
        self.cmd_list = {}
        self.skypath = skypath

    def run_text_ui(self):
        while(True):
            self.show_cmds()
            choice = ['foo']
            while choice[0] not in ['add','save','load','locate', 'exit']:
                choice = self.ask_user()
            if choice[0] == 'add':
                if len(choice) > 1:
                    self.add_cmd(arg=choice[1::]) #further parsing happens by method
                else:
                    self.add_cmd()
            if choice[0] == 'save':
                if len(choice) > 1:
                    self.save_cmds(choice[1])#filename
                else:
                    self.save_cmds()
            if choice[0] == 'load':
                if len(choice) > 1:
                    self.load_cmds(choice[1])#filename
                else:
                    self.load_cmds()
            if choice[0] == 'locate':
                self.locate_skyrim()
            if choice[0] == 'exit':
                break

    def ask_user(self):
        return input('Enter Your Command from save, load, add or locate followed by additional parameters: ').split()


    def help(self):
        print('show_cmds() : prints commands')
        print('add_command() : dialog to create console command. You can pass these parameters into it:')
        print('\t exact:text of command, key:id of command, target:usually player')
        print('locate_skyrim() : searches computer for skyrimse.exe')

    def pop(self, index):
        if index == 0:
            raise IndexError
        self.cmd_list.pop(index)

    '''searches through folders to find skyrim and sets it to self.skypath'''
    def locate_skyrim(self, start_folder='C:/'):
        for root, dirs, files in os.walk(start_folder):
            if 'SkyrimSE.exe' in files:
                self.skypath = root
                return

    #console command editorz
    '''Prints console commands stored in self.cmd_list'''
    def show_cmds(self):
        if len(self.cmd_list) <= 1:
            print('No Commands Stored')
        else:
            for i in range(1,len(self.cmd_list)):
                print(i, self.cmd_list[i]['NAME'], '\n\t', self.cmd_list[i]['CODE'])

    '''Enter Console Command Wizard'''

    def add_cmd(self, arg=None):
        #first argument should be either key to command or name of command
        #if it is, then the command wizard proceeds and stops when input runs out
        #if it is not, them the command wizard regards input as garbage and
        #continues as if there were no arguments
        if arg:
            basearg = arg.pop(0)
            #check if the argument is the key corresponding to a command
            try:
                basearg = int(basearg)
            except ValueError: #check if its a number
                pass
            if basearg in skyrim_commands:#e.g. 'add 10'
                key = basearg
                cmdbase = skyrim_commands[basearg][0]
            else:
                for c in skyrim_commands:#check if argument is the name of a command
                    if basearg == skyrim_commands[c][0]:
                        key = c
                        cmdbase = basearg#e.g. 'add additem', 'add setscale'
                        break
                #bad input means loop finishes
                key = self._ask_for_cmd_key()
                cmdbase = skyrim_commands[key][0]
        else:
            key = self._ask_for_cmd_key()
            cmdbase = skyrim_commands[key][0]

        #next argument is the desired target if applicable
        if key >= 10:
            if arg:
                target = arg.pop(0)  #e.g. add additem player
            else:
                target = self._ask_for_target()
        else:
            target = None

        #next is all remaining parameters as per the if/else hell below
        other_params = skyrim_commands[key][1::]
        param_answers = []
        if arg:
            param_answers = arg  #e.g. add additem player f 20 => [f, 20]

        #runs if unfilled parameter slots, offset by the command base
        if len(other_params) > len(param_answers):
            param_answers.extend(self._ask_for_param(other_params[len(param_answers)::]))

        name = input('Enter Desired Name or Press Enter: ')
        if not name:
            name=' '

        cmd = {}
        cmd['NAME'] = name
        cmd['CODE'] = self._form_cmd(cmdbase, target, param_answers)
        self.cmd_list[len(self.cmd_list)] = cmd.copy() #gonna be set to the next value
        print(cmd['NAME'], cmd['CODE'])

    '''
    def add_cmd(self, key=None, exact=None, name=' ', target=None, params=[]):
        if exact != None:
            cmd = {}
            cmd['NAME'] = name
            cmd['CODE'] = exact
            self.cmd_list[len(self.cmd_list)] = cmd.copy()
            return
        if key:
            cmdbase = skyrim_commands[key][0]
        else:
            key = self._ask_for_cmd_key()
            cmdbase = skyrim_commands[key][0]
        if key >= 10 and target == None:
            target = self._ask_for_target()
        if len(skyrim_commands[key]) > 1:
            p = skyrim_commands[key][1::]
            params = self._ask_for_param(p)
        if name == ' ':
            name = input('Enter Desired Name or Press Enter: ')
        #adding to master dict
        cmd = {}
        cmd['NAME'] = name
        cmd['CODE'] = self._form_cmd(cmdbase, target, params)
        self.cmd_list[len(self.cmd_list)] = cmd.copy() #gonna be set to the next value
    '''
    '''Saves command as a list to folder designated as skyrim directory'''
    def save_cmds(self, filename, skypath=None):
        if skypath==None: skypath=self.skypath
        #if theres not a folder for this batch already, make one:
        os.makedirs(os.path.dirname('/batches/'+filename), exist_ok=True)

        #writing file for this batch  to put in batches folder
        with open('/batches/'+filename+'/code.txt', "w") as f:
            for cmd in self.cmd_list:
                f.write(cmd['CODE']+'\n')
            f.close()

        #writing file to put names in alongside previous file
        with open('/batches/'+filename+'/names.txt', "w") as f:
            for cmd in self.cmd_list:
                f.write(cmd['CODE']+'\n')
            f.close()

        #writing file to put in skyrim directory
        with open(skypath+'/'+filename+'.txt') as f:
            for cmd in self.cmd_list:
                f.write(cmd['CODE']+'\n')
            f.close()

    '''Loads commands from local folder in /batches'''
    def load_cmds(self, filename):
        with open('/batches/'+filename+'/code.txt') as c, open('/batches/'+filename+'/code.txt') as n:
            codes = c.readlines()
            names = n.readlines()
            for i in range(len(codes)):#they will have same length
                cmd = {}
                cmd['CODE'] = codes[i]
                cmd['NAME'] = names[i]
                self.cmd_list[len(self.cmd_list)] = cmd.copy()

    #Helper methods for the console command writer
    def _ask_for_cmd_key(self):
        s = ''
        for i in skyrim_commands:
            print(i, skyrim_commands[i])
        while(s not in skyrim_commands):
            s = input('select key: ')
            try:
                s = int(s)
            except ValueError: #wait for user to type a number
                continue
        return s

    def _ask_for_target(self):
        if input('is the player the target? ').lower() == 'y':
            return 'player'
        else:
            return self.browse_ids(catalog=skyrim_npcs, title='npc')

    def _ask_for_param(self, paramIDs):
        params = []
        for p in paramIDs:
            print(p)
            if p == 'item_id':
                params.append(self._browse_ids(skyrim_items, 'item')[1])
            elif p ==  'perk_id':
                params.append(self._browse_ids(skyrim_perks, 'perk')[1])
            elif p ==  'spell_id':
                params.append(self._browse_ids(skyrim_spells, 'spell')[1])
            elif p ==  'faction_id':
                params.append(self._browse_ids(skyrim_factions, 'faction')[1])
            elif p ==  'target_id':
                params.append(self._browse_ids(skyrim_npcs, 'target')[1])
            elif p ==  'skill':
                params.append(self._browse_ids(skyrim_skills, 'skill')[0])
            elif p ==  'quest_id':
                params.append(self._browse_ids(skyrim_quests, 'quest')[1])
            elif p ==  'atribute':
                params.append(self._browse_ids(skyrim_avs, 'av')[0])
            elif p ==  '0':
                params.append('0')
            elif p ==  '1':
                params.append('1')
            else:
                word = input(p+'? ')
                params.append(word)
        return params

    def _form_cmd(self, cmdbase, target=None, params=None):
        text = ''
        if target != None:
            text += target+'.'
        text += cmdbase+' '#space doesnt harm if theres no parameters after
        if params != None:
            text += ' '.join(params)
        return text

    def _browse_ids(self, catalog, title='item'): #catalog is string
        start_char = input("Enter the first letters of the desired "+title+": ")
        for i in catalog:
            if catalog[i][0] is None:
                print(i, catalog[i])
            elif catalog[i][0].lower().startswith(start_char):
                print(i, catalog[i])
        word = input('which item is being added? ')
        try:
            word = int(word)
        except:
            word = 0
        item = skyrim_items[word]
        return item
