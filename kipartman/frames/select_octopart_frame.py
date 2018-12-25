from dialogs.panel_select_octopart import PanelSelectOctopart
from octopart.queries import PartsQuery
import wx.dataview
import wx.lib.newevent
import helper.tree
from octopart.extractor import OctopartExtractor
import helper.tree_parameters

SelectOctopartOkEvent, EVT_SELECT_OCTOPART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectOctopartCancelEvent, EVT_SELECT_OCTOPART_APPLY_EVENT = wx.lib.newevent.NewEvent()

class DataColumnParameter(object):
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name

class DataModelOctopart(helper.tree.TreeContainerItem):
    def __init__(self, tree_model, octopart):
        super(DataModelOctopart, self).__init__()
        self.model = tree_model
        self.octopart = octopart
        
        self.extractor = OctopartExtractor(octopart)

        parameters = self.extractor.ExtractParameters()
        self.parameters = {}
        for param in parameters:
            self.parameters[param['name']] = param 

    def GetValue(self, col):
        if col<7:
            reference = self.extractor.ExtractReference()
            vMap = { 
                0 : reference['manufacturer'],
                1 : reference['description'],
                2 : reference['name'],
                3 : str(len(self.octopart.item().offers())),
                4 : str(len(self.octopart.item().datasheets())),
                5 : str(len(self.octopart.item().specs())),
                6 : self.octopart.item().octopart_url(), #TODO
            }
            if vMap[col] is None:
                return ""
            return vMap[col]
        elif self.model.GetColumnName(col) in self.parameters:
            return self.parameters[self.model.GetColumnName(col)]['display_value']
#            return self.FormatParameter(self.parameters[self.model.GetColumnName(col)])
        else:
            return ''

class TreeManagerOctopart(helper.tree_parameters.TreeManagerParameters):
    def __init__(self, tree_view):
        super(TreeManagerOctopart, self).__init__(tree_view)

    def AppendOctopart(self, octopart):
        octopartobj = DataModelOctopart(self.model, octopart)
        self.AppendItem(None, octopartobj)
        return octopartobj
  
class SelectOctopartFrame(PanelSelectOctopart):
    def __init__(self, parent, initial_search=None, multiselect=False): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectOctopartFrame, self).__init__(parent)

        self.search_octopart.Value = initial_search
    
        # create octoparts list
        self.tree_octoparts_manager = TreeManagerOctopart(self.tree_octoparts)
        self.tree_octoparts_manager.AddTextColumn("Manufacturer")
        self.tree_octoparts_manager.AddTextColumn("Description")
        self.tree_octoparts_manager.AddTextColumn("Name")
        self.tree_octoparts_manager.AddIntegerColumn("Offers")
        self.tree_octoparts_manager.AddIntegerColumn("Datasheets")
        self.tree_octoparts_manager.AddIntegerColumn("Parameters")
        self.tree_octoparts_manager.AddTextColumn("Details")

        # set result functions
        self.cancel = None
        self.result = None
    
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
    
    def search(self):
        # apply new filter and reload
        self.tree_octoparts_manager.ClearItems()
        self.tree_octoparts_manager.RemoveColumns(7)
                
        q = PartsQuery()
        q.get(self.search_octopart.Value)

        columns = {}
        for octopart in q.results():
            for spec in octopart.item().specs():
                columns[spec] = None
        for spec in columns:
            column = self.tree_octoparts_manager.AddParameterColumn(spec)
            columns[spec] = DataColumnParameter(spec)
           
        for octopart in q.results():
            self.tree_octoparts_manager.AppendOctopart(octopart)

    # Virtual event handlers, overide them in your derived class
    def onSearchOctopartButton( self, event ):
        self.search()
    
    def onSearchOctopartEnter( self, event ):
        self.search()
    
    def onButtonCancelClick( self, event ):
        event = SelectOctopartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        parts = []
        for item in self.tree_octoparts.GetSelections():
            obj = self.tree_octoparts_manager.ItemToObject(item)
            if isinstance(obj, DataModelOctopart):
                parts.append(obj.octopart)

        # trigger result event
        event = SelectOctopartOkEvent(data=parts)
        wx.PostEvent(self, event)
        if self.result:
            self.result(parts)
