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
from dovah.skyrimdata.alchemy import ingredients
import os

MS_SKYPATH = 'C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition'

class CommandMaker:

    def __init__(self, skypath=MS_SKYPATH):
        self.cmd_list = {0:{'NAME':'Dummy', 'CODE':'Dummy'}}
        self.skypath = skypath

    def help(self):
        print('show_cmds() : prints commands')
        print('add_command() : dialog to create console command. You can pass these parameters into it:')
        print('\t exact:text of command, key:id of command, target:usually player')
        print('locate_skyrim() : searches computer for skyrimse.exe')

    def pop(self, index):
        if index == 0: raise IndexError
        self.cmd_list.pop(index)

    '''searches through folders to find skyrim and sets it to self.skypath'''
    def locate_skyrim(self, start_folder='C:/'):
        for root, dirs, files in os.walk(start_folder):
            if 'SkyrimSE.exe' in files:
                self.skypath = root
                return

    #console command editor
    '''Prints console commands stored in self.cmd_list'''
    def show_cmds(self):
        if len(self.cmd_list) == 1:
            print('No Commands Stored')
        else:
            for i in range(1,len(self.cmd_list)):
                print(i, self.cmd_list[i]['NAME'], '\n\t', self.cmd_list[i]['CODE'])

    '''Enter Console Command Wizard'''
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
