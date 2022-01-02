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
import sys
'''
    Known issues with certain commands:
13 - addfac - need to scrape data
16 - cast weird bug where values not assigned; got a concatenate string to none error
17 - remove 'none's from quest search
22 - duplicateallitems works with reference ids NOT base ids
28 - location ids
37 - actorid reference
54 - topicid reference
67 - more in depth setstage?
75 - words of power reference

    WHERE IM AT
    3. clean up skydata into one import
'''
class SkyData():
    #initializes data object for skyrim
    def __init__(self):
        self.commands = skyrim_commands
        self.avs = skyrim_avs
        #self.enchantments = skyrim_enchantments
        self.items = skyrim_items
        self.npcs = skyrim_npcs
        self.perks = skyrim_perks
        self.quests = skyrim_quests
        self.spells = skyrim_spells
        self.weather = skyrim_weather
        self.skills = skyrim_skills

class NVData():
    #initializes data object for new vegas
    def __init__(self):
        pass

class Command():
    #a single command with its components divided into parts
    def __init__(self, base='', target='', params = [], name=''):
        self.base = base
        self.target = target
        self.params = params
        self.name = name

    def text(self):
        t = ''
        if self.target != '':
            t += self.target+'.'
        t += self.base
        for i in self.params:
            t += ' '
            t += i
        return t

