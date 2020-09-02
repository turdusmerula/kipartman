from dialogs.panel_part_parameters import PanelPartParameters
from frames.edit_part_parameter_frame import EditPartParameterFrame
import helper.tree
from helper.unit import format_unit_prefix
from helper.log import log
import api.data.part_parameter

class PartParameter(helper.tree.TreeContainerItem):
    def __init__(self, part, parameter):
        super(PartParameter, self).__init__()
        self.part = part
        self.parameter = parameter
    
    def GetValue(self, col):
        unit_symbol = ''
        if self.parameter.unit:
            unit_symbol = self.parameter.unit.symbol
        
        
        if col==0:
            if self.part.value_parameter and self.part.value_parameter==self.parameter.name:
                return True
            return False
        elif col==1:
            return self.parameter.name
        elif col==5:
            if self.parameter.unit:
                return self.parameter.unit.name
        elif col==6:
            return self.parameter.description
        
        if self.parameter.numeric==True:
            if col==2:
                if self.parameter.nom_value is not None:
                    return format_unit_prefix(self.parameter.nom_value, unit_symbol)
            elif col==3:
                if self.parameter.min_value is not None:
                    return format_unit_prefix(self.parameter.min_value, unit_symbol)
            elif col==4:
                if self.parameter.max_value is not None:
                    return format_unit_prefix(self.parameter.max_value, unit_symbol)
        else:
            if col==2:
                return self.parameter.text_value
            
        return ""

class TreeManagerPartParameter(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartParameter, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for parameter in api.data.part_parameter.find([api.data.part_parameter.FilterPart(self.part)]):
                parameterobj = self.FindParameter(parameter.id)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    parameterobj.parameter = parameter
                    self.Update(parameterobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindParameter(self, id):
        for data in self.data:
            if isinstance(data, PartParameter) and data.parameter.id==id:
                return data
        return None

class PartParametersFrame(PanelPartParameters):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartParametersFrame, self).__init__(parent)
        
        # create parameters list
        self.tree_parameters_manager = TreeManagerPartParameter(self.tree_parameters, context_menu=self.menu_parameter)
        self.tree_parameters_manager.AddToggleColumn("*")
        self.tree_parameters_manager.AddTextColumn("Parameter")
        self.tree_parameters_manager.AddTextColumn("Value")
        self.tree_parameters_manager.AddTextColumn("Min")
        self.tree_parameters_manager.AddTextColumn("Max")
        self.tree_parameters_manager.AddTextColumn("Unit")
        self.tree_parameters_manager.AddTextColumn("Description")
        self.tree_parameters_manager.OnItemBeforeContextMenu = self.onTreeParametersBeforeContextMenu
        self.tree_parameters_manager.OnItemValueChanged = self.onTreeParametersItemValueChanged

        self.editing = False    # indicate if value changed by editing or clicking
        
        self.tree_parameters_manager.Clear()
        self.SetPart(None)
        
     
    def SetPart(self, part):
        self.tree_parameters_manager.SetPart(part)
        self._enable(False)
        
    def EditPart(self, part):
        self.tree_parameters_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled



#     def AddParameter(self, parameter):
#         """
#         Add a parameter to the part, or update if parameter already exists
#         """
#         # check if parameter exists
#         if self.ExistParameter(parameter.name):
#             # update existing parameter
#             self.RemoveParameter(parameter.name)
#         
#         # add parameter
#         if self.part.parameters is None:
#             self.part.parameters = []
#         self.part.parameters.append(parameter)
#         self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))
# 
#     def ExistParameter(self, name):
#         """
#         Test if a parameter exists by its name
#         """
#         if not self.part.parameters:
#             return False
#         for param in self.part.parameters:
#             if param.name==name:
#                 return True
#         return False
# 
#     def FindParameter(self, name):
#         for data in self.tree_parameters_manager.data:
#             if data.parameter.name==name:
#                 return data
#         return None
#         
# 
#     def RemoveParameter(self, name):
#         """
#         Remove a parameter using its name
#         """
#         if not self.part.parameters:
#             return False
#         
#         parameterobj = self.FindParameter(name)
#         self.part.parameters.remove(parameterobj.parameter)
#         self.tree_parameters_manager.DeleteItem(None, parameterobj)
# 
# 
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
#             
#     def onTreeParametersItemStartEditing( self, event ):
#         log.debug("onTreeParametersItemStartEditing")
#         
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
#         
#     def onMenuParameterAddParameter( self, event ):
#         parameter = EditPartParameterFrame(self).AddParameter(self.part)
#         if not parameter is None:
#             self.part.parameters.append(parameter)
#             self.tree_parameters_manager.AppendItem(None, DataModelPartParameter(self.part, parameter))
#     
#     def onMenuParameterEditParameter( self, event ):
#         item = self.tree_parameters.GetSelection()
#         if item.IsOk()==False:
#             return
#         parameterobj = self.tree_parameters_manager.ItemToObject(item)
# 
#         parameter = EditPartParameterFrame(self).EditParameter(self.part, parameterobj.parameter)
#         self.editing = True
#         self.tree_parameters_manager.UpdateItem(parameterobj)
#         
#     def onMenuParameterRemoveParameter( self, event ):
#         parameters = []
#         for item in self.tree_parameters.GetSelections():
#             obj = self.tree_parameters_manager.ItemToObject(item)
#             parameters.append(obj)
# 
#         for parameterobj in parameters:
#             self.part.parameters.remove(parameterobj.parameter)
#             self.tree_parameters_manager.DeleteItem(None, parameterobj)
#  
