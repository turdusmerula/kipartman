from dialogs.panel_select_octopart import PanelSelectOctopart
from octopart.queries import PartsQuery
import wx.dataview
import wx.lib.newevent

SelectOctopartOkEvent, EVT_SELECT_OCTOPART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectOctopartCancelEvent, EVT_SELECT_OCTOPART_APPLY_EVENT = wx.lib.newevent.NewEvent()

class OctopartDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, searchpart):
        super(OctopartDataModel, self).__init__()
        if searchpart!='':
            q = PartsQuery()
            q.get(searchpart)
            self.data = q.results()
        else:
            self.data = []
            
    def GetColumnCount(self):
        return 7

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'string',
            3 : 'long',
            4 : 'long',
            5 : 'long',
            6 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for octopart in self.data:
                children.append(self.ObjectToItem(octopart))
            return len(self.data)
        return 0
    
    def IsContainer(self, item):
        if not item:
            return True
        else:
            return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : obj.item().manufacturer().name(),
            1 : obj.snippet(),
            2 : obj.item().mpn(),
            3 : str(len(obj.item().offers())),
            4 : str(len(obj.item().datasheets())),
            5 : str(len(obj.item().specs())),
            6 : obj.item().octopart_url(), #TODO
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False

#     def HasDefaultCompare(self):
#         return False
#     
#     def Compare(self, item1, item2, column, ascending):
        #TODO allow sort integer columns properly
            
class SelectOctopartFrame(PanelSelectOctopart):
    def __init__(self, parent, initial_search=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectOctopartFrame, self).__init__(parent)

        self.search_octopart.Value = initial_search
    
        # create octoparts list
        self.octoparts_symbol = OctopartDataModel(initial_search)
        self.tree_octoparts.AssociateSymbol(self.octoparts_symbol)
        # add default columns
        self.tree_octoparts.AppendTextColumn("Manufacturer", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Description", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Name", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Offers", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Datasheets", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Parameters", 5, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Details", 6, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_octoparts.Columns:
            c.Sortable = True

        # set result functions
        self.cancel = None
        self.result = None
    
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
    
    def _search(self):
        # apply new filter and reload
        self.octoparts_symbol.Cleared()
        self.octoparts_symbol = OctopartDataModel(self.search_octopart.Value)
        self.tree_octoparts.AssociateSymbol(self.octoparts_symbol)

   # Virtual event handlers, overide them in your derived class
    def onSearchOctopartButton( self, event ):
        self._search()
    
    def onSearchOctopartEnter( self, event ):
        self._search()
    
    def onButtonCancelClick( self, event ):
        event = SelectOctopartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        sel = self.tree_octoparts.GetSelection()
        if not sel:
            return
        octopart = self.octoparts_symbol.ItemToObject(self.tree_octoparts.GetSelection())
        
        # trigger result event
        event = SelectOctopartOkEvent(data=octopart)
        wx.PostEvent(self, event)
        if self.result:
            self.result(octopart)
