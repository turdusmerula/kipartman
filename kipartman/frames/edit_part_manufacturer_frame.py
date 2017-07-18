from dialogs.dialog_edit_part_manufacturer import DialogEditPartManufacturer
import wx
import rest

class EditPartManufacturerFrame(DialogEditPartManufacturer):
    def __init__(self, parent): 
        super(EditPartManufacturerFrame, self).__init__(parent)
        self.loadManufacturers()

    def loadManufacturers(self):
        manufacturers = rest.api.find_manufacturers()
        choices = ["<none>"]
        for manufacturer in manufacturers:
            choices.append(manufacturer.name)
        self.choice_manufacturer.SetItems(choices)

    def AddManufacturer(self, part):
        self.Title = "Add manufacturer"
        self.part = part
        self.manufacturer = rest.model.PartManufacturer()
 
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

        if manufacturer:
            manufacturer_id = rest.api.find_manufacturers(name=self.manufacturer.name)[0].id
            self.choice_manufacturer.SetSelection(manufacturer_id)
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
                raise Exception("Missing manufacturer")
            else:
                manufacturer = rest.api.find_manufacturer(self.choice_manufacturer.GetSelection())
            self.manufacturer.name = manufacturer.name
            self.manufacturer.part_name = self.edit_part_manufacturer_name.Value

        except ValueError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 

        self.EndModal(wx.ID_OK)

    def onButtonPartManufacturerEditCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
