from dialogs.panel_edit_symbol import PanelEditSymbol
from frames.select_snapeda_frame import SelectSnapedaFrame, EVT_SELECT_SNAPEDA_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from kicad import kicad_lib_file
import wx.lib.newevent
import tempfile
import os.path
import webbrowser
import cfscrape
from configuration import configuration
from dialogs.dialog_snapeda_error import DialogSnapedaError
from snapeda.queries import DownloadQuery
import zipfile
import glob
import datetime
import json
from helper.exception import print_stack
from helper.log import log
from helper import colors

EditSymbolApplyEvent, EVT_EDIT_SYMBOL_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditSymbolCancelEvent, EVT_EDIT_SYMBOL_CANCEL_EVENT = wx.lib.newevent.NewEvent()

scraper = cfscrape.create_scraper()

none_image = os.path.abspath(os.path.join('resources', 'none-128x128.png'))

def NoneValue(value, default):
    if value:
        return value
    return default

def MetadataValue(metadata, value, default):
    if metadata is None:
        return default
    if value in metadata:
        return metadata[value]
    return default

class EditSymbolFrame(PanelEditSymbol): 
    def __init__(self, parent):
        super(EditSymbolFrame, self).__init__(parent)
        self.snapeda_uid = ''
        self.symbol_path = ''
        
        # set initial state
        self.SetSymbol(None)
        self._enable(False)
        
    def SetSymbol(self, symbol):
        self.symbol = symbol
        self._show_symbol(symbol)
        self._enable(False)

    def EditSymbol(self, symbol):
        self.symbol = symbol
        self._show_symbol(symbol)
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
            self.button_open_url_snapeda.Label = "<None>"

#             img = wx.Image()
#             img.Create(1, 1)
#             img = img.ConvertToBitmap()
#             self.bitmap_edit_symbol.SetBitmap(img)

    def _enable(self, enabled=True):
        self.edit_symbol_name.Enabled = enabled
        self.edit_symbol_description.Enabled = enabled
        self.button_remove_url_snapeda.Enabled = enabled
        self.button_symbol_editApply.Enabled = enabled
        self.button_symbol_editCancel.Enabled = enabled
        self.button_snapeda.Enabled = enabled

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
            self.button_symbol_editApply.Enabled = True
    
    def onButtonSymbolEditApply( self, event ):
        symbol = self.symbol
        
        if symbol.metadata:
            metadata = json.loads(symbol.metadata)
        else:
            metadata = json.loads('{}')
        metadata['description'] = self.edit_symbol_description.Value
        metadata['comment'] = self.edit_symbol_comment.Value
        
        if self.button_open_url_snapeda.Label!="<None>":
            metadata['snapeda'] = self.button_open_url_snapeda.Label
            metadata['snapeda_uid'] = self.snapeda_uid
            metadata['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            metadata.pop('snapeda', '')
            metadata.pop('snapeda_uid', '')
            metadata.pop('updated', '')
        
        symbol.metadata = json.dumps(metadata)
        if not symbol.content:
            symbol.content = ''
            symbol.md5 = hash.md5(symbol.content).hexdigest()
            
        # send result event
        event = EditSymbolApplyEvent(
            data=symbol,
            # source_path is not changed in the symbol as we only have the filename here, not the full path
            # the full path should be reconstructed by caller
            symbol_name=self.edit_symbol_name.Value+".mod"
            )
        wx.PostEvent(self, event)
    
    def onButtonSymbolEditCancel( self, event ):
        event = EditSymbolCancelEvent()
        wx.PostEvent(self, event)
    
    def onTextEditSymbolNameText( self, event ):
#         self.symbol.symbol_file.
        event.Skip()

    def onTextEditSymbolDescriptionText( self, event ):
        event.Skip()
