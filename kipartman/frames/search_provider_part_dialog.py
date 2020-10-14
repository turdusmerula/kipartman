from dialogs.dialog_provider_search_part import DialogProviderSearchPart
import wx.dataview
import wx.lib.newevent
import helper.tree
from helper.exception import print_stack
from frames.wait_dialog import WaitDialog

SelectPartOkEvent, EVT_SELECT_PART_OK_EVENT = wx.lib.newevent.NewEvent()

class ColumnParameter(object):
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
 
class Part(helper.tree.TreeItem):
    def __init__(self, part, columns):
        super(Part, self).__init__()
#         self.model = tree_model
        self.part = part
        self.columns = columns
         
    def GetValue(self, col):
        if col==0:
            return self.part.manufacturer
        elif col==1:
            return self.part.description
        elif col==2:
            return self.part.name
        elif col==3:
            return len(self.part.offers)
        else:
            param_name = self.columns[col]
            for param in self.part.parameters:
                if param.name==param_name:
                    return param.value
            return "-"
        
        return ""
 
class TreeManagerProviderPart(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerProviderPart, self).__init__(tree_view, *args, **kwargs)
        
        self.AddTextColumn("Manufacturer")
        self.AddTextColumn("Description")
        self.AddTextColumn("Name")
        self.AddIntegerColumn("Offers")
        
        self.parts = []
        self.columns = {}
        
    def Load(self):
        for part in self.parts:
            partobj = Part(part, self.columns)
            self.Append(None, partobj)
    
    def SetParts(self, parts):
        self.parts = parts

        # add parameters columns
        columns = []
        for part in parts:
            for parameter in part.parameters:
                if parameter.name not in columns:
                    columns.append(parameter.name)
        
        index = 4
        self.columns = {}
        self.RemoveColumns(start_index=index)
        columns.sort()
        for column in columns:
            self.AddTextColumn(column)
            self.columns[index] = column
            index += 1
    
        self.Load()
   
class SelectProviderPartDialog(DialogProviderSearchPart):
    def __init__(self, parent, provider, initial_search=None, multiselect=False): 
        super(SelectProviderPartDialog, self).__init__(parent)

        self.provider = provider
        if initial_search is not None:
            self.search_text.Value = initial_search
#     
#         # create octoparts list
        self.tree_provider_part_manager = TreeManagerProviderPart(self.tree_parts)
#
        self.tree_provider_part_manager.Clear()
        
    def onSearchEnter( self, event ):
        # TODO add asynchronous search capabilities
#         wait_dialog = WaitDialog(self)
#         wait_dialog.Request(self.result, self.req, 10)
        parts = self.provider().SearchPart(self.search_text.Value)
        
        self.tree_provider_part_manager.Clear()        
        self.tree_provider_part_manager.SetParts(parts)
        
        event.Skip()

    def onSearchCancel( self, event ):
        self.tree_provider_part_manager.Clear()
        event.Skip()

    def onButtonCancelClick( self, event ):
        event.Skip()

    def onButtonOkClick( self, event ):
        parts = []
        for item in self.tree_parts.GetSelections():
            obj = self.tree_octoparts_manager.ItemToObject(item)
            if isinstance(obj, Part):
                parts.append(obj.part)
 
        # trigger result event
        event = SelectPartOkEvent(data=parts)
        wx.PostEvent(self, event)
        event.Skip()
