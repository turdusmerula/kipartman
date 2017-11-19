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

query_filter = {'search': u'resistor'}
importItems = rest.api.find_parts(**query_filter)
len(importItems)
[key for key in importItems[0].swagger_types.viewkeys()]
importItems[0].swagger_types.viewvalues()
[importItems[0].to_dict()[key] for key in importItems[0].swagger_types.viewkeys()]

importItems[0].to_dict()['name']
importItems[0].name

dir(importItems[0].swagger_types)

importItems[0].swagger_types.viewkeys()



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
#CSV
#importers[0]().import(base, parts)
#SQL

importItems = importers[1]().fetch(base, importItem  = rest.model)


for importItem in importItems:

    part = rest.model.PartNew()
    #SET imported Parts Fields
    
    part.name = importItem['name']
    part.description = importItem['description']
    part.comment  = 'NEW IMPORT Timestamp:{:%y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())
    self.edit_state='import'
    
    # set category
    # item = self.tree_categories.GetSelection()
    if item.IsOk():
        # category = self.tree_categories_manager.ItemToObject(item)
        if category.category:
            part.category = category.category
    #Update edit_part panel
    self.edit_part(part)
    #Update progress indicator
    #TODO: Import Progress Indicator

    try:
        if self.edit_state=='edit':
            # update part on server
            part = rest.api.update_part(part.id, part)
            # self.tree_parts_manager.UpdatePart(part)
        elif self.edit_state=='import':
            
            part = rest.api.add_part(part)
            # self.tree_parts_manager.AppendPart(part)
    except Exception as e:
        # wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        pass
        #return
#TODO : uncomment these
# self.edit_state = None
# self.show_part(part)

# import_dialog = wx.FileDialog(self, "import BOM", "", "",
#                                 wildcards,
#                                 wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

# if import_dialog.ShowModal() == wx.ID_CANCEL:
#     pass

# base, ext = os.path.splitext(import_dialog.GetPath())
# filt_idx = import_dialog.GetFilterIndex()

# importers[filt_idx]().import(base, self.component_type_map)
# pass



# def testimporters():
#     importers = plugin_loader.load_import_plugins()

#     wildcards = '|'.join([x.wildcard for x in importers])

#     import_dialog = wx.FileDialog(self, "import BOM", "", "",
#                                     wildcards,
#                                     wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

#     if import_dialog.ShowModal() == wx.ID_CANCEL:
#         return

#     base, ext = os.path.splitext(import_dialog.GetPath())
#     filt_idx = import_dialog.GetFilterIndex()

#     importers[filt_idx]().import(base, self.component_type_map)
#     return

# testimporters()
