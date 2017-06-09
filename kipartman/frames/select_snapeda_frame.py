from dialogs.panel_select_snapeda import PanelSelectSnapeda
from snapeda.queries import PartsQuery
import wx.dataview
import wx.lib.newevent

SelectSnapedaOkEvent, EVT_SELECT_SNAPEDA_OK_EVENT = wx.lib.newevent.NewEvent()
SelectSnapedaCancelEvent, EVT_SELECT_SNAPEDA_APPLY_EVENT = wx.lib.newevent.NewEvent()

class SnapedaDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, searchpart):
        super(SnapedaDataModel, self).__init__()
        if searchpart!='':
            q = PartsQuery()
            q.get(searchpart)
            self.data = q.results()
        else:
            self.data = []
            
    def GetColumnCount(self):
        return 6

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'long',
            3 : 'string',
            4 : 'string',
            5 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            snapeda_len = 0
            for snapeda in self.data:
                if snapeda.has_footprint():
                    children.append(self.ObjectToItem(snapeda))
                    snapeda_len = snapeda_len+1
            return snapeda_len
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : obj.manufacturer(),
            1 : obj.name(),
            2 : str(obj.pin_count()),
            3 : obj.package_type(),
            4 : obj.short_description(),
            5 : obj._links().self().href(),
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
            
class SelectSnapedaFrame(PanelSelectSnapeda):
    def __init__(self, parent, initial_search=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectSnapedaFrame, self).__init__(parent)

        self.search_snapeda.Value = initial_search
    
        # create snapedas list
        self.snapedas_model = SnapedaDataModel(initial_search)
        self.tree_snapedas.AssociateModel(self.snapedas_model)
        # add default columns
        self.tree_snapedas.AppendTextColumn("Manufacturer", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_snapedas.AppendTextColumn("Part", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_snapedas.AppendTextColumn("Pin Count", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_snapedas.AppendTextColumn("Package Type", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_snapedas.AppendTextColumn("Description", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_snapedas.AppendTextColumn("URL", 5, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_snapedas.Columns:
            c.Sortable = True

        # set result functions
        self.cancel = None
        self.result = None
    
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
    
    def _search(self):
        # apply new filter and reload
        self.snapedas_model.Cleared()
        self.snapedas_model = SnapedaDataModel(self.search_snapeda.Value)
        self.tree_snapedas.AssociateModel(self.snapedas_model)

    # Virtual event handlers, overide them in your derived class
    def onSearchSnapedaButton( self, event ):
        self._search()
    
    def onSearchSnapedaEnter( self, event ):
        self._search()
    
    def onButtonCancelClick( self, event ):
        event = SelectSnapedaCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        sel = self.tree_snapedas.GetSelection()
        if not sel:
            return
        snapeda = self.snapedas_model.ItemToObject(self.tree_snapedas.GetSelection())
        
        # trigger result event
        event = SelectSnapedaOkEvent(data=snapeda)
        wx.PostEvent(self, event)
        if self.result:
            self.result(snapeda)
