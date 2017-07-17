from dialogs.dialog_edit_category import DialogEditCategory

import wx

class EditCategoryFrame(DialogEditCategory):
    def __init__(self, parent): 
        super(EditCategoryFrame, self).__init__(parent)

    def addCategory(self, type):
        self.Title = "Add category"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            category = type(name=self.text_name.Value, description=self.text_description.Value)
            return category
        return None
    
    def editCategory(self, category):
        self.Title = "Edit category"
        self.button_validate.LabelText = "Apply"
        self.text_name.Value = category.name
        self.text_description.Value = category.description
        result = self.ShowModal()
        if result==wx.ID_OK:
            category.name = self.text_name.Value
            category.description = self.text_description.Value
            return category
        return None
    
    # Virtual event handlers, overide them in your derived class
    def onValidateClick( self, event ):
        self.EndModal(wx.ID_OK)
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
