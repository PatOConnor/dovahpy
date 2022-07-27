from skyrimdata.skyrimcommands import skyrim_commands
from rich import print
from rich.panel import Panel
from rich.columns import Columns
# from rich.table import Table
from rich.layout import Layout
from os import system, get_terminal_size, path
import lookup

def run():
    cm = CommandMaker()
    cm.run()

class CommandMaker:
    MS_SKYPATH = 'C:\Program Files (x86)\Steam\steamapps\common\Skyrim Special Edition'  
    def __init__(self, skypath=None):
        self.cmd_list = []        
        if skypath == None:
            self.skypath = CommandMaker.MS_SKYPATH
        elif skypath == 'find':
            self.skypath = CommandMaker.locate_skyrim()
        else:
            self.skypath = skypath
        self.generate_layout()
        self.panel_markdown = '[green]{}[/green] [yellow]{}[/yellow]\n{}'

    def run(self, args=None):
        if not args:
            self.run_text_ui()
        elif args[0] =='load':
            if len(args) == 1:
                filename = input('Enter file to load: ')
            else: #the second one is the filename
                filename = args[1]
            self.load_cmds(filename)
            self.run_text_ui()
        else:
            #the word "new" may or may not be present
            if args[0] == 'new' and len(args) > 1:
                self.run_text_ui(args[1::])
            else:
                self.run_text_ui(args)

    def run_text_ui(self, args=None):
        def main_menu(): return input('Main Menu: Save, Load, Add, Remove, Exit:  ').lower().split()
        while(True):
            self.update_commands_box()
            print(self.ui)
            if not args: choice = ['foo']
            else:        choice = args
            while choice[0] not in ['add','save','load', 'exit', 'remove']:
                choice = main_menu()
                if not choice: choice = ['foo']
            
            if choice[0] == 'add':
                if len(choice) > 1:
                    self.add_cmd(arg=choice[1::]) #further parsing happens by method
                else:
                    self.add_cmd()

            if choice[0] == 'save':
                if len(choice) > 1:
                    self.save_cmds(choice[1])#filename
                else:
                    filename = input('What to name this file? ')
                    self.save_cmds(filename)

            if choice[0] == 'load':
                if len(choice) > 1:
                    self.load_cmds(choice[1])#filename
                else:
                    self.load_cmds()

            if choice[0] == 'remove':
                print('i am here')
                if len(choice) > 1:
                    self.remove_cmd(choice[1])#index
                else:
                    self.remove_cmd()

            if choice[0] == 'exit':
                break
            #after first loop, delete arguments and input from user
            choice.clear()
            if args: args.clear()


    '''Add Command to cmd_list'''
    def add_cmd(self, arg=None):
        #first argument should be either key to command or name of command
        #if it is, then the command wizard proceeds and stops when input runs out
        #if it is not, them the command wizard regards input as garbage and
        #continues as if there were no arguments
        if arg:
            basearg = arg.pop(0)
            #check if the argument is the key corresponding to a command
            k = lookup.catalog_lookup(basearg, 'commands')
            if k < 0:
                k = CommandMaker._ask_for_cmd_key()
            cmdbase = skyrim_commands[k]['NAME']
        else:
            k = CommandMaker._ask_for_cmd_key()
            cmdbase = skyrim_commands[k]['NAME']
        #next argument is the desired target if applicable
        if arg:
            target = arg.pop(0)  #e.g. add additem player
        elif 24 <= k <= 94 or k in [4,7,8]:
            target = CommandMaker._ask_for_target()
        else:
            target = ''
        #next is all remaining parameters get passed through ask_for_param
        other_params = skyrim_commands[k]['PARAMS']
        param_answers = []
        if arg:
            param_answers = arg  #e.g. add additem player f 20 => [f, 20]
        paramcount = len(param_answers)
        if other_params and len(other_params) > len(param_answers):
            param_answers.extend(CommandMaker._ask_for_param(other_params[paramcount::]))
        command = CommandMaker.__form_cmd(cmdbase, target, param_answers)
        name = input('Input the nickname of this command:')
        name = ' ' if name == None else name
        # input(f'{cmdbase} {target}, {param_answers}')
        # input(f'{command}, {name}')
        self.cmd_list.append((name, command))


    '''Saves command as a list to folder designated as skyrim directory'''
    def save_cmds(self, filename):
        #writing file for skyrim folder
        skyrim_filename = self.skypath+'/'+filename+'.txt'
        with open(skyrim_filename, "w") as f:
            for cmd in self.cmd_list:
                f.write(cmd[1]+'\n')
            f.close()
        
        batches_filename = path.dirname(__file__)+'/batches/'+filename+'.txt'
        with open(batches_filename, "w") as f:
            for cmd in self.cmd_list:
                f.write(cmd[0]+'\n')
                f.write(cmd[1]+'\n')
            f.close()
        
        

    '''Loads commands from local folder in /batches'''
    def load_cmds(self, filename=None):
        if filename == None:
            filename = input('which file would you like to load? ')
        filename = path.dirname(__file__)+'/batches/'+filename+'.txt'
        with open(filename) as f:
            codes = f.readlines()
            # print(codes)
            for c in range(len(codes)):
                if not c%2:
                    cmd_name = codes[c]
                else:
                    cmd_code = codes[c]
                    self.cmd_list.append((cmd_name, cmd_code))
            f.close()

    def remove_cmd(self, cmd_index=None):
        try:
            cmd_index = int(cmd_index)
            #making sure its within bounds
            if -len(self.cmd_list) <= cmd_index < len(self.cmd_list):
                self.cmd_list.pop(cmd_index)
            return
        except TypeError:
            pass #continue on as if no arg was given

    #Helper methods for the console command writer
    def _ask_for_cmd_key():
        s = input('input name or id# of desired command: ')
        s_key = lookup.catalog_lookup(s, 'commands')
        if s_key > 0:
            return s_key
        else:
            cmdlist_markup = '[green]{}[/green] {}\n[yellow]{}[/yellow]'
            cmdlist_formatstr = [cmdlist_markup.format( x, skyrim_commands[x]['NAME'],
                CommandMaker.__insert_linebreaks(skyrim_commands[x]['DETAILS'], 30)
                ) for x in skyrim_commands]
            panel_pages = [[Panel(x) for x in cmdlist_formatstr[0:35]],
                            [Panel(x) for x in cmdlist_formatstr[35:69]],
                            [Panel(x) for x in cmdlist_formatstr[70:104]],
                            [Panel(x) for x in cmdlist_formatstr[105:]]]
            page_num = 0
            while page_num < 4:
                cmdlist_layout = Columns(panel_pages[page_num])
                print(cmdlist_layout)
                wants_more = input('See more commands? Enter y for yes: ')
                if wants_more.lower() == 'y':
                    page_num += 1
                else:
                    page_num = 5
                    try:
                        #if user inputs the key at this prompt, it gets accepted
                        s_key = int(wants_more)
                    except ValueError: 
                        pass

            while s_key < 0:
                print('Enter name or [green]local ID[/green] of desired command.')
                s = input('\t:')
                s_key = lookup.catalog_lookup(s, 'commands')
            return s_key


    def __insert_linebreaks(_str, width):
        outputstr = ''
        for word in _str.split():
            if len(outputstr.split('\n')[-1]) + len(word) >= width:
                outputstr += '\n'
            outputstr += word+' '
        return outputstr

    def _ask_for_target():
        if input('is the player the target? ').lower() == 'y':
            return 'player'
        else:
            return lookup.user_lookup('npcs')[1]#second entry is the code

    def _ask_for_param(paramIDs):
        params = []
        for p in paramIDs:
            p = p.strip()
            if p == '<item ID>':
                params.append(lookup.user_lookup('items')[1])
            elif p ==  '<perk ID>':
                params.append(lookup.user_lookup('perks')[1])
            elif p ==  '<spell ID>':
                params.append(lookup.user_lookup('spells')[1])
            elif p ==  '<faction ID>':
                params.append(lookup.user_lookup('factions')[1])
            elif p ==  '<target>':
                params.append(lookup.user_lookup('npcs')[1])
            elif p ==  '<skill>':
                params.append(lookup.user_lookup('skills')[0])
            elif p ==  '<quest ID>':
                params.append(lookup.user_lookup('quests')[1])
            elif p ==  '<attribute>':
                params.append(lookup.user_lookup('avs')[0])
            elif p ==  '<0>':
                params.append('0')
            elif p ==  '<1>':
                params.append('1')
            else:
                word = input(p+'? ')
                params.append(word)
        return params

    def __form_cmd(cmdbase, target='', params=None):
        text = ''
        if target != '':
            text += target+'.'
        text += cmdbase+' '#space doesnt harm if theres no parameters after
        if params != None:
            text += ' '.join(params)
        return text

    def generate_layout(self)->Layout:
        # height = get_terminal_size().lines
        width = get_terminal_size().columns
        self.ui = Layout()
        self.ui.split_column(
            Layout(name="DovahPy is a free and open source package.", size=1),
            Layout(name="titlebox", size=3),
            Layout(name='content')
        )
        self.ui['content'].split_row(
            Layout(name='instructions', size=width//3),
            Layout(name='sidebox')
        )
        instructions_list = [
            'Welcome to DovahPy command maker!',
            'input "add" to start building your console command! If you know how youre going to proceed in the program, you can daisy chain the inputs together like so:',
            '"add additem player" will jump to the stage where you search for your desired item.',
            'files will be saved to the standard skyrim directory or a different one if you so choose.',
            '"remove" does not work on its own, it needs to be followed by the [green]local ID[/green] of the command you\'d like to delete.'
        ]
        self.ui['instructions'].update(Panel('\n\n  '.join(instructions_list)))
        self.ui['titlebox'].update(Panel('DovahPy | Console Command Builder'))
        self.update_commands_box()

    def update_commands_box(self):
        if len(self.cmd_list) > 0:
            command_panels = [Panel(self.panel_markdown.format(self.cmd_list.index(x), x[0], x[1])) for x in self.cmd_list]
        else:
            command_panels = [Panel("No commands loaded")]
        self.ui['sidebox'].update(Columns(command_panels))