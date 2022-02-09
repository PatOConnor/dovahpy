import numpy as np
import cv2
import pyautogui
import keyboard
import pygetwindow as gw
from time import sleep

def take_screenshot(filename):
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite('alchemy_images/'+filename+'.png', image)

def magnify_skyrim():
    win = gw.getWindowsWithTitle('Skyrim Special Edition')[0]
    win.activate()

def scroll_down(amt):
    for i in range(amt):
        keyboard.send('s')
        sleep(0.25)

def gather_inventory():
    i = 0
    magnify_skyrim()
    sleep(3)
    take_screenshot('alch_'+str(i))
    scroll_down(8)#crop the top of the inventory
    inv_list = image_to_list()#first image of inventory
    while(True):
        i += 1
        take_screenshot('alch_'+str(i)  )
        scroll_down(16)
        inv_page = image_to_list()
        #if it hasn't gotten to the end of the list
        #if inv_page[-1] != inv_list[-1]:      <=actual condition
        if i < 5:
            inv_list.extend(inv_page)
        else:
            break
    inv_list = list(set(inv_list))#remove duplicates

def image_to_list():
    return [1,2]

def crunch_inventory(inv_list):
    pass

def run():
    print('Alchemist Engine. Boot Skyrim to inventory menu and press any key.')
    input()
    ingredients = gather_inventory()
    potions_list = crunch_inventory(ingredients)
    for p in potions_list:
        print(p, potions_list[p])

if __name__=="__main__":
    run()
