from dialogs.panel_edit_parameter import PanelEditParameter
from frames.dropdown_dialog import DropdownDialog
from frames.select_unit_frame import SelectUnitFrame
import wx
from helper.exception import print_stack
import api.data.unit
import helper.colors as colors

EditParameterApplyEvent, EVT_EDIT_PARAMETER_APPLY_EVENT = wx.lib.newevent.NewEvent()
EditParameterCancelEvent, EVT_EDIT_PARAMETER_CANCEL_EVENT = wx.lib.newevent.NewEvent()

class KicadParameterFrameException(Exception):
    def __init__(self, error):
        super(KicadParameterFrameException, self).__init__(error)


class EditParameterFrame(PanelEditParameter):
    def __init__(self, parent): 
        super(EditParameterFrame, self).__init__(parent)

        self._unit = None
        
        # set initial state
        self.SetParameter(None)
        self._enable(False)
        

    def SetParameter(self, parameter):
        self.parameter = parameter
        if parameter is None:
            self._unit = None
        else:
            self._unit = parameter.unit
        
        self._show_parameter(parameter)
        self._enable(False)
        self._check()

    def EditParameter(self, parameter):
        self.parameter = parameter
        if parameter is None:
            self._unit = None
        else:
            self._unit = parameter.unit
        
        self._show_parameter(parameter)
        self._enable(True)
        self._check()

    def AddParameter(self):
        self.parameter = None
        self._unit = None
        
        self._show_parameter(self.parameter)
        self._enable(True)
        self._check()

    def _show_parameter(self, parameter):
        # enable everything else
        if parameter is not None:
            self.edit_parameter_name.Value = parameter.name
            self.edit_parameter_description.Value = parameter.description
            
            if parameter.numeric:
                self.radio_choice_parameter_numeric.SetValue(True)
                self.static_unit.Show()
                self.button_search_unit.Show()
                self.button_remove_unit.Show()
            else:
                self.radio_choice_parameter_text.SetValue(True)
                self.static_unit.Hide()
                self.button_search_unit.Hide()
                self.button_remove_unit.Hide()
                
            if self._unit is not None:
                self.button_search_unit.Label = f"{self._unit.name} ({self._unit.symbol})"
            else:
                self.button_search_unit.Label = "<none>"
        else:
            self.edit_parameter_name.Value = ""
            self.edit_parameter_description.Value = ""
            self.radio_choice_parameter_numeric.SetValue(True)
            self.button_search_unit.Label = "<none>"
            self.static_unit.Show()
            self.button_search_unit.Show()
            self.button_remove_unit.Show()
 
    def _enable(self, enabled=True):
        self.edit_parameter_name.Enabled = enabled
        self.edit_parameter_description.Enabled = enabled
        self.radio_choice_parameter_numeric.Enabled = enabled
        self.radio_choice_parameter_text.Enabled = enabled
        self.button_search_unit.Enabled = enabled
        self.button_remove_unit.Enabled = enabled
        self.button_parameter_editApply.Enabled = enabled
        self.button_parameter_editCancel.Enabled = enabled

    def _check(self):
        error = False
        
        if self.edit_parameter_name.Value=="":
            self.edit_parameter_name.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.edit_parameter_name.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if error:
            self.button_parameter_editApply.Enabled = False
        else:
            self.button_parameter_editApply.Enabled = self.button_parameter_editCancel.Enabled

    def onButtonPartParameterEditApply( self, event ):
        if self.parameter is None and len(api.data.parameter.find([api.data.parameter.FilterSearchParameter(self.edit_parameter_name.Value)]).all())>0:
            raise KicadParameterFrameException(f"parameter '{self.edit_parameter_name.Value}' already exists")
        
        try:
            if self.parameter is None:
                self.parameter = api.data.parameter.create()
            
            self.parameter.name = self.edit_parameter_name.Value
            self.parameter.description = self.edit_parameter_description.Value
            
            self.parameter.unit = self._unit
            
            if self.radio_choice_parameter_numeric.Value:
                self.parameter.numeric = True
            else:
                self.parameter.numeric = False
                
            self.parameter.save()
            
            wx.PostEvent(self, EditParameterApplyEvent(data=self.parameter))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error renaming library', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def onButtonPartParameterEditCancel( self, event ):
        wx.PostEvent(self, EditParameterCancelEvent())
        event.Skip()

    def onTextEditParameterName( self, event ):
        self._check()
        event.Skip()

    def onTextEditParameterDescription( self, event ):
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
        