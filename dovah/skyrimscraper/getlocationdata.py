from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen
import os
from rich import print
from .writetofile import write_to_file

def run(is_test=True):
    url = 'https://elderscrolls.fandom.com/wiki/Console_Commands_(Skyrim)/Locations'
    locations = scrape_page(url)
    # print(locations)
    write_to_file('locations', locations, is_test)

def scrape_page(url_string):
    locations = []
    try:
        page = urlopen(url_string)
    except:
        print("error opening URL")
        return
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('tr')
    for row in rows[1:-7]:#remove infobars at top and bottom
        location_name = row.contents[1].text
        if str(location_name).strip() == 'Name': continue
        location_name = location_name.replace('\n','')
        sublocations = row.contents[3]
        if len(sublocations.contents) == 1:
            location_code = sublocations.text
            location_code = location_code.replace('\n','')
            locations.append({'NAME':location_name, 'CODE':location_code})
        else:
            #get all even-numbered entries as a separate file
            for loc in sublocations.contents[::2]:
                location_code = str(loc)
                location_code = location_code.replace('\n','')
                locations.append({'NAME':location_name, 'CODE':location_code})
    return locations

if __name__ == '__main__':
    run()
