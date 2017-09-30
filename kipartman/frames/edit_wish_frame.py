from dialogs.dialog_edit_wish import DialogEditWish

import wx

class EditWishFrame(DialogEditWish):
    def __init__(self, parent): 
        super(EditWishFrame, self).__init__(parent)

    def addWish(self, type):
        self.Title = "Add wish"
        self.button_validate.LabelText = "Add"
        result = self.ShowModal()
        if result==wx.ID_OK:
            wish = type(quantity=self.spin_quantity.GetValue())
            return wish
        return None
    
    def editWish(self, wish):
        self.Title = "Edit wish"
        self.button_validate.LabelText = "Apply"
        self.spin_quantity.SetValue(wish.quantity)
        result = self.ShowModal()
        if result==wx.ID_OK:
            wish.quantity = self.spin_quantity.GetValue()
            return wish
        return None
    
    # Virtual event handlers, overide them in your derived class
    def onValidateClick( self, event ):
        self.EndModal(wx.ID_OK)
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
