from dialogs.dialog_edit_storage import DialogEditStorage
import wx
from helper.exception import print_stack
from helper import colors
import api.data.storage

class EditStorageFrame(DialogEditStorage):
    def __init__(self, parent): 
        super(EditStorageFrame, self).__init__(parent)

    def AddStorage(self, category):
        self.storage = api.data.storage.create()        
        self.storage.category = category
        
        self.Title = "Add storage"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.storage
        return None
    
    def EditStorage(self, storage):
        self.storage = storage
        
        self.Title = "Edit storage"
        self.button_validate.LabelText = "Apply"
        self.text_name.Value = storage.name
        self.text_description.Value = storage.description
        self.text_comment.Value = storage.comment
        result = self.ShowModal()
        if result==wx.ID_OK:
            return storage
        return None

    def _check(self):
        error = False
        
        if self.text_name.Value=="":
            self.text_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.text_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            
        if error:
            self.button_validate.Enabled = False
        else:
            self.button_validate.Enabled = True

    def onValueChanged( self, event ):
        self._check()
        
    # Virtual event handlers, overide them in your derived class
    def onValidateClick( self, event ):
        self.storage.name = self.text_name.Value
        self.storage.description = self.text_description.Value
        self.storage.comment = self.text_comment.Value
        api.data.storage.save(self.storage)
        
        self.EndModal(wx.ID_OK)
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
