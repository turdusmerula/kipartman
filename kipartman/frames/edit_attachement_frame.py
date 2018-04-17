from dialogs.dialog_edit_attachement import DialogEditAttachement

import wx
import rest
import os
from configuration import Configuration
import webbrowser

class EditAttachementFrame(DialogEditAttachement):
    def __init__(self, parent): 
        super(EditAttachementFrame, self).__init__(parent)
        self.local_file = ''
        self.attachement = None
        
    def addAttachement(self, type):
        self.Title = "Add attachement"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            attachement = type(id=self.attachement.id, description=self.text_description.Value, source_name=self.attachement.source_name, storage_path=self.attachement.storage_path)
            return attachement
        return None
    
    def editAttachement(self, attachement):
        self.Title = "Edit attachement"
        self.button_validate.LabelText = "Apply"
        self.attachement = attachement
        self.button_open_file.Label = attachement.source_name
        self.text_description.Value = attachement.description
        result = self.ShowModal()
        if result==wx.ID_OK:
            attachement.id = self.attachement.id
            attachement.description = self.text_description.Value
            return attachement
        return None

    def onButtonOpenFileClick( self, event ):
        configuration = Configuration()
        if self.button_open_file.Label!="<None>":
            url = os.path.join(configuration.kipartbase, 'file', self.attachement.storage_path)
            url = url.replace('\\','/') #Work around for running on Windows
            webbrowser.open(url)
    
    def onButtonAddFileClick( self, event ):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard="Symbol (*)|*",
                style=wx.FD_OPEN |
                wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                wx.FD_PREVIEW
        )
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.button_open_file.Label = os.path.basename(dlg.GetPath())
            self.local_file = os.path.basename(dlg.GetPath())

    # Virtual event handlers, overide them in your derived class
    def onValidateClick( self, event ):
        try:
            if self.local_file=='' and self.attachement is None:
                wx.MessageBox("No file selected", 'Error', wx.OK | wx.ICON_ERROR)
            elif self.local_file:
                attachement = rest.api.add_upload_file(upfile=self.local_file)
                if self.attachement is None:
                    self.attachement = rest.model.PartAttachement(id=attachement.id)
                self.attachement.id = attachement.id
                self.attachement.source_name = attachement.source_name
                self.attachement.storage_path = attachement.storage_path
                self.EndModal(wx.ID_OK)
            else:
                self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return None
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
