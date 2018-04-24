from dialogs.panel_edit_footprint import PanelEditFootprint
from frames.select_snapeda_frame import SelectSnapedaFrame, EVT_SELECT_SNAPEDA_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from kicad import kicad_mod_file
from kicad import lib_convert
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

EditFootprintApplyEvent, EVT_EDIT_FOOTPRINT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditFootprintCancelEvent, EVT_EDIT_FOOTPRINT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

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

class EditFootprintFrame(PanelEditFootprint): 
    def __init__(self, parent):
        super(EditFootprintFrame, self).__init__(parent)
        self.snapeda_uid = ''
        self.footprint_path = ''
        
    def SetFootprint(self, footprint):
        self.footprint = footprint
        self.ShowFootprint(footprint)

    def ShowFootprint(self, footprint):
        configuration = Configuration()
        
        # enable everything else
        if footprint:
            
            if footprint.metadata:
                metadata = json.loads(footprint.metadata)
            else:
                metadata = json.loads('{}')

            self.edit_footprint_name.Value = ''
            self.footprint_path = ''
            
            if NoneValue(footprint.source_path, '')!='':
                name = os.path.basename(footprint.source_path)
                if name.endswith('.kicad_mod')==True:
                    # path is a footprint
                    self.edit_footprint_name.Value = name.replace(".kicad_mod", "")
                    self.footprint_path = os.path.dirname(NoneValue(footprint.source_path, ''))
                elif name.endswith('.pretty')==True:
                    # path is a lib
                    self.footprint_path = name
                    
            self.edit_footprint_description.Value = MetadataValue(metadata, 'description', '')
            self.edit_footprint_comment.Value = MetadataValue(metadata, 'comment', '')
             
            self.button_open_url_snapeda.Label = MetadataValue(metadata, 'snapeda', '<None>')
            
            print "----", os.path.join(configuration.kicad_footprints_path, footprint.source_path)
            if self.edit_footprint_name.Value!='' and os.path.exists(os.path.join(configuration.kicad_footprints_path, footprint.source_path)):
                mod = kicad_mod_file.KicadModFile()
                mod.LoadFile(os.path.join(configuration.kicad_footprints_path, footprint.source_path))
                image_file = tempfile.NamedTemporaryFile()
                mod.Render(image_file.name, self.panel_image_footprint.GetRect().width, self.panel_image_footprint.GetRect().height)
                img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                image_file.close()
            else:
                img = wx.Image()
                img.Create(1, 1)

            img = img.ConvertToBitmap()
            self.bitmap_edit_footprint.SetBitmap(img)
                
        else:
            self.edit_footprint_name.Value = ''
            self.edit_footprint_description.Value = ''
            self.edit_footprint_comment.Value = ''
            self.button_open_url_snapeda.Label = "<None>"

            img = wx.Image()
            img.Create(1, 1)
            img = img.ConvertToBitmap()
            self.bitmap_edit_footprint.SetBitmap(img)


        
    def enable(self, enabled=True):
        self.edit_footprint_name.Enabled = enabled
        self.edit_footprint_description.Enabled = enabled
        self.edit_footprint_comment.Enabled = enabled
        self.button_remove_url_snapeda.Enabled = enabled
        self.button_footprint_editApply.Enabled = enabled
        self.button_footprint_editCancel.Enabled = enabled
        self.button_snapeda.Enabled = enabled
        
    def onButtonSnapedaClick( self, event ):
        # create a snapeda frame
        # dropdown frame
        dropdown = DropdownDialog(self.button_snapeda, SelectSnapedaFrame, initial_search=self.edit_footprint_name.Value, preview='footprint')
        dropdown.panel.Bind( EVT_SELECT_SNAPEDA_OK_EVENT, self.onSelectSnapedaFrameOk )
        dropdown.Dropdown()

    def onSelectSnapedaFrameOk(self, event):
        snapeda = event.data
        if not snapeda:
            return
        print snapeda.json
        
        self.edit_footprint_name.Value = snapeda.part_number()
        self.edit_footprint_description.Value = snapeda.short_description()
        self.snapeda_uid = snapeda.uniqueid()
        
        try:
            download = DownloadQuery()
            download.get(part_number=snapeda.part_number(), 
                               manufacturer=snapeda.manufacturer(),
                               uniqueid=snapeda.uniqueid(),
                               has_symbol=snapeda.has_symbol(),
                               has_footprint=snapeda.has_footprint())
            if download.error():
                wx.MessageBox(download.error(), 'Error downloading footprint', wx.OK | wx.ICON_ERROR)
                
        except:
            DialogSnapedaError(self).ShowModal()
            return
        
        self.button_open_url_snapeda.Label = "https://www.snapeda.com"+snapeda._links().self().href()

        # download footprint
        if download.url() and download.url()!='':
            try:
                print "Download from:", download.url()
                filename = os.path.join(tempfile.gettempdir(), os.path.basename(download.url()))
                content = scraper.get(download.url()).content
                with open(filename, 'wb') as outfile:
                    outfile.write(content)
                outfile.close()
            except :
                wx.MessageBox(download.url(), 'Error loading footprint', wx.OK | wx.ICON_ERROR)
                return
                
            # unzip file
            try:
                zip_ref = zipfile.ZipFile(filename, 'r')
                zip_ref.extractall(filename+".tmp")
                zip_ref.close()
            except Exception as e:
                wx.MessageBox(format(e), 'Error unziping footprint', wx.OK | wx.ICON_ERROR)

            for file in glob.glob(filename+".tmp/*"):
                kicad_file = ''
                if file.endswith(".mod"):
                    dst_libpath, list_of_parts = lib_convert.convert_mod_to_pretty(file, file.replace('.mod', '.pretty'))
                    if len(list_of_parts)>0:
                        kicad_file = os.path.join(dst_libpath, list_of_parts[0]+".kicad_mod")
                elif file.endswith(".kicad_mod"):
                    kicad_file = file

                self.footprint.content = ''
                if kicad_file!='':
                    with open(kicad_file, 'r') as content_file:
                        self.footprint.content = content_file.read()
                        print "****", self.footprint.content
                    
                    mod = kicad_mod_file.KicadModFile()
                    mod.LoadFile(kicad_file)
                    image_file = tempfile.NamedTemporaryFile()
                    mod.Render(image_file.name, self.panel_image_footprint.GetRect().width, self.panel_image_footprint.GetRect().height)
                    img = wx.Image(image_file.name, wx.BITMAP_TYPE_ANY)
                    image_file.close()
                    img = img.ConvertToBitmap()
                    self.bitmap_edit_footprint.SetBitmap(img)
            
            self.footprint.md5 = hashlib.md5(self.footprint.content).hexdigest()

        # download 3D symbol
        #TODO
                        
    def onButtonOpenUrlSnapedaClick( self, event ):
        if self.button_open_url_snapeda.Label!="<None>":
            webbrowser.open(self.button_open_url_snapeda.Label)
    
    def onButtonRemoveUrlSnapedaClick( self, event ):
        self.button_open_url_snapeda.Label = "<None>"
        self.button_open_url_snapeda = ''

    def onButtonFootprintEditApply( self, event ):
        footprint = self.footprint
        
        if footprint.metadata:
            metadata = json.loads(footprint.metadata)
        else:
            metadata = json.loads('{}')
        metadata['description'] = self.edit_footprint_description.Value
        metadata['comment'] = self.edit_footprint_comment.Value
        
        if self.button_open_url_snapeda.Label!="<None>":
            metadata['snapeda'] = self.button_open_url_snapeda.Label
            metadata['snapeda_uid'] = self.snapeda_uid
            metadata['updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            metadata.pop('snapeda', '')
            metadata.pop('snapeda_uid', '')
            metadata.pop('updated', '')
        
        footprint.metadata = json.dumps(metadata)
        if not footprint.content:
            footprint.content = ''
            footprint.md5 = hashlib.md5(footprint.content).hexdigest()
            
        # send result event
        event = EditFootprintApplyEvent(
            data=footprint,
            # source_path is not changed in the footprint as we only have the filename here, not the full path
            # the full path should be reconstructed by caller
            footprint_name=self.edit_footprint_name.Value+".kicad_mod"
            )
        wx.PostEvent(self, event)
    
    def onButtonFootprintEditCancel( self, event ):
        event = EditFootprintCancelEvent()
        wx.PostEvent(self, event)
