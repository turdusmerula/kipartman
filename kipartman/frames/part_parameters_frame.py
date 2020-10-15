from dialogs.panel_part_parameters import PanelPartParameters
from frames.edit_part_parameter_frame import EditPartParameterFrame
from frames.models.tree_manager_part_parameters import PartParameter, TreeManagerPartParameter
from helper.log import log
import api.data.part_parameter


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
        self.tree_parameters_manager.OnItemBeforeContextMenu = self.onTreeParametersBeforeContextMenu

        self.tree_parameters_manager.Clear()
        self.SetPart(None)
                
        self._enable(False)

    def SetPart(self, part):
        self.part = part
        self.tree_parameters_manager.SetPart(part)
        self._enable(False)
        
    def EditPart(self, part):
        self.part = part
        self.tree_parameters_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled

    def Save(self, part):
        pass

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
        
    def onMenuParameterAddParameter( self, event ):
        EditPartParameterFrame(self).AddPartParameter(self.part)
        self.tree_parameters_manager.Load()
        
    def onMenuParameterEditParameter( self, event ):
        item = self.tree_parameters.GetSelection()
        if item.IsOk()==False:
            return
        part_parameterobj = self.tree_parameters_manager.ItemToObject(item)

        EditPartParameterFrame(self).EditPartParameter(self.part, part_parameterobj.part_parameter)
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
