from dialogs.panel_edit_footprint import PanelEditFootprint
from frames.select_snapeda_frame import SelectSnapedaFrame, EVT_SELECT_SNAPEDA_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
import wx.lib.newevent
import urllib2
import tempfile
import os.path
import webbrowser
import cfscrape
import rest
from configuration import Configuration
from dialogs.dialog_snapeda_error import DialogSnapedaError
from snapeda.connection import snapeda_connection
from snapeda.queries import DownloadQuery
import zipfile
import glob, os
import datetime

EditFootprintApplyEvent, EVT_EDIT_FOOTPRINT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditFootprintCancelEvent, EVT_EDIT_FOOTPRINT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

scraper = cfscrape.create_scraper()

none_image = os.path.abspath(os.path.join('resources', 'none-128x128.png'))

def NoneValue(value, default):
    if value:
        return value
    return default

class EditFootprintFrame(PanelEditFootprint): 
    def __init__(self, parent):
        super(EditFootprintFrame, self).__init__(parent)
        
    def SetFootprint(self, footprint):
        self.footprint = footprint
        self.ShowFootprint(footprint)

    def ShowFootprint(self, footprint):
        configuration = Configuration()
        
        # set local files to be added
        self.local_file_image = None
        self.local_file_footprint = None
        
        # enable evrything else
        if footprint:
            self.edit_footprint_name.Value = NoneValue(footprint.name, '')
            self.edit_footprint_description.Value = NoneValue(footprint.description, '')
            self.edit_footprint_comment.Value = NoneValue(footprint.comment, '')

            try:
                self.button_open_file_image.Label = footprint.image.source_name
                try:
                    self.SetImage(os.path.join(configuration.kipartbase, 'file', footprint.image.storage_path))
                except Exception as e:
                    wx.MessageBox(format(e), "Error, failed to load '%s'" % (configuration.kipartbase+footprint.image.storage_path), wx.OK | wx.ICON_ERROR)
            except:
                self.button_open_file_image.Label = "<None>"
                self.SetImage()
            
            try:
                self.button_open_file_footprint.Label = footprint.footprint.source_name
            except:
                self.button_open_file_footprint.Label = "<None>"

            if footprint.snapeda:
                self.button_open_url_snapeda.Label = NoneValue(footprint.snapeda, '')
            else:
                self.button_open_url_snapeda.Label = "<None>"
        else:
            self.edit_footprint_name.Value = ''
            self.edit_footprint_description.Value = ''
            self.edit_footprint_comment.Value = ''
            self.button_open_file_image.Label = "<None>"
            self.button_open_file_footprint.Label = "<None>"
            self.button_open_url_snapeda.Label = "<None>"

    def enable(self, enabled=True):
        self.edit_footprint_name.Enabled = enabled
        self.edit_footprint_description.Enabled = enabled
        self.edit_footprint_comment.Enabled = enabled
        self.button_remove_url_snapeda.Enabled = enabled
        self.button_add_file_footprint.Enabled = enabled
        self.button_add_file_image.Enabled = enabled
        self.button_footprint_editApply.Enabled = enabled
        self.button_footprint_editCancel.Enabled = enabled
        self.button_remove_file_footprint.Enabled = enabled
        self.button_remove_file_image.Enabled = enabled
        self.button_snapeda.Enabled = enabled
        
    def SetImage(self, filename=none_image):
        try:
            data = urllib2.urlopen(filename)
            print "Load url:", filename
            f = os.path.join(tempfile.gettempdir(), os.path.basename(filename))
            with open(f, 'wb') as outfile:
                outfile.write(data.read())
            outfile.close()
        except:  # invalid URL, this is a file
            print "Load file:", filename
            f = filename
         
        img = wx.Image(f, wx.BITMAP_TYPE_ANY)
        #img = wx.Bitmap(self.file_footprint_image.GetPath(), wx.BITMAP_TYPE_ANY)
        self.PhotoMaxSize = self.bitmap_edit_footprint.GetSize().x
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        img = img.ConvertToBitmap()

        self.bitmap_edit_footprint.SetBitmap(img)

    def onButtonSnapedaClick( self, event ):
        # create a snapeda frame
        # dropdown frame
        dropdown = DropdownDialog(self.button_snapeda, SelectSnapedaFrame, self.edit_footprint_name.Value)
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

        # download image
        if snapeda.image()!='':
            try:
                filename = os.path.join(tempfile.gettempdir(), os.path.basename(snapeda.image()))
                content = scraper.get(snapeda.image()).content
                with open(filename, 'wb') as outfile:
                    outfile.write(content)
                outfile.close()
                 
                self.button_open_file_image.Label = os.path.basename(filename)
                self.local_file_image = filename
                self.SetImage(filename)
            except Exception as e:
                wx.MessageBox(format(e), 'Error loading image', wx.OK | wx.ICON_ERROR)

        # download footprint
        if download.url() and download.url()!='':
            try:
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
                if file.endswith(".lib"):
                    self.button_open_file_footprint.Label = os.path.basename(file)
                    self.local_file_footprint = file

    def onButtonOpenFileImageClick( self, event ):
        url = None
        configuration = Configuration()
        if self.local_file_image:
            url = self.local_file_image
        elif self.button_open_file_image.Label!="<None>":
            url = os.path.join(configuration.kipartbase, 'file', self.footprint.image.storage_path)
        if url:    
            webbrowser.open(url)

    def onButtonAddFileImageClick( self, event ):
        dlg = wx.FileDialog(
            self, message="Choose an image file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Bitmap (*.bmp)|*.bmp|PNG (*.png)|*.png|JPEG (*.jpg)|*.jpg|GIF (*.gif)|*.gif",
                style=wx.FD_OPEN |
                wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.button_open_file_image.Label = os.path.basename(dlg.GetPath())
            self.local_file_image = os.path.basename(dlg.GetPath())
            self.SetImage(dlg.GetPath())

            
    def onButtonRemoveFileImageClick( self, event ):
        self.button_open_file_image.Label = "<None>"
        self.local_file_image = ''
        self.SetImage()


    def onButtonOpenFileFootprintClick( self, event ):
        configuration = Configuration()
        if self.local_file_footprint:
            url = self.local_file_footprint
        elif self.button_open_file_footprint.Label!="<None>":
            url = os.path.join(configuration.kipartbase, 'file', self.footprint.footprint.storage_path)
        if url:    
            webbrowser.open(url)
    
    def onButtonAddFileFootprintClick( self, event ):
        dlg = wx.FileDialog(
            self, message="Choose a footprint file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Footprint (*.kicad_mod)|*.kicad_mod",
                style=wx.FD_OPEN |
                wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.button_open_file_footprint.Label = os.path.basename(dlg.GetPath())
            self.local_file_footprint = os.path.basename(dlg.GetPath())
    
    def onButtonRemoveFileFootprintClick( self, event ):
        self.button_open_file_footprint.Label = "<None>"
        self.local_file_footprint = ''

    def onButtonFootprintEditApply( self, event ):
        footprint = self.footprint
        
        footprint.name = self.edit_footprint_name.Value
        footprint.description = self.edit_footprint_description.Value
        footprint.comment = self.edit_footprint_comment.Value
        
        try:
            if self.local_file_image=='':
                footprint.image = None
            elif self.local_file_image:
                footprint.image = rest.api.add_upload_file(upfile=self.local_file_image)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        try:
            if self.local_file_footprint=='':
                footprint.footprint = None
            elif self.local_file_footprint:
                footprint.footprint = rest.api.add_upload_file(upfile=self.local_file_footprint)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        footprint.snapeda = self.button_open_url_snapeda.Label
        footprint.snapeda_uid = self.snapeda_uid
        footprint.updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # send result event
        event = EditFootprintApplyEvent(data=footprint)
        wx.PostEvent(self, event)
    
    def onButtonFootprintEditCancel( self, event ):
        event = EditFootprintCancelEvent()
        wx.PostEvent(self, event)

    def onButtonOpenUrlSnapedaClick( self, event ):
        if self.button_open_url_snapeda.Label!="<None>":
            webbrowser.open(self.button_open_url_snapeda.Label)
    
    def onButtonRemoveUrlSnapedaClick( self, event ):
        self.button_open_url_snapeda.Label = "<None>"
        self.button_open_url_snapeda = ''
