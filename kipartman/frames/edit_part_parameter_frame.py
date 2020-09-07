from dialogs.dialog_edit_part_parameter import DialogEditPartParameter
from frames.dropdown_dialog import DropdownDialog
from frames.select_parameter_frame import SelectParameterFrame
import wx
from helper.exception import print_stack
import api.data.unit_prefix
import api.data.part_parameter
from helper import colors

class EditPartParameterFrame(DialogEditPartParameter):
    def __init__(self, parent): 
        super(EditPartParameterFrame, self).__init__(parent)
        self.loadPrefixes()
        
        self.part = None
        self.part_parameter = None
        
        self.value_parameter = None
        
    def loadPrefixes(self):
        prefixes = api.data.unit_prefix.find()
        choices = ["auto"]
        for prefix in prefixes:
            choices.append(prefix.symbol+"  "+prefix.name+" ("+prefix.power+")")
        self.choice_part_parameter_min_prefix.SetItems(choices)
        self.choice_part_parameter_nom_prefix.SetItems(choices)
        self.choice_part_parameter_max_prefix.SetItems(choices)
    
    def _check(self):
        error = False
        
        if self.button_search_parameter.Label=="...":
            self.button_search_parameter.SetBackgroundColour( colors.RED_ERROR )
            error = True
        else:
            self.button_search_parameter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
            
        try:
            if self.edit_part_parameter_min_value.Value!="":
                float(self.edit_part_parameter_min_value.Value) 
            self.edit_part_parameter_min_value.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        except:
            error = True
            self.edit_part_parameter_min_value.SetBackgroundColour( colors.RED_ERROR )

        try:
            if self.edit_part_parameter_nom_value.Value!="":
                float(self.edit_part_parameter_nom_value.Value) 
            self.edit_part_parameter_nom_value.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        except:
            error = True
            self.edit_part_parameter_nom_value.SetBackgroundColour( colors.RED_ERROR )

        try:
            if self.edit_part_parameter_max_value.Value!="":
                float(self.edit_part_parameter_max_value.Value) 
            self.edit_part_parameter_max_value.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        except:
            error = True
            self.edit_part_parameter_max_value.SetBackgroundColour( colors.RED_ERROR )

        if error:
            self.button_part_editApply.Enabled = False
        else:
            self.button_part_editApply.Enabled = True

    def AddParameter(self, part):
        self.part = part        
        self.part_parameter = api.data.part_parameter.create(self.part)
        
        self.Title = "Add parameter"

        self.onRadioNumeric(None)

        self.button_search_parameter.Label = "..."
        self.button_parameter_description.Label = ""
        self.button_parameter_unit.Label = ""
        self.choice_part_parameter_min_prefix.SetSelection(0)
        self.choice_part_parameter_nom_prefix.SetSelection(0)
        self.choice_part_parameter_max_prefix.SetSelection(0)

        self._check()
        
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_parameter
        return None

    def EditParameter(self, part, part_parameter):
        self.part = part
        self.part_parameter = part_parameter

        self.Title = "Edit parameter"

        self.value_parameter = part.value_parameter
        
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

        if part_parameter.text_value:
            self.edit_part_parameter_value.Value = part_parameter.text_value

        if part_parameter.min_value:
            self.edit_part_parameter_min_value.Value = str(part_parameter.min_value) 
        if part_parameter.min_prefix:
            self.choice_part_parameter_min_prefix.SetSelection(part_parameter.min_prefix.id)
        else:
            self.choice_part_parameter_min_prefix.SetSelection(0)
            
        if part_parameter.nom_value:
            self.edit_part_parameter_nom_value.Value = str(part_parameter.nom_value) 
        if part_parameter.nom_prefix:
            self.choice_part_parameter_nom_prefix.SetSelection(part_parameter.nom_prefix.id)
        else:
            self.choice_part_parameter_nom_prefix.SetSelection(0)
            
        if part_parameter.max_value:
            self.edit_part_parameter_max_value.Value = str(part_parameter.max_value) 
        if part_parameter.max_prefix:
            self.choice_part_parameter_max_prefix.SetSelection(part_parameter.max_prefix.id)
        else:
            self.choice_part_parameter_max_prefix.SetSelection(0)

        if self.part.value_parameter==self.part_parameter.parameter.name:
            self.check_part_value.Value = True
        else:
            self.check_part_value.Value = False
            
            
        self._check()
            
        result = self.ShowModal()
        if result==wx.ID_OK:
            return self.part_parameter
        return None

    def onButtonPartParameterEditApply( self, event ):
        try:
            if self.part_parameter.parameter is None:
                raise ValueError('No parameter selected')
            
            if self.edit_part_parameter_value.Value!='':
                self.part_parameter.text_value = self.edit_part_parameter_value.Value
            else:
                self.part_parameter.text_value = None
                
            if self.choice_part_parameter_min_prefix.GetSelection()==0:
                self.part_parameter.min_prefix = None
            else:
                self.part_parameter.min_prefix = api.data.unit_prefix.find_by_id(self.choice_part_parameter_min_prefix.GetSelection())
            if self.edit_part_parameter_min_value.Value!='':
                if self.part_parameter.min_prefix is not None:
                    self.part_parameter.min_value = float(self.edit_part_parameter_min_value.Value)/float(self.part_parameter.min_prefix.power)
            else:
                self.part_parameter.min_value = None
    
            if self.choice_part_parameter_nom_prefix.GetSelection()==0:
                self.part_parameter.nom_prefix = None
            else:
                self.part_parameter.nom_prefix = api.data.unit_prefix.find_by_id(self.choice_part_parameter_nom_prefix.GetSelection())
            if self.edit_part_parameter_nom_value.Value!='':
                if self.part_parameter.nom_prefix is not None:
                    self.part_parameter.nom_value = float(self.edit_part_parameter_nom_value.Value)/float(self.part_parameter.nom_prefix.power)
            else:
                self.part_parameter.nom_value = None

            if self.choice_part_parameter_max_prefix.GetSelection()==0:
                self.part_parameter.max_prefix = None
            else:
                self.part_parameter.max_prefix = api.data.unit_prefix.find_by_id(self.choice_part_parameter_max_prefix.GetSelection())
            if self.edit_part_parameter_max_value.Value!='':
                if self.part_parameter.max_prefix is not None:
                    self.part_parameter.max_value = float(self.edit_part_parameter_max_value.Value)/float(self.part_parameter.max_prefix.power)
            else:
                self.part_parameter.max_value = None
                
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

    def onButtonPartParameterEditCancel( self, event ):
        self.part.value_parameter = self.value_parameter
        
        self.EndModal(wx.ID_CANCEL)
    
    def onRadioNumeric( self, event ):
        self.static_value.Hide()
        self.edit_part_parameter_value.Hide()
        
        self.static_min_value.Show()
        self.edit_part_parameter_min_value.Show()
        self.choice_part_parameter_min_prefix.Show()
        
        self.static_nom_value.Show()
        self.edit_part_parameter_nom_value.Show()
        self.choice_part_parameter_nom_prefix.Show()
        
        self.static_max_value.Show()
        self.edit_part_parameter_max_value.Show()
        self.choice_part_parameter_max_prefix.Show()
        
        self._check()
        
    def onRadioText( self, event ):
        self.static_value.Show()
        self.edit_part_parameter_value.Show()

        self.static_min_value.Hide()
        self.edit_part_parameter_min_value.Hide()
        self.choice_part_parameter_min_prefix.Hide()
        
        self.static_nom_value.Hide()
        self.edit_part_parameter_nom_value.Hide()
        self.choice_part_parameter_nom_prefix.Hide()
        
        self.static_max_value.Hide()
        self.edit_part_parameter_max_value.Hide()
        self.choice_part_parameter_max_prefix.Hide()
        
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
        
    def CheckPartParameterValueChanged( self, event ):
        self._check()
        if self.check_part_value.Value:
            self.part.value_parameter = self.part_parameter.parameter.name
        else:
            self.part.value_parameter = None
        event.Skip()

    def EditPartParameterValueChanged( self, event ):
        self._check()
        event.Skip()
