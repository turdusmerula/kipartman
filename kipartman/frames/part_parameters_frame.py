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
        self.part.parameters.append(parameter)
        self.create_list.append(parameter)
        self._showParameters()

    def ExistParameter(self, name):
        """
        Test if a parameter exists by its name
        """
        for param in self.part.parameters:
            if param.name==name:
                return True
        return False

    def RemoveParameter(self, name):
        """
        Remove a parameter using its name
        """
        for param in self.part.parameters:
            if param.name==name:
                if param.id!=-1:
                    self.remove_list.append(param)
                    self.part.parameters.remove(param)
                    # remove it from update list if present
                    try:
                        # remove it if already exists
                        self.update_list.remove(param)
                    except:
                        pass
                else:
                    self.part.parameters.remove(param)
                    

    def showParameters(self):
        self.tree_parameters_manager.ClearItems()

        if self.part and self.part.parameters:
            for parameter in self.part.parameters:
                self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(parameter))
    
    def ApplyChanges(self, part):
        for param in self.remove_list:
            param.part = part
            api.queries.PartParametersQuery().delete(param)
        self.remove_list = []

        # apply changes to current part
        for param in self.create_list:
            param.part = part
            api.queries.PartParametersQuery().create(param)
        self.create_list = []
        
        for param in self.update_list:
            param.part = part
            api.queries.PartParametersQuery().update(param)
        self.update_list = []
        
    def onButtonAddParameterClick( self, event ):
        parameter = EditPartParameterFrame(self).AddParameter(self.part)
        if not parameter is None:
            self.part.parameters.append(parameter)
            self.create_list.append(parameter)
        self._showParameters()
            
    def onButtonEditParameterClick( self, event ):
        parameter = self.parameters_model.ItemToObject(self.tree_parameters.GetSelection())
        if not parameter:
            return 
        if EditPartParameterFrame(self).EditParameter(self.part, parameter) and parameter.id!=-1:
            # set parameter to be updated
            try:
                # remove it from update list to avoid multiple update
                self.update_list.remove(parameter)
            except:
                pass
            self.update_list.append(parameter)
        self._showParameters()
    
    def onButtonRemoveParameterClick( self, event ):
        item = self.tree_parameters.GetSelection()
        if not item:
            return
        parameter = self.parameters_model.ItemToObject(item)
        self.part.parameters.remove(parameter)
        # set parameter to be removed
        if parameter.id!=-1:
            self.remove_list.append(parameter)
            try:
                # remove it from update list if present
                self.update_list.remove(parameter)
            except:
                pass

        self._showParameters()
