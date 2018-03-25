from dialogs.panel_edit_model_proto import PanelEditModelProto
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
from kicad.kicad_file_manager import KicadFileManagerLib

EditModelApplyEvent, EVT_EDIT_FOOTPRINT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditModelCancelEvent, EVT_EDIT_FOOTPRINT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

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

class EditModelFrameProto(PanelEditModelProto): 
    def __init__(self, parent):
        super(EditModelFrameProto, self).__init__(parent)
        self.snapeda_uid = ''
        self.model_path = ''
        self.lib_cache = KicadFileManagerLib()
        
    def SetModel(self, model):
        self.model = model
        self.ShowModel(model)

    def ShowModel(self, model):
        configuration = Configuration()
            
        # enable everything else
        if model:
            
            if model.metadata:
                metadata = json.loads(model.metadata)
            else:
                metadata = json.loads('{}')

            self.edit_model_name.Value = ''
            self.model_path = ''
            
            if NoneValue(model.source_path, '')!='':
                name = os.path.basename(NoneValue(model.source_path, ''))
                if name.endswith('.lib')==False:
                    # path is a model
                    self.edit_model_name.Value = name.replace(".mod", "")
                    self.model_path = os.path.dirname(model.source_path)
                    
            self.edit_model_description.Value = MetadataValue(metadata, 'description', '')
            self.edit_model_comment.Value = MetadataValue(metadata, 'comment', '')
             
            self.button_open_url_snapeda.Label = MetadataValue(metadata, 'snapeda', '<None>')
            
            if self.edit_model_name.Value!='' and self.lib_cache.Exists(model.source_path):
                self.lib_cache.LoadContent(model)
                lib = kicad_lib_file.KicadLibFile()
                lib.Load(model.content)
                image_file = tempfile.NamedTemporaryFile()
                lib.Render(image_file.name, self.panel_image_model.GetRect().width, self.panel_image_model.GetRect().height)
                img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                image_file.close()
            else:
                img = wx.Image()
                img.Create(1, 1)

            img = img.ConvertToBitmap()
            self.bitmap_edit_model.SetBitmap(img)
                
        else:
            self.edit_model_name.Value = ''
            self.edit_model_description.Value = ''
            self.edit_model_comment.Value = ''
            self.button_open_url_snapeda.Label = "<None>"

            img = wx.Image()
            img.Create(1, 1)
            img = img.ConvertToBitmap()
            self.bitmap_edit_model.SetBitmap(img)


        
    def enable(self, enabled=True):
        self.edit_model_name.Enabled = enabled
        self.edit_model_description.Enabled = enabled
        self.edit_model_comment.Enabled = enabled
        self.button_remove_url_snapeda.Enabled = enabled
        self.button_model_editApply.Enabled = enabled
        self.button_model_editCancel.Enabled = enabled
        self.button_snapeda.Enabled = enabled
        
    def onButtonSnapedaClick( self, event ):
        # create a snapeda frame
        # dropdown frame
        dropdown = DropdownDialog(self.button_snapeda, SelectSnapedaFrame, initial_search=self.edit_model_name.Value, preview='model')
        dropdown.panel.Bind( EVT_SELECT_SNAPEDA_OK_EVENT, self.onSelectSnapedaFrameOk )
        dropdown.Dropdown()

    def onSelectSnapedaFrameOk(self, event):
        snapeda = event.data
        if not snapeda:
            return
        print snapeda.json
        
        self.edit_model_name.Value = snapeda.part_number()
        self.edit_model_description.Value = snapeda.short_description()
        self.snapeda_uid = snapeda.uniqueid()
        
        try:
            download = DownloadQuery()
            download.get(part_number=snapeda.part_number(), 
                               manufacturer=snapeda.manufacturer(),
                               uniqueid=snapeda.uniqueid(),
                               has_symbol=snapeda.has_symbol(),
                               has_model=snapeda.has_model())
            if download.error():
                wx.MessageBox(download.error(), 'Error downloading model', wx.OK | wx.ICON_ERROR)
                
        except:
            DialogSnapedaError(self).ShowModal()
            return
        
        self.button_open_url_snapeda.Label = "https://www.snapeda.com"+snapeda._links().self().href()

        # download model
        if download.url() and download.url()!='':
            try:
                filename = os.path.join(tempfile.gettempdir(), os.path.basename(download.url()))
                content = scraper.get(download.url()).content
                with open(filename, 'wb') as outfile:
                    outfile.write(content)
                outfile.close()
            except :
                wx.MessageBox(download.url(), 'Error loading model', wx.OK | wx.ICON_ERROR)
                return
                
            # unzip file
            try:
                zip_ref = zipfile.ZipFile(filename, 'r')
                zip_ref.extractall(filename+".tmp")
                zip_ref.close()
            except Exception as e:
                wx.MessageBox(format(e), 'Error unziping model', wx.OK | wx.ICON_ERROR)

            for file in glob.glob(filename+".tmp/*"):
                kicad_file = ''
                if file.endswith(".lib"):
                    with open(kicad_file, 'r') as content_file:
                        self.model.content = content_file.read()
                        print "--", self.model.content
                    
                    mod = kicad_lib_file.KicadLibFile()
                    mod.LoadFile(kicad_file)
                    image_file = tempfile.NamedTemporaryFile()
                    mod.Render(image_file.name, self.panel_image_model.GetRect().width, self.panel_image_model.GetRect().height)
                    img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                    image_file.close()
                    img = img.ConvertToBitmap()
                    self.bitmap_edit_model.SetBitmap(img)
            
            self.model.md5 = hashlib.md5(self.model.content).hexdigest()

        # download 3D model
        #TODO
                        
    def onButtonOpenUrlSnapedaClick( self, event ):
        if self.button_open_url_snapeda.Label!="<None>":
            webbrowser.open(self.button_open_url_snapeda.Label)
    
    def onButtonRemoveUrlSnapedaClick( self, event ):
        self.button_open_url_snapeda.Label = "<None>"
        self.button_open_url_snapeda = ''

    def onButtonModelEditApply( self, event ):
        model = self.model
        
        if model.metadata:
            metadata = json.loads(model.metadata)
        else:
            metadata = json.loads('{}')
        metadata['description'] = self.edit_model_description.Value
        metadata['comment'] = self.edit_model_comment.Value
        
        if self.button_open_url_snapeda.Label!="<None>":
            metadata['snapeda'] = self.button_open_url_snapeda.Label
            metadata['snapeda_uid'] = self.snapeda_uid
            metadata['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            metadata.pop('snapeda', '')
            metadata.pop('snapeda_uid', '')
            metadata.pop('updated', '')
        
        model.metadata = json.dumps(metadata)
        if not model.content:
            model.content = ''
            model.md5 = hashlib.md5(model.content).hexdigest()
            
        # send result event
        event = EditModelApplyEvent(
            data=model,
            # source_path is not changed in the model as we only have the filename here, not the full path
            # the full path should be reconstructed by caller
            model_name=self.edit_model_name.Value+".mod"
            )
        wx.PostEvent(self, event)
    
    def onButtonModelEditCancel( self, event ):
        event = EditModelCancelEvent()
        wx.PostEvent(self, event)
