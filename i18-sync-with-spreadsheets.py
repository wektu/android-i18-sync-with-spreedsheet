#!/usr/bin/python
import pygsheets
import sys
import getopt
import pathlib

#used for xm parsing
from xml.dom import minidom
import xml.etree.ElementTree as ET  

#used to print colored in terminal
#from colorama import Fore
#from colorama import Style

#Fix pygsheets not available 
#	pip install pygsheets

#Fix oauth2client not available
#	pip3 install --upgrade oauth2client 

class Item():
	def __init__(self):
		self.name = ''
		self.translatable = True
		self.formatted = False


def main(argv):

	language = ''
	
	try:
		opts, args = getopt.getopt(argv,"hl:",["language="])
	except getopt.GetoptError:
		print("i18-sync.py -l <language>")
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print('i18-sync.py -l <language>')
			sys.exit()
		elif opt in ("-l", "--language"):
			language = arg

	language = language.replace(' ','')
	
	print ('Language is ', language.upper())
	
	worksheet = open_worksheet_for_language(language)

	items_worksheet = get_items_from_worksheet(worksheet)
	
	# open the android strings folder for english in order to iterate all items


	"""
	### region using minidom ###

	# parse an xml file by name
	mydoc = minidom.parse('./values/strings.xml')

	items = mydoc.getElementsByTagName('string')

	# total amount of items
	print("Read " + len(items) + " items")  

	# all item attributes
	print ('\nAll attributes and their data')  
	for elem in items:  
		key = elem.attributes['name'].value
		value = elem.firstChild.data
		print (key + " -> " + value)
	"""

	### region using ElementTree ###
	items_en = get_xml_items_for_language("en")

	items_lang = get_xml_items_for_language(language)

	keys_a = set(items_en.keys())
	keys_b = set(items_lang.keys())

	#union = dict(items_en.items() | items_lang.items())
 	
	translated_keys = keys_a & keys_b # '&' operator is used for set intersection
	
	not_translated_keys = keys_a ^ keys_b

	print ("Found %d words that needs to be checked", len(translated_keys))
	print ("Found %d words not translated", len(not_translated_keys))


def get_xml_items_for_language(lang):
	list = {} 
	# add the language and - only if not the default english language
	file = "/values" + ("" if lang == "en" else "-" + lang) +"/strings.xml"
	pathlib.Path(file).mkdir(parents=True, exist_ok=True)
	with open(file, "w") as f:
		print ("oppened")

	xml_path = 	"." + file

	tree = ET.parse(xml_path)
	root = tree.getroot()

	# all item attributes
	print('\nAll attributes:')  
	for elem in root: 
		item = Item()
		for attrib in elem.attrib:
			val = elem.text
			if attrib == "name":
				item.name = val
			elif attrib == "translatable":
				item.translatable = val
			else:
				item.formatted = val
		
		list[item.name] = item

	print ("Added %d items", len(list))

	return list


def open_worksheet_for_language(language):
	gc = pygsheets.authorize(outh_file='client_secret.json')

	# You can open a spreadsheet by its title as it appears in Google Docs 
	sheet_name = "LINX translation"
	try:
		sh = gc.open(sheet_name)
	except pygsheets.SpreadsheetNotFound:
		print("Spreadsheet " + language + "not available")
		sh = gc.create(sheet_name)			
			
	try:
		sh = gc.open(sheet_name)
	except pygsheets.SpreadsheetNotFound:
		print("Unable to create the spreadsheet :(")
		sys.exit()

	print (sheet_name + ' was successfully opened')

	try:
		worksheet_lang = sh.worksheet_by_title(language)
	except pygsheets.WorksheetNotFound:
		# create a new sheet with 50 rows and 60 colums
		worksheet_lang = sh.add_worksheet(language,rows=500,cols=3)
		print ("Worksheet for language " + language.upper() + ' was successfully created')
	
	print ("Worksheet for language " + language.upper() + ' was successfully oppened')


	return worksheet_lang


def get_items_from_worksheet(worksheet):
	list = {}
	# Get all values of sheet as 2d list of cells
	cell_matrix = worksheet.get_all_values(returnas='matrix')

	# Get values as 2d array('matrix') which can easily be converted to an numpy aray or as 'cell' list
	values_mat = worksheet.get_values(start=(1,1), end=(len(cell_matrix),3), returnas='matrix')



	return list


def get_spreadsheet(lan):
	list = {}

	return list

if __name__ == "__main__":
   main(sys.argv[1:])



