from dialogs.panel_part_preview_data import PanelPartPreviewData
import helper.tree
from configuration import configuration
import os
import wx

class PartPreviewDataFrame(PanelPartPreviewData):
    def __init__(self, parent): 
        super(PartPreviewDataFrame, self).__init__(parent)
        
        self.part = None

    def SetPart(self, part):
        self.part = part
        self.showData()

    def showData(self):
        self.show_symbol()
        self.show_footprint()

    def show_symbol(self):
#         if self.part and self.part.symbol and self.lib_cache.Exists(self.part.symbol.source_path):
#             self.lib_cache.LoadContent(self.part.symbol)
#             lib = kicad_lib_file.KicadLibFile()
#             lib.Load(self.part.symbol.content)
#             image_file = tempfile.NamedTemporaryFile()
#             lib.Render(image_file.name, self.panel_image_symbol.GetRect().width, self.panel_image_symbol.GetRect().height)
#             img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
#             image_file.close()
#         else:
#             img = wx.Image()
#             img.Create(1, 1)
# 
#         img = img.ConvertToBitmap()
#         self.image_symbol.SetBitmap(img)
        pass
    
    def show_footprint(self):
#         if self.part and self.part.footprint and os.path.exists(os.path.join(configuration.kicad_footprints_path, self.part.footprint.source_path)):
#             mod = kicad_mod_file.KicadModFile()
#             mod.LoadFile(os.path.join(configuration.kicad_footprints_path, self.part.footprint.source_path))
#             image_file = tempfile.NamedTemporaryFile()
#             mod.Render(image_file.name, self.panel_image_footprint.GetRect().width, self.panel_image_footprint.GetRect().height)
#             img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
#             image_file.close()
#         else:
#             img = wx.Image()
#             img.Create(1, 1)
# 
#         img = img.ConvertToBitmap()
#         self.image_footprint.SetBitmap(img)
        pass
