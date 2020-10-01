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
#         self.edit_distributor_name.Enabled = enabled
#         self.edit_distributor_description.Enabled = enabled
#         self.radio_choice_distributor_numeric.Enabled = enabled
#         self.radio_choice_distributor_text.Enabled = enabled
#         self.button_search_unit.Enabled = enabled
#         self.button_remove_unit.Enabled = enabled
#         self.button_distributor_editApply.Enabled = enabled
#         self.button_distributor_editCancel.Enabled = enabled
        pass
    
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

    def onButtonPartDistributorEditApply( self, event ):
        if self.distributor is None and len(api.data.distributor.find([api.data.distributor.FilterSearchDistributor(self.edit_distributor_name.Value)]).all())>0:
            raise KicadDistributorFrameException(f"distributor '{self.edit_distributor_name.Value}' already exists")
        
        try:
            if self.distributor is None:
                self.distributor = api.data.distributor.create()
            
            self.distributor.name = self.edit_distributor_name.Value
            self.distributor.description = self.edit_distributor_description.Value
            
            self.distributor.unit = self._unit
            
            if self.radio_choice_distributor_numeric.Value:
                self.distributor.numeric = True
            else:
                self.distributor.numeric = False
                
            self.distributor.save()
            
            wx.PostEvent(self, EditDistributorApplyEvent(data=self.distributor))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def onButtonPartDistributorEditCancel( self, event ):
        wx.PostEvent(self, EditDistributorCancelEvent())
        event.Skip()

    def onTextEditDistributorName( self, event ):
        self._check()
        event.Skip()

    def onTextEditDistributorDescription( self, event ):
        self._check()
        event.Skip()

    def onRadioNumeric( self, event ):
        self._check()
        self.static_unit.Show()
        self.button_search_unit.Show()
        event.Skip()

    def onRadioText( self, event ):
        self._check()
        self.static_unit.Hide()
        self.button_search_unit.Hide()
        event.Skip()

    def onButtonSearchUnitClick( self, event ):
        frame = DropdownDialog(self, SelectUnitFrame, "")
        frame.DropHere(self.onSelectUnitFrameOk)
        event.Skip()

    def onButtonRemoveUnitClick( self, event ):
        self._unit = None
        self.button_search_unit.Label = "<none>"
        event.Skip()

    def onSelectUnitFrameOk(self, unit):
        self._unit = unit
        self.button_search_unit.Label = f"{self._unit.name} ({self._unit.symbol})"
        self._check()

# 
#     def onButtonAddDistributorClick( self, event ):
#         self.ShowDistributor(None)
#         self.panel_edit_distributor.Enabled = True
#         self.panel_distributors.Enabled = False
# 
#     def onButtonEditDistributorClick( self, event ):
#         item = self.tree_distributors.GetSelection()
#         if item.IsOk()==False:
#             return 
#         distributor = self.tree_distributors_manager.ItemToObject(item)
#         self.ShowDistributor(distributor.distributor)
#         
#         self.panel_edit_distributor.Enabled = True
#         self.panel_distributors.Enabled = False
# 
#     def onButtonRemoveDistributorClick( self, event ):
#         item = self.tree_distributors.GetSelection()
#         if item.IsOk()==False:
#             return
#         distributor = self.tree_distributors_manager.ItemToObject(item)
#         rest.api.delete_distributor(distributor.distributor.id)
#         self.tree_distributors_manager.DeleteItem(None, distributor)
#         
#     def onButtonRefreshDistributorsClick( self, event ):
#         self.load()
#     
#     def onTreeDistributorsSelectionChanged( self, event ):
#         item = self.tree_distributors.GetSelection()
#         if item.IsOk()==False:
#             return
#         distributor = self.tree_distributors_manager.ItemToObject(item)
#         self.ShowDistributor(distributor.distributor)
#     
#     def onApplyButtonClick( self, event ):
#         
#         if self.distributor is None:
#             distributor = rest.model.DistributorNew()
#             distributor.allowed = True
#         else:
#             distributor = self.distributor
#         
#         distributor.name = self.edit_distributor_name.Value
#         distributor.address = self.edit_distributor_address.Value
#         distributor.website = self.edit_distributor_website.Value
#         distributor.sku_url = self.edit_distributor_sku_url.Value
#         distributor.email = self.edit_distributor_email.Value
#         distributor.phone = self.edit_distributor_phone.Value
#         distributor.comment = self.edit_distributor_comment.Value
# 
#         try:
#             if self.distributor is None:
#                 distributor = rest.api.add_distributor(distributor)
#                 self.tree_distributors_manager.AppendItem(None, Distributor(distributor))
#             else:
#                 distributor = rest.api.update_distributor(distributor.id, distributor)
#                 self.tree_distributors_manager.UpdateDistributor(distributor)
#                 
#             self.panel_edit_distributor.Enabled = False
#             self.panel_distributors.Enabled = True
#             
#         except Exception as e:
#             print_stack()
#             wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
# 
#         
#     def onCancelButtonClick( self, event ):
#         self.panel_edit_distributor.Enabled = False
#         self.panel_distributors.Enabled = True

