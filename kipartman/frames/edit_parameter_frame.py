from dialogs.panel_edit_parameter import PanelEditParameter
from frames.dropdown_dialog import DropdownDialog
from frames.select_unit_frame import SelectUnitFrame
import wx
from helper.exception import print_stack
import api.data.unit
import api.data.parameter_alias
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
        self._alias = []
        
        # set initial state
        self.SetParameter(None)
        self._enable(False)
        

    def SetParameter(self, parameter):
        self.parameter = parameter
        self._unit = None
        self._alias = []
        if parameter is not None:
            self._unit = parameter.unit

        self._show_parameter(parameter)
        self._enable(False)
        self._check()

    def EditParameter(self, parameter):
        self.parameter = parameter
        self._unit = parameter.unit
        self._alias = []
        for alias in parameter.alias.all():
            self._alias.append(alias.name)
        
        self._show_parameter(parameter)
        self._enable(True)
        self._check()

    def AddParameter(self, name=None):
        self.parameter = None
        self._unit = None
        self._alias = []
        
        self._show_parameter(self.parameter)
        
        if name is not None:
            self.edit_parameter_name.Value = name
            
        self._enable(True)
        self._check()

    def _show_parameter(self, parameter):
        # enable everything else
        if parameter is not None:
            self.edit_parameter_name.Value = parameter.name
            
            self.combo_parameter_alias.Clear()
            for alias in self._alias:
                self.combo_parameter_alias.Append(alias)

            self.edit_parameter_description.Value = parameter.description
            
            if parameter.value_type==api.models.ParameterType.INTEGER:
                self.radio_choice_parameter_integer.SetValue(True)
                self.static_unit.Show()
                self.button_search_unit.Show()
                self.button_remove_unit.Show()
            elif parameter.value_type==api.models.ParameterType.INTEGER:
                self.radio_choice_parameter_float.SetValue(True)
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
            self.combo_parameter_alias.Clear()
            self.edit_parameter_description.Value = ""
            self.radio_choice_parameter_float.SetValue(True)
            self.button_search_unit.Label = "<none>"
            self.static_unit.Show()
            self.button_search_unit.Show()
            self.button_remove_unit.Show()
 
    def _enable(self, enabled=True):
        self.edit_parameter_name.Enabled = enabled
        self.combo_parameter_alias.Enable = enabled
        self.combo_parameter_alias.SetEditable(enabled)
        self.button_parameter_alias_add.Enable = enabled
        self.button_parameter_alias_remove.Enable = enabled
        self.edit_parameter_description.Enabled = enabled
        self.radio_choice_parameter_float.Enabled = enabled
        self.radio_choice_parameter_integer.Enabled = enabled
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
        
        if self.combo_parameter_alias.Value=="":
            self.button_parameter_alias_add.Enabled = False
            self.button_parameter_alias_remove.Enabled = False
        else:
            self.button_parameter_alias_add.Enabled = self.button_parameter_editCancel.Enabled
            self.button_parameter_alias_remove.Enabled = self.button_parameter_editCancel.Enabled
            
            if self.combo_parameter_alias.Value in self._alias:
                self.button_parameter_alias_add.Enabled = False
            if self.combo_parameter_alias.Value not in self._alias:
                self.button_parameter_alias_remove.Enabled = False
                    
        if error:
            self.button_parameter_editApply.Enabled = False
        else:
            self.button_parameter_editApply.Enabled = self.button_parameter_editCancel.Enabled

    def onButtonPartParameterEditApply( self, event ):
        
        try:
            if self.parameter is None and len(api.data.parameter.find([api.data.parameter.FilterSearchParameter(self.edit_parameter_name.Value)]).all())>0:
                raise KicadParameterFrameException(f"parameter '{self.edit_parameter_name.Value}' already exists")

            if self.parameter is None:
                self.parameter = api.data.parameter.create()

            
            self.parameter.name = self.edit_parameter_name.Value
            
            for alias in self.parameter.alias.all():
                if alias.name not in self._alias:
                    self.parameter.alias.remove_pending(alias)
            for alias in self._alias:
                parameter_alias = api.data.parameter_alias.create()
                parameter_alias.name = alias
                
                # check if alias must be add
                found = False
                for a in self.parameter.alias.all():
                    if alias==a.name:
                        found = True
                
                if found==False:
                    if len(api.data.parameter_alias.find([api.data.parameter_alias.FilterName(alias)]))>0:
                        raise KicadParameterFrameException(f"parameter '{alias}' already exists")
                    if len(api.data.parameter.find([api.data.parameter.FilterName(alias)]))>0: 
                        raise KicadParameterFrameException(f"parameter '{alias}' already exists")
                    self.parameter.alias.add_pending(parameter_alias)
                
            self.parameter.description = self.edit_parameter_description.Value
            
            self.parameter.unit = self._unit
            
            if self.radio_choice_parameter_float.Value:
                self.parameter.value_type = api.models.ParameterType.FLOAT
            elif self.radio_choice_parameter_integer.Value:
                self.parameter.value_type = api.models.ParameterType.INTEGER
            else:
                self.parameter.value_type = api.models.ParameterType.TEXT
                
            if self.parameter.value_type==api.models.ParameterType.INTEGER and self._unit is not None and self._unit.prefixable==True:
                raise KicadParameterFrameException(f"Cannot use a prefixable unit with an integer parameter")
                
            self.parameter.save()
            
            wx.PostEvent(self, EditParameterApplyEvent(data=self.parameter))
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error saving parameter', wx.OK | wx.ICON_ERROR)

        event.Skip()

    def onButtonPartParameterEditCancel( self, event ):
        wx.PostEvent(self, EditParameterCancelEvent())
        event.Skip()

    def onTextEditParameterName( self, event ):
        self._check()
        event.Skip()

    def onComboParameterAliasChange( self, event ):
        self._check()
        event.Skip()

    def onButtonParameterAliasAddClick( self, event ):
        self._alias.append(self.combo_parameter_alias.Value)
        self.combo_parameter_alias.Clear()
        for alias in self._alias:
            self.combo_parameter_alias.Append(alias)
        
        event.Skip()

    def onButtonParameterAliasRemoveClick( self, event ):
        self._alias.remove(self.combo_parameter_alias.Value)
        self.combo_parameter_alias.Clear()
        for alias in self._alias:
            self.combo_parameter_alias.Append(alias)
        event.Skip()

    def onTextEditParameterDescription( self, event ):
        self._check()
        event.Skip()

    def onRadioValueType( self, event ):
        self._check()
        if self.radio_choice_parameter_float.Value==True or self.radio_choice_parameter_integer.Value==True:
            self.static_unit.Show()
            self.button_search_unit.Show()
            self.button_remove_unit.Show()
        else:
            self.static_unit.Hide()
            self.button_search_unit.Hide()
            self.button_remove_unit.Hide()
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
        