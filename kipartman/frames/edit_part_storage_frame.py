from dialogs.dialog_edit_part_storage import DialogEditPartStorage
from frames.select_storage_frame import SelectStorageFrame
from frames.dropdown_frame import DropdownFrame
import wx
import api.data.part_storage
from helper import colors

class EditPartStorageFrame(DialogEditPartStorage):
    def __init__(self, parent): 
        super(EditPartStorageFrame, self).__init__(parent)

        self.part = None
        self.part_storage = None

    def AddStorage(self, part):
        self.Title = "Add storage"
        self.button_validate.Label = "Add"
        self.part = part
        self.part_storage = api.data.part_storage.create(self.part, quantity=0)
 
        self.button_storage.Label = "<None>"
        self.storage = None
        self.spin_quantity.Value = 0

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_storage
        return None

    def EditStorage(self, part, part_storage):
        self.Title = "Edit storage"
        self.button_validate.Label = "Apply"
        self.part = part
        self.part_storage = part_storage
        
        if part_storage:
            self.button_storage.Label = part_storage.storage.name
        else:
            self.button_storage.Label = "<None>"
        self.storage = None
        self.spin_quantity.Value = self.part_storage.quantity
        
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_storage
        return None

    def _check(self):
        error = False
        
        if self.button_storage.Label=="<None>":
            error = True
            self.button_storage.SetBackgroundColour( colors.RED_ERROR )
        else:
            self.button_storage.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        try:
            self.spin_quantity.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            value = int(self.spin_quantity.Value)
            if value<0:
                self.spin_quantity.SetBackgroundColour( colors.RED_ERROR )
                error = True
                
        except Exception as e:
            error = True
            self.spin_quantity.SetBackgroundColour( colors.RED_ERROR )
            
        if error:
            self.button_validate.Enabled = False
        else:
            self.button_validate.Enabled = True

    def onButtonPartStorageClick( self, event ):
        frame = DropdownFrame(self.button_storage, SelectStorageFrame, self.storage)
        frame.Dropdown(self.onSetStorageCallback)
        self._check()
        event.Skip()

    def onSetStorageCallback(self, storage):
        if storage:
            self.button_storage.Label = storage.name
        else:
            self.button_storage.Label = "<none>"
        self.storage = storage
        self._check()

    def onValidateClick( self, event ):
        self._check()
        event.Skip()
            
    def onValidateClick( self, event ):
        if self.button_storage.Label=="<None>":
            raise Exception("No storage selected")
        if self.storage:
            self.part_storage.storage = self.storage            
        self.part_storage.quantity = self.spin_quantity.Value
        self.part.storages.add_pending(self.part_storage)
        self.EndModal(wx.ID_OK)
    
    def onCancelClick( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
