from dialogs.panel_edit_symbol import PanelEditSymbol
from frames.dropdown_dialog import DropdownDialog
import wx.lib.newevent
from helper.exception import print_stack
from helper.log import log
from helper import colors
import os
from kicad.kicad_file_manager_symbols import KicadSymbolLibraryManager, KicadSymbolFile, KicadSymbol

EditSymbolApplyEvent, EVT_EDIT_SYMBOL_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditSymbolCancelEvent, EVT_EDIT_SYMBOL_CANCEL_EVENT = wx.lib.newevent.NewEvent()

none_image = os.path.abspath(os.path.join('resources', 'none-128x128.png'))

class EditSymbolFrame(PanelEditSymbol): 
    def __init__(self, parent):
        super(EditSymbolFrame, self).__init__(parent)
        
        # set initial state
        self.SetSymbol(None)
        self._enable(False)
        
    def SetSymbol(self, symbol):
        self.symbol = symbol
        
        self._show_symbol(symbol)
        self._enable(False)
        self._check()

    def EditSymbol(self, symbol):
        self.symbol = symbol
        
        self._show_symbol(symbol)
        self._enable(True)
        self._check()

    def AddSymbol(self, library):
        self.library = library
        self.symbol = None
        
        self._show_symbol(self.symbol)
        self._enable(True)
        self._check()

    def _show_symbol(self, symbol):
        # enable everything else
        if symbol is not None:

            self.edit_symbol_name.Value = symbol.Name
            self.edit_symbol_description.Value = symbol.Description
            
#             self.button_open_url_snapeda.Label = MetadataValue(metadata, 'snapeda', '<None>')
#             
#             if symbol.Content!='':
#                 lib = kicad_lib_file.KicadLibFile()
#                 lib.Load(symbol.Content)
#                 image_file = tempfile.NamedTemporaryFile()
#                 lib.Render(image_file.name, self.panel_image_symbol.GetRect().width, self.panel_image_symbol.GetRect().height)
#                 img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
#                 image_file.close()
#             else:
#                 img = wx.Image()
#                 img.Create(1, 1)
#  
#             img = img.ConvertToBitmap()
#             self.bitmap_edit_symbol.SetBitmap(img)
#                 
        else:
            self.edit_symbol_name.Value = ''
            self.edit_symbol_description.Value = ''

#             img = wx.Image()
#             img.Create(1, 1)
#             img = img.ConvertToBitmap()
#             self.bitmap_edit_symbol.SetBitmap(img)

    def _enable(self, enabled=True):
        self.edit_symbol_name.Enabled = enabled
        self.edit_symbol_description.Enabled = enabled
        self.button_symbol_editApply.Enabled = enabled
        self.button_symbol_editCancel.Enabled = enabled

    def _check(self):
        error = False
        
        if self.edit_symbol_name.Value=="":
            self.edit_symbol_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_symbol_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if error:
            self.button_symbol_editApply.Enabled = False
        else:
            self.button_symbol_editApply.Enabled = self.button_symbol_editCancel.Enabled
    
    def onButtonSymbolEditApply( self, event ):
        try:
            if self.symbol is None:
                self.symbol = KicadSymbolLibraryManager.CreateSymbol(self.library, self.edit_symbol_name.Value)
            else:
                KicadSymbolLibraryManager.RenameSymbol(self.symbol, self.edit_symbol_name.Value)
            
            wx.PostEvent(self, EditSymbolApplyEvent(data=self.symbol))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)

        event.Skip()
    
    def onButtonSymbolEditCancel( self, event ):
        wx.PostEvent(self, EditSymbolCancelEvent())

    def onTextEditSymbolNameText( self, event ):
        self._check()
        event.Skip()

    def onTextEditSymbolDescriptionText( self, event ):
        self._check()
        event.Skip()
