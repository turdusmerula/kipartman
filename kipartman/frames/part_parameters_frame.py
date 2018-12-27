from dialogs.panel_part_parameters import PanelPartParameters
from frames.edit_part_parameter_frame import EditPartParameterFrame
import helper.tree
import helper.tree_parameters
from helper.unit import format_unit_prefix

class DataModelPartParameter(helper.tree.TreeContainerItem):
    def __init__(self, part, parameter):
        super(DataModelPartParameter, self).__init__()
        self.part = part
        self.parameter = parameter

    def HasValue(self, column):
        return True
    
    def IsNumeric(self, column):
        return self.parameter.numeric

    def GetUnit(self, column):
        if self.parameter.unit:
            return self.parameter.unit.name
        return None
    
    def GetNumericValue(self, col):
        return self.parameter.nom_value

    def GetValue(self, col):
        value_parameter = False
        if self.part.value_parameter and self.part.value_parameter==self.parameter.name:
            value_parameter = True
        
        unit_symbol = ''
        unit_name = ''
        if self.parameter.unit:
            unit_symbol = self.parameter.unit.symbol
            unit_name = self.parameter.unit.name
        
        min_value = ''
        if self.parameter.min_value is not None:
            min_value = format_unit_prefix(self.parameter.min_value, unit_symbol)
            
        nom_value = ''
        if self.parameter.nom_value is not None:
            nom_value = format_unit_prefix(self.parameter.nom_value, unit_symbol)

        max_value = ''
        if self.parameter.max_value is not None:
            max_value = format_unit_prefix(self.parameter.max_value, unit_symbol)

        if self.parameter.numeric==True:
            vMap = {
                0 : value_parameter,
                1 : self.parameter.name,
                2 : nom_value,
                3 : min_value,
                4 : max_value,
                5 : unit_name,
                6 : self.parameter.description,
            }
        else:
            vMap = { 
                0 : value_parameter,
                1 : self.parameter.name,
                2 : self.parameter.text_value,
                3 : "",
                4 : "",
                5 : unit_name,
                6 : self.parameter.description,
            }
        return vMap[col]

    def IsContainer(self):
        return False

class PartParametersFrame(PanelPartParameters):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartParametersFrame, self).__init__(parent)
        
        # create parameters list
        self.tree_parameters_manager = helper.tree_parameters.TreeManagerParameters(self.tree_parameters, context_menu=self.menu_parameter)
        self.tree_parameters_manager.AddToggleColumn("*")
        self.tree_parameters_manager.AddTextColumn("Parameter")
        self.tree_parameters_manager.AddParameterColumn("Value")
        self.tree_parameters_manager.AddParameterColumn("Min")
        self.tree_parameters_manager.AddParameterColumn("Max")
        self.tree_parameters_manager.AddTextColumn("Unit")
        self.tree_parameters_manager.AddTextColumn("Description")
        self.tree_parameters_manager.OnItemBeforeContextMenu = self.onTreeParametersBeforeContextMenu
        self.tree_parameters_manager.OnItemValueChanged = self.onTreeParametersItemValueChanged

        self.editing = False    # indicate if value changed by editing or clicking
        
        self.enable(False)
        
     
    def SetPart(self, part):
        self.part = part
        self.showParameters()
    
    def enable(self, enabled=True):
        self.enabled = enabled
    
    def AddParameter(self, parameter):
        """
        Add a parameter to the part, or update if parameter already exists
        """
        # check if parameter exists
        if self.ExistParameter(parameter.name):
            # update existing parameter
            self.RemoveParameter(parameter.name)
        
        # add parameter
        if self.part.parameters is None:
            self.part.parameters = []
        self.part.parameters.append(parameter)
        self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))

    def ExistParameter(self, name):
        """
        Test if a parameter exists by its name
        """
        if not self.part.parameters:
            return False
        for param in self.part.parameters:
            if param.name==name:
                return True
        return False

    def FindParameter(self, name):
        for data in self.tree_parameters_manager.data:
            if data.parameter.name==name:
                return data
        return None
        

    def RemoveParameter(self, name):
        """
        Remove a parameter using its name
        """
        if not self.part.parameters:
            return False
        
        parameterobj = self.FindParameter(name)
        self.part.parameters.remove(parameterobj.parameter)
        self.tree_parameters_manager.DeleteItem(None, parameterobj)

    def showParameters(self):
        self.tree_parameters_manager.ClearItems()

        if self.part and self.part.parameters:
            for parameter in self.part.parameters:
                self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))

    def onTreeParametersBeforeContextMenu( self, event ):
        self.menu_parameter_add_parameter.Enable(True)
        self.menu_parameter_edit_parameter.Enable(True)
        self.menu_parameter_remove_parameter.Enable(True)

        if len(self.tree_parameters.GetSelections())==0:
            self.menu_parameter_edit_parameter.Enable(False)
            self.menu_parameter_remove_parameter.Enable(False)
        if len(self.tree_parameters.GetSelections())>1:
            self.menu_parameter_edit_parameter.Enable(False)
        
        if self.enabled==False:
            self.menu_parameter_add_parameter.Enable(False)
            self.menu_parameter_edit_parameter.Enable(False)
            self.menu_parameter_remove_parameter.Enable(False)
            
    def onTreeParametersItemStartEditing( self, event ):
        print("onTreeParametersItemStartEditing")
        
    def onTreeParametersItemValueChanged( self, event ):
        if self.editing==True:
            self.editing = False
            return
        
        if self.enabled==False:
            return
        item = self.tree_parameters.GetSelection()
        if item.IsOk()==False:
            return
        parameterobj = self.tree_parameters_manager.ItemToObject(item)
        
        if self.part.value_parameter and parameterobj.parameter.name==self.part.value_parameter:
            self.part.value_parameter = None
        else:
            self.part.value_parameter = parameterobj.parameter.name
        
    def onMenuParameterAddParameter( self, event ):
        parameter = EditPartParameterFrame(self).AddParameter(self.part)
        if not parameter is None:
            self.part.parameters.append(parameter)
            self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))
    
    def onMenuParameterEditParameter( self, event ):
        item = self.tree_parameters.GetSelection()
        if item.IsOk()==False:
            return
        parameterobj = self.tree_parameters_manager.ItemToObject(item)

        parameter = EditPartParameterFrame(self).EditParameter(self.part, parameterobj.parameter)
        self.editing = True
        self.tree_parameters_manager.UpdateItem(parameterobj)
        
    def onMenuParameterRemoveParameter( self, event ):
        parameters = []
        for item in self.tree_parameters.GetSelections():
            obj = self.tree_parameters_manager.ItemToObject(item)
            parameters.append(obj)

        for parameterobj in parameters:
            self.part.parameters.remove(parameterobj.parameter)
            self.tree_parameters_manager.DeleteItem(None, parameterobj)
 
