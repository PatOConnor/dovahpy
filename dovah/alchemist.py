import numpy as np
import cv2
import pyautogui
import keyboard
import pygetwindow as gw
from time import sleep
from pytesseract import pytesseract as tess
from rich import print
import re
from skyrimdata.skyrimalchemy import ingredients
import alchemycruncher
from webbrowser import open as website_open
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
tess.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def take_screenshot():
    left = 0.14*screensize[0]
    top = 0
    height = screensize[1]
    width = 0.25*screensize[0]
    image = pyautogui.screenshot(region=(left, top, height, width))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite('image.png', image)
    return image

def magnify(window):
    if window == 'skyrimSE':
        win = gw.getWindowsWithTitle('Skyrim Special Edition')[0]
        win.activate()
        #win.maximize()
    elif window == 'shell':
        win = gw.getWindowsWithTitle('Windows PowerShell')[0]
        win.activate()

def scroll(amt,direction):
    for i in range(amt):
        keyboard.press_and_release(direction)
        sleep(0.15)

def read_alchemy_list(inv_list):
    #pattern = re.compile(r"([a-zA-Z]+( [a-zA-Z]+)+) ?(\([0-9]+\))?")
    pattern = re.compile(r"[a-zA-Z ']+(\([0-9]+\))?")
    true_list = []
    sus_list = []
    for item in inv_list:
        if item and item[0] == '`':
            item = item[1::]
        #valid skyrim item
        if pattern.match(item, re.IGNORECASE):
            paren_index = item.find('(')
            if paren_index > 1:
                q = item[paren_index+1:item.find(')'):]
                q = int(q)
                n = item[:paren_index-1:]
            else:
                n = item
                q = 1
            true_list.append([n, q])
    return true_list

def image_to_list(img):
    inv_list = []
    text = tess.image_to_string(img).split('\n')
    #print(len(text),text[0],text[len(text)-1])
    return text

def gather(direction):
    inv_list = []
    img = take_screenshot()
    inv_page = image_to_list(img)
    prev_page = inv_page
    inv_list.extend(inv_page)
    while(True):
        scroll(8,direction)
        sleep(.3)#motion blur
        img = take_screenshot()
        inv_page = image_to_list(img)
        inv_list.extend(inv_page)
        #stops when it goes twice in a row
        if inv_page[0] == prev_page[0]:
            break
        else:
            prev_page = inv_page

    #print('before conversion: ', inv_list)
    inv_list = list(set(inv_list))#remove duplicates
    inv_list.sort()
    #print('after conversion: ', inv_list)
    return inv_list

def filter_inventory(inv_list):
    true_list = []
    sus_list = []
    for item in inv_list:
        for ingr in ingredients:
            if item[0].lower().strip() == ingredients[ingr]['NAME'].lower().strip():
                true_list.append(item)
    for item in inv_list:
        if item not in true_list:
            sus_list.append(item)
    return true_list, sus_list

def ask_user(confirmed_list, sus_list):
    reformed_list = []
    for item in sus_list:
        for gooditem in confirmed_list:
            dupli = False
            commonletters = set(item[0].rstrip(' ')+gooditem[0].rstrip(' '))
            #print(commonletters, gooditem[0], item[0])
            #if it is one character off:
            if len(commonletters)-len(item[0]) < 2:
                dupli = True
                break#continue outer loop on next item
        #ask user if it couldn't tell
        if not dupli and len(item[0]) > 4:
            print(item[0])
            #'tesseract has no idea what its looking at' case
            garb = input('is this garbage input? y/n ')
            if garb.lower() == 'n':
                dup = input('is this item a duplicate of one above? y/n ')
                if dup.lower() == 'n':
                    correct = input('enter the correct name for this item ')
                    reformed_list.append([correct, item[1]])
    return reformed_list

def gather_inventory(final_item):
    i = 0
    magnify('skyrimSE')
    sleep(1)
    final_list = []
    for i in range(2):
        list1 = gather('s')
        scroll(3, 'w')
        list2 = gather('w')
        inv_list = list1
        inv_list.extend(list2)
        inv_list = list(set(inv_list))
        inv_list.sort()
        final_list.extend(inv_list)
    final_list = list(set(final_list))
    final_list.sort()

    final_list.append(final_item)
    final_list = read_alchemy_list(final_list)
    #print(final_list)
    confirmed_ingr, sus_ingr = filter_inventory(final_list)
    print(confirmed_ingr)
    #print(len(final_list), len(confirmed_ingr), len(sus_ingr))
    reformed_ingr = ask_user(confirmed_ingr, (sus_ingr))
    if reformed_ingr:
        confirmed_ingr.extend(reformed_ingr)
    return confirmed_ingr

def write_test_to_file(data):
    print('write method started')
    file = open("alchemy_lists.py", 'a', encoding="utf-8")
    print('write open...')
    file.write('[\n')
    for item in data:  #this writes it in python dictionary syntax
        file.write('[\''+item[0]+'\', '+str(item[1])+'],\n')
    file.write(']\n\n')
    print('write finished')
    file.close()


def run():
    print('Alchemist Engine. Boot Skyrim to top of ingredients section of inventory')
    #final_item = input('what i6s the last item in your inventory?: ')
    #final_item = 'White Cap'
    #inventory = gather_inventory(final_item)
    #print(inventory)
    #write_test_to_file(inventory)
    #alchemycruncher.run(inventory)
    alchemycruncher.run()
    #potions_list = alchemycruncher.crunch(inventory)
    #for p in potions_list:
    #    print(p)



if __name__=="__main__":
    run()
