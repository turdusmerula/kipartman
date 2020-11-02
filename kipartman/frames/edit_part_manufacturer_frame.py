from dialogs.dialog_edit_part_manufacturer import DialogEditPartManufacturer
import wx
from helper.exception import print_stack
import api.data.manufacturer
import api.data.part_manufacturer
from helper import colors

class EditPartManufacturerFrame(DialogEditPartManufacturer):
    def __init__(self, parent): 
        super(EditPartManufacturerFrame, self).__init__(parent)
        self.loadManufacturers()

        self.part = None
        self.part_manufacturer = None

    def loadManufacturers(self):
        self.manufacturers = [None]
        for manufacturer in api.data.manufacturer.find():
            self.manufacturers.append(manufacturer)
        choices = ["<none>"]
        for manufacturer in self.manufacturers[1:]:
            choices.append(manufacturer.name)
        self.choice_manufacturer.SetItems(choices)

    def AddManufacturer(self, part):
        self.Title = "Add manufacturer"
        self.part = part
        self.part_manufacturer = api.data.part_manufacturer.create(self.part)
 
        self.choice_manufacturer.SetSelection(0)
        self.edit_part_manufacturer_name.Value = ''

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_manufacturer
        return None

    def EditManufacturer(self, part, part_manufacturer):
        self.Title = "Edit manufacturer"
        self.part = part
        self.part_manufacturer = part_manufacturer

        if part_manufacturer:
            manufacturer_id = self.choice_manufacturer.FindString(self.part_manufacturer.manufacturer.name, caseSensitive=True)
            if manufacturer_id!=wx.NOT_FOUND:
                self.choice_manufacturer.SetSelection(manufacturer_id)
        else:
            self.choice_manufacturer.SetSelection(0)
        self.edit_part_manufacturer_name.Value = str(part_manufacturer.part_name)

        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_manufacturer
        return None

    def _check(self):
        error = False
        
        if self.choice_manufacturer.GetSelection()==0:
            error = True
            self.choice_manufacturer.SetBackgroundColour( colors.RED_ERROR )
        else:
            self.choice_manufacturer.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if self.edit_part_manufacturer_name.Value=="":
            self.edit_part_manufacturer_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_part_manufacturer_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            
        if error:
            self.button_part_editApply.Enabled = False
        else:
            self.button_part_editApply.Enabled = True


    def onButtonPartManufacturerEditApply( self, event ):
        try:
            if self.choice_manufacturer.GetSelection()==0:
                raise Exception("Missing manufacturer")
            else:
                manufacturer = self.manufacturers[self.choice_manufacturer.GetSelection()]
            self.part_manufacturer.manufacturer = manufacturer
            self.part_manufacturer.part_name = self.edit_part_manufacturer_name.Value

            self.part.manufacturers.add_pending(self.part_manufacturer)
        except ValueError as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 

        self.EndModal(wx.ID_OK)

    def onButtonPartManufacturerEditCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    
    def onValueChanged( self, event ):
        self._check()
        event.Skip()

