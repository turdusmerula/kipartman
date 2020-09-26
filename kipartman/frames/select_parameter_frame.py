from dialogs.panel_select_parameter import PanelSelectParameter
import helper.tree
import wx
from helper.exception import print_stack
import api.data.parameter

    
class Parameter(helper.tree.TreeItem):
    def __init__(self, parameter):
        super(Parameter, self).__init__()
        self.parameter = parameter
            
    def unit_string(self):
        if self.parameter.unit is None:
            return ""
        return self.parameter.unit.name+" ("+self.parameter.unit.symbol+")"

    def numeric(self):
        if self.parameter.numeric:
            return "true"
        return "false"

    def GetValue(self, col):
        if col==0:
            return self.parameter.name
        elif col==1:
            return self.parameter.description
        elif col==2:
            return self.unit_string()
        elif col==3:
            return self.numeric()

        return ""


class TreeManagerParameters(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerParameters, self).__init__(tree_view, *args, **kwargs)

        self.AddTextColumn("Name")
        self.AddTextColumn("Description")
        self.AddTextColumn("Unit")
        self.AddTextColumn("Numeric")

        self.filters = filters

    def Load(self):
        
        self.SaveState()
        
        for parameter in api.data.parameter.find(filters=self.filters.get_filters()):
            parameterobj = self.FindParameter(parameter.id)
            if parameterobj is None:
                parameterobj = Parameter(parameter)
                self.Append(None, parameterobj)
            else:
                parameterobj.parameter = parameter
                self.Update(parameterobj)
        
        self.PurgeState()

    def FindParameter(self, id):
        for data in self.data:
            if isinstance(data, Parameter) and data.parameter.id==id:
                return data
        return None


class SelectParameterFrame(PanelSelectParameter):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: parameter name to select by default
        """
        super(SelectParameterFrame, self).__init__(parent)
        
        # parameters filters
        self.filters = helper.filter.FilterSet(self)
        self.filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        if initial is not None:
            self.filters.replace(api.data.parameter.FilterSearchText(initial), 'search')
            
        # create parameters list
        self.tree_parameters_manager = TreeManagerParameters(self.tree_parameters, filters=self.filters)
        self.tree_parameters_manager.OnSelectionChanged = self.onTreeParametersSelectionChanged
        
        if initial:
            self.tree_parameters.Select(self.tree_parameters_manager.ObjectToItem(self.tree_parameters_manager.FindPartParameter(initial)))
        
        # set result functions
        self.cancel = None
        self.result = None

        # initial state
        self.button_select_parameterOK.Enabled = False            
        self.tree_parameters_manager.Clear()

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
        
    def onTreeParametersSelectionChanged( self, event ):
        item = self.tree_parameters.GetSelection()
        if item.IsOk():
            self.button_select_parameterOK.Enabled = True
        else:
            self.button_select_parameterOK.Enabled = False            
        event.Skip()
        
    def onFilterChanged( self, event ):
        self.tree_parameters_manager.Load()
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        parameter = self.tree_parameters_manager.ItemToObject(self.tree_parameters.GetSelection())
        if isinstance(parameter, Parameter) and self.result:
            self.result(parameter.parameter)

    def onSearchParameterCancel( self, event ):
        self.filters.remove_group('search')

    def onSearchParameterButton( self, event ):
        self.filters.replace(api.data.parameter.FilterSearchText(self.search_parameter.Value), 'search')
        
    def onSearchParameterEnter( self, event ):
        self.filters.replace(api.data.parameter.FilterSearchText(self.search_parameter.Value), 'search')
        event.Skip()
