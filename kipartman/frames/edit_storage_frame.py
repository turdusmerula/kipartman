from dialogs.dialog_edit_storage import DialogEditStorage

import wx

class EditStorageFrame(DialogEditStorage):
    def __init__(self, parent): 
        super(EditStorageFrame, self).__init__(parent)

    def addStorage(self, type):
        self.Title = "Add storage"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            storage = type(name=self.text_name.Value, description=self.text_description.Value, comment=self.text_comment.Value)
            return storage
        return None
    
    def editStorage(self, storage):
        self.Title = "Edit storage"
        self.button_validate.LabelText = "Apply"
        self.text_name.Value = storage.name
        self.text_description.Value = storage.description
        self.text_comment.Value = storage.comment
        result = self.ShowModal()
        if result==wx.ID_OK:
            storage.name = self.text_name.Value
            storage.description = self.text_description.Value
            storage.comment = self.text_comment.Value
            return storage
        return None
    
    # Virtual event handlers, overide them in your derived class
    def onValidateClick( self, event ):
        self.EndModal(wx.ID_OK)
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
