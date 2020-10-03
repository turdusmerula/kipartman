from dialogs.panel_select_storage import PanelSelectStorage
import wx
import wx.lib.newevent
import wx.dataview
from frames.models.tree_manager_storages import StorageCategory, Storage, TreeManagerStorages
import helper.tree
import api.data

SelectStorageOkEvent, EVT_SELECT_STORAGE_OK_EVENT = wx.lib.newevent.NewEvent()
SelectStorageCancelEvent, EVT_SELECT_STORAGE_APPLY_EVENT = wx.lib.newevent.NewEvent()


class SelectStorageFrame(PanelSelectStorage):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectStorageFrame, self).__init__(parent)
    
        # storages filters
        self._filters = helper.filter.FilterSet(self)
        self._filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        
        # create storage list
        self.tree_storages_manager = TreeManagerStorages(self.tree_storages, filters=self._filters)
        self.tree_storages_manager.OnSelectionChanged = self.onTreeStoragesSelectionChanged

        # set result functions
        self.cancel = None
        self.result = None
        
        # initial state
        self.button_storage_selectOK.Enabled = False            

        self.tree_storages_manager.Clear()
        self.tree_storages_manager.Load()

    def _expand_categories(self):
        for category in self.tree_storages_manager.FindCategories():
            self.tree_storages_manager.Expand(category)

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel

    def onTreeStoragesSelectionChanged( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(storageobj, Storage)==False:
            self.button_storage_selectOK.Enabled = False
            self.tree_parameters_manager.SetStorage(None)
            return
        
        self.button_storage_selectOK.Enabled = True
        
        self.tree_parameters_manager.SetStorage(storageobj.storage)

    def onFilterChanged( self, event ):
        self.tree_storages_manager.Load()
        self._expand_categories()
        event.Skip()
  
    def onButtonCancelClick( self, event ):
        event = SelectStorageCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(storageobj, Storage)==False:
            return
        
        # trigger result event
        event = SelectStorageOkEvent(data=storageobj.storage)
        wx.PostEvent(self, event)
        if self.result:
            self.result(storageobj.storage)

    def onSearchStorageCancelButton( self, event ):
        self._filters.remove_group('search')
    
    def onSearchStorageSearchButton( self, event ):
        self._filters.replace(api.data.storage.FilterTextSearch(self.search_storage.Value), 'search')

    def onSearchStorageTextEnter( self, event ):
        self._filters.replace(api.data.storage.FilterTextSearch(self.search_storage.Value), 'search')

    def onButtonRefreshStoragesClick( self, event ):
        self.tree_storages_manager.Load()
        self.tree_parameters_manager.Load()
