from dialogs.panel_edit_footprint import PanelEditFootprint
from frames.select_snapeda_frame import SelectSnapedaFrame, EVT_SELECT_SNAPEDA_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from rest_client.exceptions import QueryError
from api import models
import wx.lib.newevent
from api.queries import FootprintsQuery
import urllib2
import tempfile
import os.path
import webbrowser
import cfscrape

EditFootprintApplyEvent, EVT_EDIT_FOOTPRINT_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditFootprintCancelEvent, EVT_EDIT_FOOTPRINT_CANCEL_EVENT = wx.lib.newevent.NewEvent()

scraper = cfscrape.create_scraper()

none_image = os.path.abspath('resources/none-128x128.png')

class EditFootprintFrame(PanelEditFootprint): 
    def __init__(self, parent):
        super(EditFootprintFrame, self).__init__(parent)
        
    def SetFootprint(self, footprint):
        self.footprint = footprint
        self.ShowFootprint(footprint)

    def ShowFootprint(self, footprint):
        # set local files to be added
        self.local_file_image = None
        self.local_file_footprint = None
        
        # enable evrything else
        if footprint:
            self.edit_footprint_name.Value = footprint.name
            self.edit_footprint_description.Value = footprint.description
            self.edit_footprint_comment.Value = footprint.comment
            if footprint.image:
                self.button_open_file_image.Label = footprint.image
                self.SetImage(footprint.image)
            else:
                self.button_open_file_image.Label = "<None>"
                self.SetImage()

            if footprint.footprint:
                self.button_open_file_footprint.Label = footprint.footprint
            else:
                self.button_open_file_footprint.Label = "<None>"
            print "image:", footprint.image
            print "footprint:", footprint.footprint
        else:
            self.edit_footprint_name.Value = ''
            self.edit_footprint_description.Value = ''
            self.edit_footprint_comment.Value = ''

    def enable(self, enabled=True):
        self.edit_footprint_name.Enabled = enabled
        self.edit_footprint_description.Enabled = enabled
        self.edit_footprint_comment.Enabled = enabled
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
            f = tempfile.gettempdir()+'/'+os.path.basename(filename)
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
#        res = wx.MessageBox(format(e), 'Open SnapEDA to the selected ', wx.YES | wx.NO | wx.ICON_QUESTION)
        self.edit_footprint_name.Value = snapeda.part_number()
        self.edit_footprint_description.Value = snapeda.short_description()
        # download image
        if snapeda.image()!='':
            try:
                filename = tempfile.gettempdir()+'/'+os.path.basename(snapeda.image())
                content = scraper.get(snapeda.image()).content
                with open(filename, 'wb') as outfile:
                    outfile.write(content)
                outfile.close()
                
                self.button_open_file_image.Label = os.path.basename(filename)
                self.local_file_image = filename
                self.SetImage(filename)
            except:
                print "%s: Error loading" % snapeda.image()
            
        self.SetImage(self.file_footprint_image.GetPath())

    def onButtonOpenFileImageClick( self, event ):
        if self.button_open_file_image.Label!="<None>":
            webbrowser.open(self.button_open_file_image.Label)

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
        if self.button_open_file_footprint.Label!="<None>":
            webbrowser.open(self.button_open_file_footprint.Label)
    
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
        if not footprint:
            footprint = models.Footprint()

        footprint.name = self.edit_footprint_name.Value
        footprint.description = self.edit_footprint_description.Value
        footprint.comment = self.edit_footprint_comment.Value            
        footprint.image = self.local_file_image
        footprint.footprint = self.local_file_footprint
            
        # send result event
        event = EditFootprintApplyEvent(data=footprint)
        wx.PostEvent(self, event)
    
    def onButtonFootprintEditCancel( self, event ):
        event = EditFootprintCancelEvent()
        wx.PostEvent(self, event)
