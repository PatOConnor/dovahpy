from . import getskydata, getalchemy, getalcheffects
def run(param=None):
    print(param)
    if not param:
        print('which type of data to collect?\n', '1. Most Data\n', '2. Alchemy Ingredients\n', '3. Alchemy Effects\n',)
        module_argument = input().lower().strip()
    else:
        module_argument = param[0]
        print( module_argument)
        param = None

    if module_argument in ['1', 'm']:
        getskydata.run()
    elif module_argument in ['2', 'a']:
        getalchemy.run()
    elif module_argument in ['3', 'e']:
        getalcheffects.run()


if __name__=='__main__':
    run()
