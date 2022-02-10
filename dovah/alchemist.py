import numpy as np
import cv2
import pyautogui
import keyboard
import pygetwindow as gw
from time import sleep
from pytesseract import pytesseract as tess
tess.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)



def take_screenshot():
    left = 0.14*screensize[0]
    top = 0
    height = screensize[1]
    width = 0.3*screensize[0]
    image = pyautogui.screenshot(region=(left, top, height, width))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite('image.png', image)
    return image

def magnify_skyrim():
    win = gw.getWindowsWithTitle('Skyrim Special Edition')[0]
    win.activate()
    #win.maximize()

def scroll_down(amt):
    for i in range(amt):
        keyboard.press_and_release('s')
        sleep(0.25)

def filter_misreads(text):

def image_to_list(img):
    inv_list = []
    text = tess.image_to_string(img).split('\n')
    #text = filter_misreads(text)
    print(len(text),text[0],text[len(text)-1])
    return [1,2]

def gather_inventory():
    i = 0
    magnify_skyrim()
    sleep(1)
    scroll_down(9)#crop the top of the inventory
    while(True):
        inv_list = []
        img = take_screenshot()
        scroll_down(16)
        inv_page = image_to_list(img)
        inv_list.extend(inv_page)
        #if it hasn't gotten to the end of the list
        #if inv_page[-1] != inv_list[-1]:      <=actual condition
        i += 1
        if i == 3:
            break
    inv_list = list(set(inv_list))#remove duplicates


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
