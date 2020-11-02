from dialogs.panel_edit_manufacturer import PanelEditManufacturer
import wx
from helper.exception import print_stack
import api.data.manufacturer
import helper.colors as colors

EditManufacturerApplyEvent, EVT_EDIT_MANUFACTURER_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditManufacturerCancelEvent, EVT_EDIT_MANUFACTURER_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class KicadManufacturerFrameException(Exception):
    def __init__(self, error):
        super(KicadManufacturerFrameException, self).__init__(error)

def NoneValue(value, default):
    if value:
        return value
    return default


class EditManufacturerFrame(PanelEditManufacturer): 
    def __init__(self, parent):
        super(EditManufacturerFrame, self).__init__(parent)
        
        # set initial state
        self.SetManufacturer(None)
        self._enable(False)
        
        
    def SetManufacturer(self, manufacturer):
        self.manufacturer = manufacturer
        
        self._show_manufacturer(manufacturer)
        self._enable(False)
        self._check()

    def EditManufacturer(self, manufacturer):
        self.manufacturer = manufacturer
        
        self._show_manufacturer(manufacturer)
        self._enable(True)
        self._check()

    def AddManufacturer(self):
        self.manufacturer = None
        
        self._show_manufacturer(self.manufacturer)
        self._enable(True)
        self._check()

    def _show_manufacturer(self, manufacturer):
        self.manufacturer = manufacturer
        
        if manufacturer is not None:
            self.edit_manufacturer_name.Value = NoneValue(manufacturer.name, '')
            self.edit_manufacturer_address.Value = NoneValue(manufacturer.address, '')
            self.edit_manufacturer_website.Value = NoneValue(manufacturer.website, '')
            self.edit_manufacturer_email.Value = NoneValue(manufacturer.email, '')
            self.edit_manufacturer_phone.Value = NoneValue(manufacturer.phone, '')
            self.edit_manufacturer_comment.Value = NoneValue(manufacturer.comment, '')
        else:
            self.edit_manufacturer_name.Value = ''
            self.edit_manufacturer_address.Value = ''
            self.edit_manufacturer_website.Value = ''
            self.edit_manufacturer_email.Value = ''
            self.edit_manufacturer_phone.Value = ''
            self.edit_manufacturer_comment.Value = ''

    def _enable(self, enabled=True):
        self.edit_manufacturer_name.Enabled = enabled
        self.edit_manufacturer_address.Enabled = enabled
        self.edit_manufacturer_website.Enabled = enabled
        self.edit_manufacturer_email.Enabled = enabled
        self.edit_manufacturer_phone.Enabled = enabled
        self.edit_manufacturer_comment.Enabled = enabled
        self.button_manufacturer_editApply.Enabled = enabled
        self.button_manufacturer_editCancel.Enabled = enabled

    def _check(self):
        error = False
        
        if self.edit_manufacturer_name.Value=="":
            self.edit_manufacturer_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_manufacturer_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if error:
            self.button_manufacturer_editApply.Enabled = False
        else:
            self.button_manufacturer_editApply.Enabled = self.button_manufacturer_editCancel.Enabled


    def onManufacturerValueChanged( self, event ):
        self._check()
        event.Skip()

    def onApplyButtonClick( self, event ):
        if self.manufacturer is None and len(api.data.manufacturer.find([api.data.manufacturer.FilterName(self.edit_manufacturer_name.Value)]).all())>0:
            raise KicadManufacturerFrameException(f"manufacturer '{self.edit_manufacturer_name.Value}' already exists")
        
        try:
            if self.manufacturer is None:
                self.manufacturer = api.data.manufacturer.create()
            
            self.manufacturer.name = self.edit_manufacturer_name.Value
            self.manufacturer.address = self.edit_manufacturer_address.Value
            self.manufacturer.website = self.edit_manufacturer_website.Value
            self.manufacturer.email = self.edit_manufacturer_email.Value
            self.manufacturer.phone = self.edit_manufacturer_phone.Value
            self.manufacturer.comment = self.edit_manufacturer_comment.Value
                
            self.manufacturer.save()
            
            wx.PostEvent(self, EditManufacturerApplyEvent(data=self.manufacturer))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def onCancelButtonClick( self, event ):
        wx.PostEvent(self, EditManufacturerCancelEvent())
        event.Skip()
