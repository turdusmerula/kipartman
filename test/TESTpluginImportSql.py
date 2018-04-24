import sys, os



#TODO: LOOK UP CURRENT DIRECTORY
# sys.argv[0] <fulldirectory>\\<this filename> in ipython does not describe this filename
# so use os.getcwd
# For this TEST just add both possible paths to the necessary imports
#
#
sys.path.append(
    os.path.join(os.path.split(os.path.dirname(sys.argv[0]))[0],'kipartman'))
sys.path.append(os.path.join(os.getcwd(),'kipartman'))

print(sys.path)



from plugins import plugin_loader
from plugins import import_plugins as import_plugins


# RETRIEVE the find_parts

import rest




'''
Gets a file path via popup, then imports content
'''


importers = plugin_loader.load_import_plugins()
wildcards = '|'.join([x.wildcard for x in importers])
wildcards
importers[0]

importpath=os.path.join(os.getcwd(),'test','TESTimportCSV.csv')
importpath
base, ext = os.path.splitext(importpath)

thecategory = eval(u"{'childs': None,\n 'description': '',\n 'id': 4,\n 'name': 'Test',\n 'parent': {'id': 1},\n 'path': '/Resistor/Test'}")
# 1: For sqldb 0: for CsvImport
importItems = importers[1]().fetch(base, thecategory,  rest.model)
