from bs4 import BeautifulSoup
from urllib.request import urlopen
from string import ascii_uppercase

################################
# program uses beautiful soup to access website, get tables, format them into
# usable data and save to file 
################################

def scrape_page(url_string):
	url = url_string
	my_table = []
	my_list = []
	try:
		page = urlopen(url)
	except:
		print("error opening URL")
		return
	soup = BeautifulSoup(page, 'html.parser')
	
	#need to write a searcher that gets all the like tables
	#and sorts the lefthand one into a dictionary of tuples
	
	content = soup.find_all('table', {"class": "wikitable"})	
	for table in content:
		rows = table.find_all('tr')
		#row has three objects which may or may not have a th. those are the ones i want
		for data in rows:
			for items in data.children:
				if items.th.string == 'Editor ID' or items.td.string == 'Form ID':
					my_list.append(items)
			my_table.append(tuple(my_list))
			my_list.clear()
	
	
	return my_table

#this writes the data to the file of the associated category
def write_to_file(category, data):
	file = open("skydata/skyrim"+category+".py", "w")
	i = 0
	file.write('skyrim_'+category+' = {\n')
	for item in data:
		file.write('\t'+str(i)+':'+str(item)+',\n')
		i += 1
	file.write('\t}')
	file.close()

#returns massive dictionary of all the data of a given category
def scrape_all():
	main_url = 'https://en.uesp.net/wiki/Skyrim:Factions_'
	value_table = list()
	for c in ascii_uppercase:
		print(main_url+c)
		value_table.append(scrape_page(main_url+c))
	return value_table	
	

if __name__=="__main__":
	print('######################################\n',
		'#\t\tSkyrim Data Scraper\n',
		'#\t\tFor use with Command Batcher\n',
		'#\t\tFaction ID scraper'
		'#\tBy Pat O\'Connor\n',
		'#\tData Courtesy of UESP\n')
	word = input('enter y to continue: ')
	if word == 'y':
		write_to_file('factions', scrape_all())