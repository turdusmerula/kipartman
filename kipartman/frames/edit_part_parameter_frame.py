from dialogs.dialog_edit_part_parameter import DialogEditPartParameter
from frames.dropdown_dialog import DropdownDialog
from frames.select_parameter_frame import SelectParameterFrame
import wx
from helper.exception import print_stack
import api.data.unit_prefix
import api.data.part_parameter
import helper.unit
from helper import colors

class EditPartParameterFrame(DialogEditPartParameter):
    def __init__(self, parent): 
        super(EditPartParameterFrame, self).__init__(parent)
        self.loadPrefixes()
        
        self.part = None
        self.part_parameter = None
        
        self._unit = None
        self._parameter = None
        
    def loadPrefixes(self):
        prefixes = api.data.unit_prefix.find()
        choices = ["auto"]
        self.prefix_symbol = [""]
        for prefix in prefixes:
            self.prefix_symbol.append(prefix.symbol)
            choices.append(prefix.symbol+"  "+prefix.name+" ("+prefix.power+")")
        self.choice_numeric_value_prefix.SetItems(choices)
    
    def AddPartParameter(self, part):
        self.part = part
        self.part_parameter = api.data.part_parameter.create(part=self.part)
        self._parameter = None
        self._unit = None
        
        self.Title = "Add parameter"

        self.button_search_parameter.Label = "..."
        self.button_parameter_description.Label = ""
        self.button_parameter_unit.Label = ""
        self.choice_numeric_value_prefix.SetSelection(0)
        self.choice_operator_numeric_value.SetSelection(0)
        self.choice_operator_text_value.SetSelection(0)
        
        self._show_parameter()
        self._check()
        
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_parameter
        return None

    def EditPartParameter(self, part, part_parameter):
        self.part = part
        self.part_parameter = part_parameter
        self._parameter = part_parameter.parameter
        self._unit = None
        if self._parameter is not None:
            self._unit = part_parameter.parameter.unit
        
        self.Title = "Edit parameter"

        self.button_search_parameter.Label = part_parameter.parameter.name
        self.button_parameter_description.Label = part_parameter.parameter.description
                    
        if part_parameter.text_value is not None:
            self.edit_text_value.Value = part_parameter.text_value
            
        if part_parameter.value is not None and self.part_parameter.parameter.value_type==api.models.ParameterType.FLOAT:
            self.edit_numeric_value.Value = str(part_parameter.value) 
        elif part_parameter.value is not None and self.part_parameter.parameter.value_type==api.models.ParameterType.INTEGER:
            self.edit_numeric_value.Value = str(int(part_parameter.value)) 
        
        if part_parameter.prefix is not None:
            self.choice_numeric_value_prefix.SetSelection(part_parameter.prefix.id)
        else:
            self.choice_numeric_value_prefix.SetSelection(0)

        if part.metapart==True and part_parameter.operator is not None:
            if self.part_parameter.parameter.value_type==api.models.ParameterType.TEXT:
                self.choice_operator_text_value.SetSelection(self.choice_operator_text_value.FindString(part_parameter.operator))
            else:
                self.choice_operator_numeric_value.SetSelection(self.choice_operator_numeric_value.FindString(part_parameter.operator))
                
        self._show_parameter()
        self._check()
        
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_parameter
        return None

    def _show_parameter(self):
        if self._parameter is not None:
            if self._unit is not None:
                self.button_parameter_unit.Label = f"{self._unit.name} ({self._unit.symbol})"
            else:
                self.button_parameter_unit.Label = ""
                
            if self._parameter.value_type==api.models.ParameterType.FLOAT:
                self.static_text_value.Hide()
                self.edit_text_value.Hide()
                
                self.static_numeric_value.Show()
                self.edit_numeric_value.Show()
                if self._unit is not None and self._unit.prefixable:
                    self.choice_numeric_value_prefix.Show()
                else:
                    self.choice_numeric_value_prefix.Hide()
                self.show_numeric_value.Show()            
                self.radio_choice_parameter_float.SetValue(True)
            elif self._parameter.value_type==api.models.ParameterType.INTEGER:
                self.static_text_value.Hide()
                self.edit_text_value.Hide()
                
                self.static_numeric_value.Show()
                self.edit_numeric_value.Show()
                self.choice_numeric_value_prefix.Hide()
                self.show_numeric_value.Show()
                self.radio_choice_parameter_integer.SetValue(True)
            else:
                self.static_text_value.Show()
                self.edit_text_value.Show()
                
                self.static_numeric_value.Hide()
                self.edit_numeric_value.Hide()
                self.choice_numeric_value_prefix.Hide()
                self.show_numeric_value.Hide()
                self.radio_choice_parameter_text.SetValue(True)
            
            if self.part.metapart==True and self._parameter.value_type==api.models.ParameterType.TEXT:
                self.choice_operator_numeric_value.Hide()
                self.choice_operator_text_value.Show()
            elif self.part.metapart==True:
                self.choice_operator_numeric_value.Show()
                self.choice_operator_text_value.Hide()
            else:
                self.choice_operator_numeric_value.Hide()
                self.choice_operator_text_value.Hide()
               
                
        else:
            self.static_text_value.Show()
            self.edit_text_value.Show()
            
            if self.part.metapart==True:
                self.choice_operator_numeric_value.Hide()
                self.choice_operator_text_value.Show()
            else:
                self.choice_operator_numeric_value.Hide()
                self.choice_operator_text_value.Hide()
                
            self.static_numeric_value.Hide()
            self.edit_numeric_value.Hide()
            self.choice_numeric_value_prefix.Hide()
            self.show_numeric_value.Hide()
            self.radio_choice_parameter_text.SetValue(True)


        self.Layout()
    
    def _check(self):
        error = False
        
        if self.button_search_parameter.Label=="...":
            self.button_search_parameter.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.button_search_parameter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        if self.radio_choice_parameter_text.Value==False:
            try:
                num, prefix, unit = helper.unit.cut_unit_value(self.edit_numeric_value.Value)
    
                if self._parameter.value_type==api.models.ParameterType.FLOAT:
                    v = helper.unit.expand_prefix(float(num), prefix)
                elif self._parameter.value_type==api.models.ParameterType.INTEGER:
                    v = int(num)
    
                self.edit_numeric_value.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            except:
                error = True
                self.edit_numeric_value.SetBackgroundColour( colors.RED_ERROR )

        if error:
            self.button_part_editApply.Enabled = False
        else:
            self.button_part_editApply.Enabled = True

    def _show_numeric_value(self):
        try:
            num, prefix, unit = helper.unit.cut_unit_value(self.edit_numeric_value.Value)

            if self._parameter.value_type==api.models.ParameterType.FLOAT:
                v = helper.unit.expand_prefix(float(num), prefix)
            elif self._parameter.value_type==api.models.ParameterType.INTEGER:
                v = int(num)
            
            if self._unit is not None:
                if self.choice_numeric_value_prefix.GetSelection()<=0:
                    self.show_numeric_value.Value = helper.unit.format_unit_prefix(v, self._unit.symbol)
                else:
                    self.show_numeric_value.Value = helper.unit.format_unit_prefix(v, self._unit.symbol, self.prefix_symbol[self.choice_numeric_value_prefix.GetSelection()])
            else:
                self.show_numeric_value.Value = str(v)
            
        except:
            self.show_numeric_value.Value = "#error"
        
    def onButtonPartParameterEditApply( self, event ):

        try:
            if self._parameter is None:
                raise ValueError('No parameter selected')

            if self.radio_choice_parameter_float.Value==True or self.radio_choice_parameter_integer.Value==True:
                self.part_parameter.text_value = None

                if self._parameter.unit_id is not None and self._parameter.unit.prefixable:
                    if self.choice_numeric_value_prefix.GetSelection()==0:
                        self.part_parameter.prefix = None
                    else:
                        self.part_parameter.prefix = api.data.unit_prefix.find_by_id(self.choice_numeric_value_prefix.GetSelection())
                else:
                    self.part_parameter.prefix = None
                
                if self.part.metapart==True:
                    self.part_parameter.metaparameter = True
                    self.part_parameter.operator = self.choice_operator_numeric_value.GetString(self.choice_operator_numeric_value.GetSelection())
                
                num, prefix, unit = helper.unit.cut_unit_value(self.edit_numeric_value.Value)
                v = helper.unit.expand_prefix(float(num), prefix)
                self.part_parameter.value = v
            else:
                self.part_parameter.text_value = self.edit_text_value.Value
                self.part_parameter.value = None
                self.part_parameter.prefix = None

                if self.part.metapart==True:
                    self.part_parameter.metaparameter = True
                    self.part_parameter.operator = self.choice_operator_text_value.GetString(self.choice_operator_text_value.GetSelection())

            self._parameter.unit = self._unit            
            self.part_parameter.parameter = self._parameter

            self.part.parameters.add_pending(self.part_parameter)
        except ValueError as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return 

        self.EndModal(wx.ID_OK)
            
    def onButtonSearchParameterClick( self, event ):
        frame = DropdownDialog(self, SelectParameterFrame, "")
        frame.DropHere(self.onSelectParameterFrameOk)
    
    def onSelectParameterFrameOk(self, parameter):
        self._parameter = parameter
        self._unit = parameter.unit
        
        self.button_search_parameter.Label = parameter.name
        self.button_parameter_description.Label = parameter.description
        
        self._show_parameter()
        self._show_numeric_value()
        self._check()

    def onTextValueChanged( self, event ):
        self._check()
        event.Skip()

    def onNumericValueChanged( self, event ):
        self._check()
        self._show_numeric_value()
        event.Skip()

    def onOperatorNumericValueChoice( self, event ):
        event.Skip()

    def onOperatorTextValueChoice( self, event ):
        event.Skip()
