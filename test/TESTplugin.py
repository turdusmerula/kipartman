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
from plugins import export_plugins as export_plugins
from plugins import import_plugins as export_plugins


# RETRIEVE the find_parts

import rest
query_filter = {'search': u'resistor'}
parts = rest.api.find_parts(**query_filter)
len(parts)
[key for key in parts[0].swagger_types.viewkeys()]
parts[0].swagger_types.viewvalues()
[parts[0].to_dict()[key] for key in parts[0].swagger_types.viewkeys()]

parts[0].to_dict()['name']
parts[0].name

dir(parts[0].swagger_types)

parts[0].swagger_types.viewkeys()



'''
Gets a file path via popup, then exports content
'''

exporters = plugin_loader.load_export_plugins()
importers = plugin_loader.load_import_plugins()
wildcards = '|'.join([x.wildcard for x in exporters])
wildcards
exporters[0]

exportpath=os.path.join(os.getcwd(),'test','TESTexportCSV.csv')
exportpath
base, ext = os.path.splitext(exportpath)
exporters[0]().export(base, parts)

# export_dialog = wx.FileDialog(self, "Export BOM", "", "",
#                                 wildcards,
#                                 wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

# if export_dialog.ShowModal() == wx.ID_CANCEL:
#     pass

# base, ext = os.path.splitext(export_dialog.GetPath())
# filt_idx = export_dialog.GetFilterIndex()

# exporters[filt_idx]().export(base, self.component_type_map)
# pass



# def testExporters():
#     exporters = plugin_loader.load_export_plugins()

#     wildcards = '|'.join([x.wildcard for x in exporters])

#     export_dialog = wx.FileDialog(self, "Export BOM", "", "",
#                                     wildcards,
#                                     wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

#     if export_dialog.ShowModal() == wx.ID_CANCEL:
#         return

#     base, ext = os.path.splitext(export_dialog.GetPath())
#     filt_idx = export_dialog.GetFilterIndex()

#     exporters[filt_idx]().export(base, self.component_type_map)
#     return

# testExporters()
