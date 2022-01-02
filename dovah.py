from skyrimdata.skyrimcommands import skyrim_commands
from skyrimdata.skyrimavs import skyrim_avs
#from skyrimdata.skyrimenchantments import skyrim_enchantments
from skyrimdata.skyrimitems import skyrim_items
from skyrimdata.skyrimnpcs import skyrim_npcs
from skyrimdata.skyrimperks import skyrim_perks
from skyrimdata.skyrimquests import skyrim_quests
from skyrimdata.skyrimspells import skyrim_spells
from skyrimdata.skyrimweather import skyrim_weather
from skyrimdata.skyrimskills import skyrim_skills

class Dovah:
    def __init__(self):
        self.cmd_list = {0:{'NAME':'Dummy', 'CODE':'Dummy'}}

    def help(self):
        print('show_cmds() : prints commands')
        print('add_command() : dialog to create console command. You can pass these parameters into it:')
        print('\t exact:text of command, key:id of command, target')

    #head methods
    def show_cmds(self):
        if len(self.cmd_list) == 1:
            print('No Commands Stored')
        else:
            for i in range(1,len(self.cmd_list)):
                print(self.cmd_list[i]['NAME'], '\n\t', self.cmd_list[i]['CODE'])

    def add_command(self, exact=None, name='', key=None, target=None, params=[]):
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
            self._ask_for_param(p)
        if name == '':
            name = input('Enter Desired Name or Press Enter: ')
        #adding to master dict
        cmd = {}
        cmd['NAME'] = name
        cmd['CODE'] = self._form_cmd(cmdbase, target, params)
        self.cmd_list[len(self.cmd_list)] = cmd.copy() #gonna be set to the next value

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
                word = input(param+'? ')
                params.append(word)
            return params

    def _form_cmd(self, cmdbase, target=None, params=None):
        text = ''
        if target != None:
            text += target+'.'
        text += cmdbase
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
