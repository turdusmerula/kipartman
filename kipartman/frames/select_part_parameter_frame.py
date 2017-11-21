from dialogs.panel_select_part_parameter import PanelSelectPartParameter
import helper.tree
import rest
import wx

    
class DataModelPartParameter(helper.tree.TreeItem):
    def __init__(self, part_parameter):
        super(DataModelPartParameter, self).__init__()
        self.part_parameter = part_parameter
            
    def unit_string(self):
        if self.part_parameter.unit is None:
            return ""
        return self.part_parameter.unit.name+" ("+self.part_parameter.unit.symbol+")"

    def numeric(self):
        if self.part_parameter.numeric:
            return "true"
        return "false"

    def GetValue(self, col):
        vMap = { 
            0 : self.part_parameter.name,
            1 : self.part_parameter.description,
            2 : self.unit_string(),
            3 : self.numeric(),
        }
        return vMap[col]


class TreeManagerPartParameters(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerPartParameters, self).__init__(tree_view)

    def FindPartParameter(self, name):
        for data in self.data:
            if isinstance(data, DataModelPartParameter) and data.part_parameter.name==name:
                return data
        return None


class SelectPartParameterFrame(PanelSelectPartParameter):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: parameter name to select by default
        """
        super(SelectPartParameterFrame, self).__init__(parent)
        
        # create part_parameters list
        self.tree_part_parameters_manager = TreeManagerPartParameters(self.tree_part_parameters)
        self.tree_part_parameters_manager.AddTextColumn("Name")
        self.tree_part_parameters_manager.AddTextColumn("Description")
        self.tree_part_parameters_manager.AddTextColumn("Unit")
        self.tree_part_parameters_manager.AddTextColumn("Numeric")
        
        self.search_filter = None
        self.search_part_parameter.Value = ''
        self.load()
        
        if initial:
            self.tree_part_parameters.Select(self.tree_part_parameters_manager.ObjectToItem(self.tree_part_parameters_manager.FindPartParameter(initial)))
        
        # set result functions
        self.cancel = None
        self.result = None

    def load(self):
        try:
            self.loadPartsParameters()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def loadPartsParameters(self):
        # clear all
        self.tree_part_parameters_manager.ClearItems()
        
        # load parts
        if self.search_filter:
            part_parameters = rest.api.find_parts_parameters(search=self.search_filter)
        else:
            part_parameters = rest.api.find_parts_parameters()
            
        for part_parameter in part_parameters:
            self.tree_part_parameters_manager.AppendItem(None, DataModelPartParameter(part_parameter))
        
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreePartParametersSelectionChanged( self, event ):
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        part_parameter = self.tree_part_parameters_manager.ItemToObject(self.tree_part_parameters.GetSelection())
        if isinstance(part_parameter, DataModelPartParameter) and self.result:
            self.result(part_parameter.part_parameter)

    def onSearchPartParameterCancel( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchPartParameterButton( self, event ):
        self.search_filter = self.search_part_parameter.Value
        self.load()
    
    def onSearchPartParameterEnter( self, event ):
        self.search_filter = self.search_part_parameter.Value
        self.load()