class ConsoleEngine():
    def __init__(self,game='skyrim'):
        if game == 'sk' or game == 'skyrim':
            self.data = SkyData()
        elif game == 'nv' or game == 'newvegas':
            self.data = NVData()
            ## TODO: scrape NV data
        self.running = True
        self.cmd_list = []


    def display_list(self):
        if self.cmd_list == []:
            return
        print('\n\tCommand List:\n')
        print('#','command','\tname')
        for i in self.cmd_list:
            print(self.cmd_list.index(i),i.text()+'\t'+i.name)

    def menu_input(self):
        valids = ['add','remove','clear','save','load','presets','quit']
        word = ''
        args = []
        while (word.lower() not in valids):
            word = input()
            word = word.lower()
        if word == 'add':
            self.add_cmd()
        elif word == 'remove':
            self.remove_cmd()
        elif word == 'clear':
            self.clear_cmds()
        elif word == 'save':
            self.save_list()
        elif word == 'load':
            self.load_list()
        elif word == 'presets':
            self.show_presets()
        elif word == 'quit':
            self.quit()

    def remove_cmd(self):
        word = input('enter # of command youd like to remove')
        self.cmd_list.pop(int(word))

    def add_cmd(self):
        print('\tNew Command\n')
        word = '-1'#wont be in list of keys
        while (int(word) not in self.data.commands):
            try:
                word = input('Enter # of command or other input to see list: ')
                word = int(word)#if an int was inputted this runs
            except:
                #if its not a number it displays the command list
                for i in self.data.commands:
                    print(i, self.data.commands[i][0])
        if word >= 10:
            target = self.choose_target()
        else:
            target = ''
        if word in self.data.commands:
            base = self.data.commands[word][0]#first item in dict list
            params = self.choose_params(word)
        word = input('name this commmand: ')
        if word == None:
            name = ''
        else:
            name = word
        self.cmd_list.append(Command(base, target, params, name))

    def choose_target(self):
        word = input('is the player the target? y for yes, else to search')
        if word.lower() == 'y':
            return 'player'
        else:
            return self.browse_ids(self.data.npcs, 'npc')

    def choose_params(self,id):#id is an int key to self.data.commands
        result = []
        for i in range(1,len(self.data.commands[id])):#number of params
            param = self.data.commands[id][i]
            if param == 'item_id':
                result.append(self.browse_ids(self.data.items, 'item')[1])
                                    #number is which data piece to use
            elif param == 'perk_id':
                result.append(self.browse_ids(self.data.perks, 'perk')[1])
            elif param == 'spell_id':
                result.append(self.browse_ids(self.data.spells, 'spell')[1])
            elif param == 'faction_id':
                result.append(self.browse_ids(self.data.factions, 'faction')[1])
            elif param == 'target_id':
                result.append(self.browse_ids(self.data.npcs, 'target')[1])
            elif param == 'skill':
                result.append(self.browse_ids(self.data.skills, 'skill')[0])
            elif param == 'quest_id':
                result.append(self.browse_ids(self.data.quests, 'quest')[1])
            elif param == 'atribute':
                result.append(self.browse_ids(self.data.avs, 'av')[0])
            elif param == '0':
                result.append('0')
            elif param == '1':
                result.append('1')
            else:
                word = input(param+'? ')
                result.append(word)
        return result

    def browse_ids(self, idref, name='item'):
        start_char = input("Enter the first letters of the desired "+name+": ")
        for i in idref:
            if idref[i][0] is None:
                print(i, idref[i])
            elif idref[i][0].lower().startswith(start_char):
                print(i, idref[i])
        word = input('which item is being added? ')
        try:
            word = int(word)
        except:
            word = 0
        item = self.data.items[word]
        return item

    def clear_cmds(self):
        word = input('are you sure? y for yes ')
        if word == 'y':
            self.cmd_list.clear()

    def save_list(self, filename=None):
        if filename == None:
            f = input('Enter filename:')
        else:
            f = filename
        #save file of just commands to be imported into skyrim
        file = open('batches/'+f+".txt", "w")
        for item in self.cmd_list:
            file.write(item.text()+'\n')
        file.close()
        #save file of commands and names to be loaded
        file = open('batches/batchdata/'+f+'.txt', 'w')
        for item in self.cmd_list:
            file.write(item.text()+' ,'+item.name+'\n')
        file.close()

    def load_list(self):
        params = []
        target = ''
        base = ''
        name = ''
        filename = input('Enter name of command batch: ')
        try:
            f = open('batches/batchdata/'+filename+'.txt', "r")
        except:
            print('file not found. try again')
            return
        self.clear_cmds()
        for line in f:
            cmd_text = line
            try:
                dot = cmd_text.index('.')
            except:
                dot = -1
            spc = cmd_text.index(' ')
            cma = cmd_text.index(',')
            if dot > -1: #there exists a .
                target = cmd_text[0:dot]
                base = cmd_text[dot+1:spc]
            else:
                base = cmd_text[0:spc]
            name = cmd_text[cma+1:-2]
            cmd_text = cmd_text[spc+1:cma]#only params Left
            params = cmd_text.split(' ')
            self.cmd_list.append(Command(base,target,params,name))
        return

    def show_presets(self):
        pass

        ''' dont implement the new feature yet. one thing at a time.
        print('\n\tPreset Command Batches:')
        presets = [
            'login', 'basicsetup', 'fullsetup', 'ebonyarmor', 'ebonyweapons',
            'destruction', 'restoration', 'conjuration', 'alteration', 'illusion',
            'shouts', 'soulgems', 'potions', 'daedrics', 'bigstats', 'perkpoints',
        ]
        for i in range(len(presets)):
            print(presets[i])
        word = input('which preset? ')
        word = word.lower()
        if word in presets:
            if word == 'basicsetup'

    def make_cmd(self, cmdnum=0, target='', params=[], name=''):
        base = self.data.commands[cmdnum][0]
        return Cmd(base,target,params,name)

    def ebonyarmor(self):
        ebony_set = []
        ebony_set.append(make_cmd(10,'player',[self.data.items[2176][0],1]))#armor
        ebony_set.append(make_cmd(10,'player',[self.data.items[2245][0],1]))#boots
        ebony_set.append(make_cmd(10,'player',[self.data.items[2329][0],1]))#gauntlets
        ebony_set.append(make_cmd(10,'player',[self.data.items[2382][0],1]))#helmet
        ebony_set.append(make_cmd(10,'player',[self.data.items[2452][0],1]))#shield
        return ebony_set

    def ebonyweapons(self):
        ebony_set = []
        ebony_set.append(make_cmd(10,'player',[self.data.items[2176][0],1]))#armor
        ebony_set.append(make_cmd(10,'player',[self.data.items[2245][0],1]))#boots
        ebony_set.append(make_cmd(10,'player',[self.data.items[2329][0],1]))#gauntlets
        ebony_set.append(make_cmd(10,'player',[self.data.items[2382][0],1]))#helmet
        ebony_set.append(make_cmd(10,'player',[self.data.items[2452][0],1]))#shield
        return ebony_set
        '''
    def quit(self):
        self.running = False

if __name__=='__main__':
    ce = ConsoleEngine()

    print('\n'+'#'*20+'\n\n\tSkyrim Console Command Batch File Generator')
    while(ce.running):
        ce.display_list()
        print('\n\tMain Menu.\nadd, remove, clear, save, load, quit')
        ce.menu_input()
