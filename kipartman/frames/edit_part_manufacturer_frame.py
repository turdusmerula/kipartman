from dialogs.dialog_edit_part_manufacturer import DialogEditPartManufacturer
from api.models import PartManufacturer
from api.queries import ManufacturersQuery
from rest_client.exceptions import QueryError
import wx
 

class EditPartManufacturerFrame(DialogEditPartManufacturer):
    def __init__(self, parent): 
        super(EditPartManufacturerFrame, self).__init__(parent)
        self.loadManufacturers()

    def loadManufacturers(self):
        manufacturers = ManufacturersQuery().get()
        choices = ["<none>"]
        for manufacturer in manufacturers:
            choices.append(manufacturer.name)
        self.choice_manufacturer.SetItems(choices)

    def AddManufacturer(self, part):
        self.Title = "Add manufacturer"
        self.part = part
        self.manufacturer = PartManufacturer()
 
        self.choice_manufacturer.SetSelection(0)
        self.edit_part_manufacturer_name.Value = ''

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.manufacturer
        return None

    def EditManufacturer(self, part, manufacturer):
        self.Title = "Edit manufacturer"
        self.part = part
        self.manufacturer = manufacturer

        if manufacturer.manufacturer:
            self.choice_manufacturer.SetSelection(self.manufacturer.manufacturer.id)
        else:
            self.choice_manufacturer.SetSelection(0)
        self.edit_part_manufacturer_name.Value = str(manufacturer.part_name)

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.manufacturer
        return None

    def onButtonPartManufacturerEditApply( self, event ):
        try:
            if self.choice_manufacturer.GetSelection()==0:
                self.manufacturer.manufacturer = None
            else:
                self.manufacturer.manufacturer = ManufacturersQuery().get()[self.choice_manufacturer.GetSelection()-1]
            self.manufacturer.part_name = int(self.edit_part_manufacturer_name.Value)

        except ValueError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 

        self.EndModal(wx.ID_OK)

    def onButtonPartManufacturerEditCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
