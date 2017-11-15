import sys, os
sys.path.append(
    os.path.join(os.path.split(os.path.dirname(sys.argv[0]))[0],'kipartman')
)

#TODO: LOOK UP CURRENT DIRECTORY
# sys.argv[0] <fulldirectory>\\<this filename>
#
#
from plugins import plugin_loader
from plugins import export_plugins as export_plugins

print(sys.path)


'''
Gets a file path via popup, then exports content
'''

exporters = plugin_loader.load_export_plugins()

wildcards = '|'.join([x.wildcard for x in exporters])

export_dialog = wx.FileDialog(self, "Export BOM", "", "",
                                wildcards,
                                wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

if export_dialog.ShowModal() == wx.ID_CANCEL:
    pass

base, ext = os.path.splitext(export_dialog.GetPath())
filt_idx = export_dialog.GetFilterIndex()

exporters[filt_idx]().export(base, self.component_type_map)
pass



def testExporters():
    exporters = plugin_loader.load_export_plugins()

    wildcards = '|'.join([x.wildcard for x in exporters])

    export_dialog = wx.FileDialog(self, "Export BOM", "", "",
                                    wildcards,
                                    wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)

    if export_dialog.ShowModal() == wx.ID_CANCEL:
        return

    base, ext = os.path.splitext(export_dialog.GetPath())
    filt_idx = export_dialog.GetFilterIndex()

    exporters[filt_idx]().export(base, self.component_type_map)
    return

testExporters()
