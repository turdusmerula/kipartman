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
                
    def loadPrefixes(self):
        prefixes = api.data.unit_prefix.find()
        choices = ["auto"]
        self.prefix_symbol = [""]
        for prefix in prefixes:
            self.prefix_symbol.append(prefix.symbol)
            choices.append(prefix.symbol+"  "+prefix.name+" ("+prefix.power+")")
        self.choice_numeric_value_prefix.SetItems(choices)
    
    def AddParameter(self, part):
        self.part = part        
        self.part_parameter = api.data.part_parameter.create(self.part)
        
        self.Title = "Add parameter"

        self.onRadioNumeric(None)

        self.button_search_parameter.Label = "..."
        self.button_parameter_description.Label = ""
        self.button_parameter_unit.Label = ""
        self.choice_numeric_value_prefix.SetSelection(0)

        self._check()
        
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_parameter
        return None

    def EditParameter(self, part, part_parameter):
        self.part = part
        self.part_parameter = part_parameter

        self.Title = "Edit parameter"

        self.button_search_parameter.Label = part_parameter.parameter.name
        self.button_parameter_description.Label = part_parameter.parameter.description
        
        if part_parameter.parameter.unit is not None:
            self.button_parameter_unit.Label = f"{part_parameter.parameter.unit.name} ({part_parameter.parameter.unit.symbol})"
        else:
            self.button_parameter_unit.Label = ""
            
        if part_parameter.parameter.numeric==True:
            self.onRadioNumeric(None)
            self.radio_choice_parameter_numeric.SetValue(True)
        else:
            self.onRadioText(None)
            self.radio_choice_parameter_text.SetValue(True)

        if part_parameter.text_value is not None:
            self.edit_text_value.Value = part_parameter.text_value

        if part_parameter.value is not None:
            self.edit_numeric_value.Value = str(part_parameter.value) 
        if part_parameter.prefix is not None:
            self.choice_numeric_value_prefix.SetSelection(part_parameter.prefix.id)
        else:
            self.choice_numeric_value_prefix.SetSelection(0)
            
        if part_parameter.parameter.unit is not None and part_parameter.parameter.unit.prefixable:
            self.choice_numeric_value_prefix.Show()
        else:
            self.choice_numeric_value_prefix.Hide()
            
        self._check()
            
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_parameter
        return None

    def _check(self):
        error = False
        
        if self.button_search_parameter.Label=="...":
            self.button_search_parameter.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.button_search_parameter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            
        try:
            if self.edit_numeric_value.Value!="":
                float(self.edit_numeric_value.Value) 
            self.edit_numeric_value.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        except:
            error = True
            self.edit_numeric_value.SetBackgroundColour( colors.RED_ERROR )

        if error:
            self.button_part_editApply.Enabled = False
        else:
            self.button_part_editApply.Enabled = True

    def onButtonPartParameterEditApply( self, event ):
        if self.part_parameter.parameter is None:
            raise ValueError('No parameter selected')

        try:
            if self.radio_choice_parameter_numeric.Value==True:
                self.part_parameter.text_value = None

                if self.part_parameter.parameter.unit_id is not None and self.part_parameter.parameter.unit.prefixable:
                    if self.choice_numeric_value_prefix.GetSelection()==0:
                        self.part_parameter.prefix = None
                    else:
                        self.part_parameter.prefix = api.data.unit_prefix.find_by_id(self.choice_numeric_value_prefix.GetSelection())
                else:
                    self.part_parameter.prefix = None
                    
                num, prefix, unit = helper.unit.cut_unit_value(self.edit_numeric_value.Value)
                v = helper.unit.expand_prefix(float(num), prefix)
                self.part_parameter.value = v
            else:
                self.part_parameter.text_value = self.edit_text_value.Value
                self.part_parameter.value = None
                self.part_parameter.prefix = None
            
            if self.part_parameter.id is None:
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
    
    def onRadioNumeric( self, event ):
        self.static_text_value.Hide()
        self.edit_text_value.Hide()
        
        self.static_numeric_value.Show()
        self.edit_numeric_value.Show()
        if self.part_parameter.parameter_id is not None and self.part_parameter.parameter.unit is not None and self.part_parameter.parameter.unit.prefixable:
            self.choice_numeric_value_prefix.Show()
        else:
            self.choice_numeric_value_prefix.Hide()
        self.show_numeric_value.Show()
        
        self.Layout()
        
        self._check()
        
    def onRadioText( self, event ):
        self.static_text_value.Show()
        self.edit_text_value.Show()
        
        self.static_numeric_value.Hide()
        self.edit_numeric_value.Hide()
        self.choice_numeric_value_prefix.Hide()
        self.show_numeric_value.Hide()

        self.Layout()
        
        self._check()
        
    def onButtonSearchParameterClick( self, event ):
        frame = DropdownDialog(self, SelectParameterFrame, "")
        frame.DropHere(self.onSelectParameterFrameOk)
    
    def onSelectParameterFrameOk(self, parameter):
        self.part_parameter.parameter = parameter
        
        self.button_search_parameter.Label = parameter.name
        self.button_parameter_description.Label = parameter.description
        
        if parameter.numeric:
            self.radio_choice_parameter_numeric.SetValue(True)
            self.onRadioNumeric(None)
        else:
            self.radio_choice_parameter_text.SetValue(True)
            self.onRadioText(None)
            
        if parameter.unit is not None:
            self.button_parameter_unit.Label = f"{parameter.unit.name} ({parameter.unit.symbol})"
        else:
            self.button_parameter_unit.Label = f""
            
        self._check()

    def onTextValueChanged( self, event ):
        self._check()
        event.Skip()

    def onNumericValueChanged( self, event ):
        try:
            num, prefix, unit = helper.unit.cut_unit_value(self.edit_numeric_value.Value)
            v = helper.unit.expand_prefix(float(num), prefix)

            if self.choice_numeric_value_prefix.GetSelection()<=0:
                self.show_numeric_value.Value = helper.unit.format_unit_prefix(v, self.part_parameter.parameter.unit.symbol)
            else:
                self.show_numeric_value.Value = helper.unit.format_unit_prefix(v, self.part_parameter.parameter.unit.symbol, self.prefix_symbol[self.choice_numeric_value_prefix.GetSelection()])
        except:
            self.show_numeric_value.Value = "#error"
            
        event.Skip()
