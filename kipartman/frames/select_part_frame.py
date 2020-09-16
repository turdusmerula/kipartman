from dialogs.panel_select_part import PanelSelectPart
import wx
import wx.lib.newevent
import wx.dataview
from frames.models.tree_manager_parts import PartCategory, Part, TreeManagerParts
from frames.models.tree_manager_part_parameters import PartParameter, TreeManagerPartParameter
import helper.tree
import api.data

SelectPartOkEvent, EVT_SELECT_PART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectPartCancelEvent, EVT_SELECT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()

            
class SelectPartFrame(PanelSelectPart):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectPartFrame, self).__init__(parent)
    
        # parts filters
        self._filters = helper.filter.FilterSet(self)
        self._filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        
        # create part list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts, filters=self._filters)
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelectionChanged

        # create parameters list
        self.tree_parameters_manager = TreeManagerPartParameter(self.tree_parameters)

        # set result functions
        self.cancel = None
        self.result = None
        
        # initial state
        self.button_part_selectOK.Enabled = False            

        self.tree_parts_manager.Clear()
        self.tree_parts_manager.Load()
        
        self.tree_parameters_manager.Clear()

    def _expand_categories(self):
        for category in self.tree_parts_manager.FindCategories():
            self.tree_parts_manager.Expand(category)

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    def onTreePartsSelectionChanged( self, event ):
        item = self.tree_parts.GetSelection()
        if item.IsOk()==False:
            return
        partobj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(partobj, Part)==False:
            self.button_part_selectOK.Enabled = False
            self.tree_parameters_manager.SetPart(None)
            return
        
        self.button_part_selectOK.Enabled = True
        
        self.tree_parameters_manager.SetPart(partobj.part)

    def onFilterChanged( self, event ):
        self.tree_parts_manager.Load()
        self._expand_categories()
        event.Skip()

    def onButtonCancelClick( self, event ):
        event = SelectPartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        item = self.tree_parts.GetSelection()
        if item.IsOk()==False:
            return
        partobj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(partobj, Part)==False:
            return
        
        # trigger result event
        event = SelectPartOkEvent(data=partobj.part)
        wx.PostEvent(self, event)
        if self.result:
            self.result(partobj.part)

    def onSearchPartCancelButton( self, event ):
        self._filters.remove_group('search')
    
    def onSearchPartSearchButton( self, event ):
        self._filters.replace(api.data.part.FilterTextSearch(self.search_part.Value), 'search')

    def onSearchPartTextEnter( self, event ):
        self._filters.replace(api.data.part.FilterTextSearch(self.search_part.Value), 'search')

    def onButtonRefreshPartsClick( self, event ):
        self.tree_parts_manager.Load()
        self.tree_parameters_manager.Load()
