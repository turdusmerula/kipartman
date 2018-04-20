from dialogs.panel_edit_symbol import PanelEditSymbol
from frames.select_snapeda_frame import SelectSnapedaFrame, EVT_SELECT_SNAPEDA_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from kicad import kicad_lib_file
import wx.lib.newevent
import tempfile
import os.path
import webbrowser
import cfscrape
from configuration import Configuration
from dialogs.dialog_snapeda_error import DialogSnapedaError
from snapeda.queries import DownloadQuery
import zipfile
import glob
import datetime
import hashlib
import json
from kicad.kicad_file_manager import KicadLibCache, KicadFileManagerLib

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
    if metadata.has_key(value):
        return metadata[value]
    return default

class EditSymbolFrame(PanelEditSymbol): 
    def __init__(self, parent):
        super(EditSymbolFrame, self).__init__(parent)
        self.snapeda_uid = ''
        self.symbol_path = ''
        self.lib_cache = KicadFileManagerLib()
        
    def SetSymbol(self, symbol):
        self.symbol = symbol
        self.ShowSymbol(symbol)

    def ShowSymbol(self, symbol):
        configuration = Configuration()
            
        # enable everything else
        if symbol:
            
            if symbol.metadata:
                metadata = json.loads(symbol.metadata)
            else:
                metadata = json.loads('{}')

            self.edit_symbol_name.Value = ''
            self.symbol_path = ''
            
            if NoneValue(symbol.source_path, '')!='':
                name = os.path.basename(NoneValue(symbol.source_path, ''))
                if name.endswith('.lib')==False:
                    # path is a symbol
                    self.edit_symbol_name.Value = name.replace(".mod", "")
                    self.symbol_path = os.path.dirname(symbol.source_path)
                    
            self.edit_symbol_description.Value = MetadataValue(metadata, 'description', '')
            self.edit_symbol_comment.Value = MetadataValue(metadata, 'comment', '')
             
            self.button_open_url_snapeda.Label = MetadataValue(metadata, 'snapeda', '<None>')
            
            if self.edit_symbol_name.Value!='' and self.lib_cache.Exists(symbol.source_path):
                self.lib_cache.LoadContent(symbol)
                lib = kicad_lib_file.KicadLibFile()
                lib.Load(symbol.content)
                image_file = tempfile.NamedTemporaryFile()
                lib.Render(image_file.name, self.panel_image_symbol.GetRect().width, self.panel_image_symbol.GetRect().height)
                img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                image_file.close()
            else:
                img = wx.Image()
                img.Create(1, 1)

            img = img.ConvertToBitmap()
            self.bitmap_edit_symbol.SetBitmap(img)
                
        else:
            self.edit_symbol_name.Value = ''
            self.edit_symbol_description.Value = ''
            self.edit_symbol_comment.Value = ''
            self.button_open_url_snapeda.Label = "<None>"

            img = wx.Image()
            img.Create(1, 1)
            img = img.ConvertToBitmap()
            self.bitmap_edit_symbol.SetBitmap(img)


        
    def enable(self, enabled=True):
        self.edit_symbol_name.Enabled = enabled
        self.edit_symbol_description.Enabled = enabled
        self.edit_symbol_comment.Enabled = enabled
        self.button_remove_url_snapeda.Enabled = enabled
        self.button_symbol_editApply.Enabled = enabled
        self.button_symbol_editCancel.Enabled = enabled
        self.button_snapeda.Enabled = enabled
        
    def onButtonSnapedaClick( self, event ):
        # create a snapeda frame
        # dropdown frame
        dropdown = DropdownDialog(self.button_snapeda, SelectSnapedaFrame, initial_search=self.edit_symbol_name.Value, preview='symbol')
        dropdown.panel.Bind( EVT_SELECT_SNAPEDA_OK_EVENT, self.onSelectSnapedaFrameOk )
        dropdown.Dropdown()

    def onSelectSnapedaFrameOk(self, event):
        snapeda = event.data
        if not snapeda:
            return
        print snapeda.json
        
        self.edit_symbol_name.Value = snapeda.part_number()
        self.edit_symbol_description.Value = snapeda.short_description()
        self.snapeda_uid = snapeda.uniqueid()
        
        try:
            download = DownloadQuery()
            download.get(part_number=snapeda.part_number(), 
                               manufacturer=snapeda.manufacturer(),
                               uniqueid=snapeda.uniqueid(),
                               has_symbol='True',
                               has_footprint='False')
            if download.error():
                wx.MessageBox(download.error(), 'Error downloading symbol', wx.OK | wx.ICON_ERROR)
                
        except:
            DialogSnapedaError(self).ShowModal()
            return
        
        self.button_open_url_snapeda.Label = "https://www.snapeda.com"+snapeda._links().self().href()

        # download symbol
        if download.url() and download.url()!='':
            try:
                filename = os.path.join(tempfile.gettempdir(), os.path.basename(download.url()))
                print "Download from:", download.url()
                content = scraper.get(download.url()).content
                with open(filename, 'wb') as outfile:
                    outfile.write(content)
                outfile.close()
            except :
                wx.MessageBox(download.url(), 'Error loading symbol', wx.OK | wx.ICON_ERROR)
                return
                
            # unzip file
            try:
                zip_ref = zipfile.ZipFile(filename, 'r')
                zip_ref.extractall(filename+".tmp")
                zip_ref.close()
            except Exception as e:
                wx.MessageBox(format(e), 'Error unziping symbol', wx.OK | wx.ICON_ERROR)

            self.symbol.content = ''
            for file in glob.glob(filename+".tmp/*"):
                if file.endswith(".lib"):
                    print "---------", file
                    lib = KicadLibCache(filename+".tmp")
                    symbols = lib.read_lib_file(os.path.basename(file))
                    if len(symbols)>0:
                        for symbol in symbols:
                            self.symbol.content = symbols[symbol].content
                            break
                    print "****", self.symbol.content
                    
                    mod = kicad_lib_file.KicadLibFile()
                    mod.LoadFile(file)
                    image_file = tempfile.NamedTemporaryFile()
                    mod.Render(image_file.name, self.panel_image_symbol.GetRect().width, self.panel_image_symbol.GetRect().height)
                    img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                    image_file.close()
                    img = img.ConvertToBitmap()
                    self.bitmap_edit_symbol.SetBitmap(img)
            
            self.symbol.md5 = hashlib.md5(self.symbol.content).hexdigest()

        # download 3D symbol
        #TODO
                        
    def onButtonOpenUrlSnapedaClick( self, event ):
        if self.button_open_url_snapeda.Label!="<None>":
            webbrowser.open(self.button_open_url_snapeda.Label)
    
    def onButtonRemoveUrlSnapedaClick( self, event ):
        self.button_open_url_snapeda.Label = "<None>"
        self.button_open_url_snapeda = ''

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
            symbol.md5 = hashlib.md5(symbol.content).hexdigest()
            
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
