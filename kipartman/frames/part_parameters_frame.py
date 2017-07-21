from dialogs.panel_part_parameters import PanelPartParameters
from frames.edit_part_parameter_frame import EditPartParameterFrame
import helper.tree

class DataModelPartParameter(helper.tree.TreeContainerItem):
    def __init__(self, parameter):
        super(DataModelPartParameter, self).__init__()
        self.parameter = parameter

    def value_string(self, value, prefix, unit):
        res = ""
        if value is None:
            return res
        res = res+"%g"%value+" "
        if not prefix is None:
            res = res+prefix.symbol
        if not unit is None:
            res = res+unit.symbol
        return res

    def min_string(self):
        return self.value_string(self.parameter.min_value, self.parameter.min_prefix, self.parameter.unit)
    def nom_string(self):
        return self.value_string(self.parameter.nom_value, self.parameter.nom_prefix, self.parameter.unit)
    def max_string(self):
        return self.value_string(self.parameter.max_value, self.parameter.max_prefix, self.parameter.unit)

    def unit_string(self):
        if self.parameter.unit is None:
            return ""
        return self.parameter.unit.name

    def GetValue(self, col):
        if self.parameter.numeric==True:
            vMap = { 
                0 : self.parameter.name,
                1 : self.min_string(),
                2 : self.nom_string(),
                3 : self.max_string(),
                4 : self.unit_string(),
                5 : self.parameter.description,
            }
        else:
            vMap = { 
                0 : self.parameter.name,
                1 : "",
                2 : self.parameter.text_value,
                3 : "",
                4 : self.unit_string(),
                5 : self.parameter.description,
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
        self.tree_parameters_manager = helper.tree.TreeManager(self.tree_parameters)
        self.tree_parameters_manager.AddTextColumn("Parameter")
        self.tree_parameters_manager.AddTextColumn("Min Value")
        self.tree_parameters_manager.AddTextColumn("Nominal Value")
        self.tree_parameters_manager.AddTextColumn("Max Value")
        self.tree_parameters_manager.AddTextColumn("Unit")
        self.tree_parameters_manager.AddTextColumn("Description")

        # set result functions
        self.cancel = None
        self.result = None
        
        self.enable(False)
        
    def SetResult(self, result, cancel=None):
        """
        Callbacks for parent dialog
        """
        self.result = result
        self.cancel = cancel
    
    def SetPart(self, part):
        self.part = part
        self.showParameters()
    
    def enable(self, enabled=True):
        self.button_add_parameter.Enabled = enabled
        self.button_edit_parameter.Enabled = enabled
        self.button_remove_parameter.Enabled = enabled

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
        self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(parameter))

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
                self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(parameter))
            
    def onButtonAddParameterClick( self, event ):
        parameter = EditPartParameterFrame(self).AddParameter(self.part)
        if not parameter is None:
            self.part.parameters.append(parameter)
            self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(parameter))
    
    def onButtonEditParameterClick( self, event ):
        item = self.tree_parameters.GetSelection()
        if item.IsOk()==False:
            return
        parameterobj = self.tree_parameters_manager.ItemToObject(item)

        parameter = EditPartParameterFrame(self).EditParameter(self.part, parameterobj.parameter)
        self.tree_parameters_manager.UpdateItem(parameterobj)
        
    def onButtonRemoveParameterClick( self, event ):
        item = self.tree_parameters.GetSelection()
        if item.IsOk()==False:
            return
        parameterobj = self.tree_parameters_manager.ItemToObject(item)
        self.part.parameters.remove(parameterobj.parameter)
        self.tree_parameters_manager.DeleteItem(None, parameterobj)
