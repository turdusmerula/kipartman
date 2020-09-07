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
        self.part_parameter = parameter
    
    def GetValue(self, col):
        unit_symbol = ''
        if self.part_parameter.parameter.unit is not None:
            unit_symbol = self.part_parameter.parameter.unit.symbol
        
        if col==0:
            if self.part.value_parameter is not None and self.part.value_parameter==self.part_parameter.parameter.name:
                return True
            return False
        elif col==1:
            return self.part_parameter.parameter.name
        elif col==5:
            if self.part_parameter.parameter.unit:
                return self.part_parameter.parameter.unit.name
        elif col==6:
            return self.part_parameter.parameter.description
        
        if self.part_parameter.parameter.numeric==True:
            if col==2:
                if self.part_parameter.nom_value is not None:
                    return format_unit_prefix(self.part_parameter.nom_value, unit_symbol)
            elif col==3:
                if self.part_parameter.min_value is not None:
                    return format_unit_prefix(self.part_parameter.min_value, unit_symbol)
            elif col==4:
                if self.part_parameter.max_value is not None:
                    return format_unit_prefix(self.part_parameter.max_value, unit_symbol)
        else:
            if col==2:
                return self.part_parameter.text_value
            
        return ""

    def GetAttr(self, col, attr):
        res = False
        if self.part_parameter.id is None:
            attr.SetColour(helper.colors.GREEN_NEW_ITEM)
            res = True
        if self.part_parameter.removed_pending():
            attr.SetStrikethrough(True)
            res = True
        return res
    
class TreeManagerPartParameter(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartParameter, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for parameter in self.part.parameters.all():
                parameterobj = self.FindParameter(parameter)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    parameterobj.part = self.part
                    parameterobj.part_parameter = parameter
                    self.Update(parameterobj)

            # add not yet persisted data
            for parameter in self.part.parameters.pendings():
                parameterobj = self.FindParameter(parameter)
                if parameterobj is None:
                    parameterobj = PartParameter(parameter.part, parameter)
                    self.Append(None, parameterobj)
                else:
                    parameterobj.part = self.part
                    parameterobj.part_parameter = parameter
                    self.Update(parameterobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindParameter(self, parameter):
        for data in self.data:
            if isinstance(data, PartParameter) and (data.part_parameter.id is not None and data.part_parameter.id==parameter.id) or data.part_parameter==parameter:
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
#         self.tree_parameters_manager.OnItemValueChanged = self.onTreeParametersItemValueChanged

        self.editing = False    # indicate if value changed by editing or clicking

        self.tree_parameters_manager.Clear()
        self.SetPart(None)
                
    def SetPart(self, part):
        self.updating = True

        self.part = part
        self.tree_parameters_manager.SetPart(part)
        self._enable(False)
        
        self.updating = False
        
    def EditPart(self, part):
        self.updating = True

        self.part = part
        self.tree_parameters_manager.SetPart(part)
        self._enable(True)
        
        self.updating = False

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

#     def onTreeParametersItemValueChanged( self, event ):
#         if self.editing==True:
#             self.editing = False
#             return
#         
#         if self.Enabled==False:
#             return
#         item = event.Item#self.tree_parameters.GetSelection()
#         if item.IsOk()==False:
#             return
#         parameterobj = self.tree_parameters_manager.ItemToObject(item)

#         self.updating = True
#         if self.part.value_parameter is not None and parameterobj.part_parameter.parameter.name==self.part.value_parameter:
#             self.part.value_parameter = None
#         else:
#             self.part.value_parameter = parameterobj.part_parameter.parameter.name
        
    def onMenuParameterAddParameter( self, event ):
        EditPartParameterFrame(self).AddParameter(self.part)
        self.tree_parameters_manager.Load()
        
    def onMenuParameterEditParameter( self, event ):
        item = self.tree_parameters.GetSelection()
        if item.IsOk()==False:
            return
        part_parameterobj = self.tree_parameters_manager.ItemToObject(item)

        EditPartParameterFrame(self).EditParameter(self.part, part_parameterobj.part_parameter)
        self.tree_parameters_manager.Load()

    def onMenuParameterRemoveParameter( self, event ):
        parameters = []
        for item in self.tree_parameters.GetSelections():
            obj = self.tree_parameters_manager.ItemToObject(item)
            parameters.append(obj)
 
        for parameterobj in parameters:
            if parameterobj.part_parameter.id is None:
                self.tree_parameters_manager.Remove(parameterobj)
            else:
                self.part.parameters.remove_pending(parameterobj.part_parameter)
        self.tree_parameters_manager.Load()
#  
