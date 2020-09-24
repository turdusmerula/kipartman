from dialogs.panel_edit_footprint import PanelEditFootprint
from frames.dropdown_dialog import DropdownDialog
import wx.lib.newevent
from helper.exception import print_stack
from helper.log import log
from helper import colors
import os
from kicad.kicad_file_manager_footprints import KicadFootprintLibraryManager

EditFootprintApplyEvent, EVT_EDIT_FOOTPRINT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditFootprintCancelEvent, EVT_EDIT_FOOTPRINT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

none_image = os.path.abspath(os.path.join('resources', 'none-128x128.png'))

def NoneValue(value, default):
    if value:
        return value
    return default

class EditFootprintFrame(PanelEditFootprint): 
    def __init__(self, parent):
        super(EditFootprintFrame, self).__init__(parent)
        
        # set initial state
        self.SetFootprint(None)
        self._enable(False)
        
    def SetFootprint(self, footprint):
        self.footprint = footprint
        self._show_footprint(footprint)
        self._enable(False)
        self._check()

    def EditFootprint(self, footprint):
        self.footprint = footprint
        self._show_footprint(footprint)
        self._enable(True)
        self._check()

    def _show_footprint(self, footprint):
        # enable everything else
        if footprint is not None:
            
            self.edit_footprint_name.Value = footprint.Name
            
#             if self.edit_footprint_name.Value!='' and os.path.exists(os.path.join(configuration.kicad_footprints_path, footprint.source_path)):
#                 mod = kicad_mod_file.KicadModFile()
#                 mod.LoadFile(os.path.join(configuration.kicad_footprints_path, footprint.source_path))
#                 image_file = tempfile.NamedTemporaryFile()
#                 mod.Render(image_file.name, self.panel_image_footprint.GetRect().width, self.panel_image_footprint.GetRect().height)
#                 img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
#                 image_file.close()
#             else:
#                 img = wx.Image()
#                 img.Create(1, 1)
# 
#             img = img.ConvertToBitmap()
#             self.bitmap_edit_footprint.SetBitmap(img)
                
        else:
            self.edit_footprint_name.Value = ''

#             img = wx.Image()
#             img.Create(1, 1)
#             img = img.ConvertToBitmap()
#             self.bitmap_edit_footprint.SetBitmap(img)

    def _enable(self, enabled=True):
        self.edit_footprint_name.Enabled = enabled
        self.button_footprint_editApply.Enabled = enabled
        self.button_footprint_editCancel.Enabled = enabled
        
    def _check(self):
        error = False

        if self.edit_footprint_name.Value=="":
            self.edit_footprint_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_footprint_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        if error:
            self.button_footprint_editApply.Enabled = False
        else:
            self.button_footprint_editApply.Enabled = True
                        

    def onButtonFootprintEditApply( self, event ):
        if self.edit_footprint_name.Value!=self.footprint.Name:
            KicadFootprintLibraryManager.RenameFootprint(self.footprint, self.edit_footprint_name.Value)

        wx.PostEvent(self, EditFootprintApplyEvent(data=self.footprint))
        event.Skip()
    
    def onButtonFootprintEditCancel( self, event ):
        wx.PostEvent(self, EditFootprintCancelEvent())
        event.Skip()

    def onTextEditFootprintNameText( self, event ):
        self._check()
        event.Skip()
