from dialogs.panel_select_snapeda import PanelSelectSnapeda
from snapeda.queries import PartsQuery
import wx.dataview
import wx.lib.newevent
import helper.tree

SelectSnapedaOkEvent, EVT_SELECT_SNAPEDA_OK_EVENT = wx.lib.newevent.NewEvent()
SelectSnapedaCancelEvent, EVT_SELECT_SNAPEDA_APPLY_EVENT = wx.lib.newevent.NewEvent()

def NoneValue(value, default):
    if value:
        return value
    return default

class DataModelSnapedaPart(helper.tree.TreeItem):
    def __init__(self, part):
        super(DataModelSnapedaPart, self).__init__()
        self.part = part
            
    def GetValue(self, col):
        vMap = { 
            0 : self.part.manufacturer(),
            1 : self.part.name(),
            2 : str(NoneValue(self.part.pin_count(), '')),
            3 : self.part.package_type(),
            4 : self.part.short_description(),
            5 : self.part._links().self().href(),
        }
        return vMap[col]

            
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
        self.tree_snapeda_manager = helper.tree.TreeManager(self.tree_snapedas)
        self.tree_snapeda_manager.AddTextColumn("Manufacturer")
        self.tree_snapeda_manager.AddTextColumn("Part")
        self.tree_snapeda_manager.AddIntegerColumn("Pin Count")
        self.tree_snapeda_manager.AddTextColumn("Package Type")
        self.tree_snapeda_manager.AddTextColumn("Description")
        self.tree_snapeda_manager.AddTextColumn("URL")

        # set result functions
        self.cancel = None
        self.result = None
    
        self.search()
                
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
    
    def search(self):
        # apply new filter and reload
        self.tree_snapeda_manager.ClearItems()
        if self.search_snapeda.Value!='':
            q = PartsQuery()
            q.get(self.search_snapeda.Value)
            
            for snapeda in q.results():
                if snapeda.has_footprint():
                    self.tree_snapeda_manager.AppendItem(None, DataModelSnapedaPart(snapeda))

    # Virtual event handlers, overide them in your derived class
    def onSearchSnapedaButton( self, event ):
        self.search()
    
    def onSearchSnapedaEnter( self, event ):
        self.search()
    
    def onButtonCancelClick( self, event ):
        event = SelectSnapedaCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        sel = self.tree_snapedas.GetSelection()
        if not sel:
            return
        snapeda = self.tree_snapeda_manager.ItemToObject(self.tree_snapedas.GetSelection())
        
        # trigger result event
        event = SelectSnapedaOkEvent(data=snapeda.part)
        wx.PostEvent(self, event)
        if self.result:
            self.result(snapeda.part)
