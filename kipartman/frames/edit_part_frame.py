from dialogs.dialog_edit_part import DialogEditPart
from api.models import Part

import wx

def enum(**enums):
    return type('Enum', (), enums)

class EditPartFrame(DialogEditPart):    
    def __init__(self, parent): 
        super(EditPartFrame, self).__init__(parent)

    def addPart(self):
        self.Title = "Add part"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            part = Part()
            part.type = Part.Type_PART
            part.name = self.edit_name.Value
            part.description = self.edit_description.Value
            part.category = None #TODO
            part.footprint = None #TODO
            part.comment = self.edit_comment.Value
            return part
        return None
    
    def addMetapart(self):
        self.Title = "Add metapart"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            part = Part()
            part.type = Part.Type_METAPART
            part.name = self.edit_name.Value
            part.description = self.edit_description.Value
            part.category = None #TODO
            part.footprint = None #TODO
            part.comment = self.edit_comment.Value
            return part
        return None

    def edit(self, part):
        self.Title = "Edit part"
        self.button_validate.LabelText = "Apply"
        self.text_name.Value = part.name
        result = self.ShowModal()
        if result==wx.ID_OK:
            part.name = self.text_name.Value
            return part
        return None
    
    # Virtual event handlers, overide them in your derived class
    def onValidateClick( self, event ):
        self.EndModal(wx.ID_OK)
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
    