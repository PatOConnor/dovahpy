from . import getskydata, getalchemy
def run():
    print('which type of data to collect?\n', '1. Most Data\n', '2. Alchemy\n', '3. \n',)
    module_argument = input()
    if module_argument == '1':
        getskydata.run()
    elif module_argument == '2':
        getalchemy.run()
    else:
        pass

if __name__=='__main__':
    run()
