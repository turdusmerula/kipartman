from dialogs.panel_edit_distributor import PanelEditDistributor
from frames.dropdown_dialog import DropdownDialog
from frames.select_unit_frame import SelectUnitFrame
import wx
from helper.exception import print_stack
import api.data.distributor
import helper.colors as colors

EditDistributorApplyEvent, EVT_EDIT_DISTRIBUTOR_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditDistributorCancelEvent, EVT_EDIT_DISTRIBUTOR_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class KicadDistributorFrameException(Exception):
    def __init__(self, error):
        super(KicadDistributorFrameException, self).__init__(error)

def NoneValue(value, default):
    if value:
        return value
    return default

class EditDistributorFrame(PanelEditDistributor):
    def __init__(self, parent): 
        super(EditDistributorFrame, self).__init__(parent)

        # set initial state
        self.SetDistributor(None)
        self._enable(False)
        

    def SetDistributor(self, distributor):
        self.distributor = distributor
        
        self._show_distributor(distributor)
        self._enable(False)
        self._check()

    def EditDistributor(self, distributor):
        self.distributor = distributor
        
        self._show_distributor(distributor)
        self._enable(True)
        self._check()

    def AddDistributor(self):
        self.distributor = None
        
        self._show_distributor(self.distributor)
        self._enable(True)
        self._check()

    def _show_distributor(self, distributor):
        if distributor is not None:
            self.edit_distributor_name.Value = NoneValue(distributor.name, '')
            self.edit_distributor_address.Value = NoneValue(distributor.address, '')
            self.edit_distributor_website.Value = NoneValue(distributor.website, '')
            self.edit_distributor_sku_url.Value = NoneValue(distributor.sku_url, '')
            self.edit_distributor_email.Value = NoneValue(distributor.email, '')
            self.edit_distributor_phone.Value = NoneValue(distributor.phone, '')
            self.edit_distributor_comment.Value = NoneValue(distributor.comment, '')
        else:
            self.edit_distributor_name.Value = ''
            self.edit_distributor_address.Value = ''
            self.edit_distributor_website.Value = ''
            self.edit_distributor_sku_url.Value = ''
            self.edit_distributor_email.Value = ''
            self.edit_distributor_phone.Value = ''
            self.edit_distributor_comment.Value = ''
 
    def _enable(self, enabled=True):
        self.edit_distributor_name.Enabled = enabled
        self.edit_distributor_address.Enabled = enabled
        self.edit_distributor_website.Enabled = enabled
        self.edit_distributor_sku_url.Enabled = enabled
        self.edit_distributor_email.Enabled = enabled
        self.edit_distributor_phone.Enabled = enabled
        self.edit_distributor_comment.Enabled = enabled
        self.button_distributor_editApply.Enabled = enabled
        self.button_distributor_editCancel.Enabled = enabled
        
    def _check(self):
        error = False
        
        if self.edit_distributor_name.Value=="":
            self.edit_distributor_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_distributor_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if error:
            self.button_distributor_editApply.Enabled = False
        else:
            self.button_distributor_editApply.Enabled = self.button_distributor_editCancel.Enabled


    def onDistributorValueChanged( self, event ):
        self._check()
        event.Skip()

    def onApplyButtonClick( self, event ):
        if self.distributor is None and len(api.data.distributor.find([api.data.distributor.FilterSearchDistributor(self.edit_distributor_name.Value)]).all())>0:
            raise KicadDistributorFrameException(f"distributor '{self.edit_distributor_name.Value}' already exists")
        
        try:
            if self.distributor is None:
                self.distributor = api.data.distributor.create()
            
            self.distributor.name = self.edit_distributor_name.Value
            self.distributor.address = self.edit_distributor_address.Value
            self.distributor.website = self.edit_distributor_website.Value
            self.distributor.sku_url =  self.edit_distributor_sku_url.Value
            self.distributor.email = self.edit_distributor_email.Value
            self.distributor.phone = self.edit_distributor_phone.Value
            self.distributor.comment = self.edit_distributor_comment.Value
                
            self.distributor.save()
            
            wx.PostEvent(self, EditDistributorApplyEvent(data=self.distributor))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def onCancelButtonClick( self, event ):
        wx.PostEvent(self, EditDistributorCancelEvent())
        event.Skip()
