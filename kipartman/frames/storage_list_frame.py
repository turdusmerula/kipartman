from dialogs.panel_storage_list import PanelStorageList
import frames.storage_parts_frame
from frames.select_storage_frame import SelectStorageFrame, EVT_SELECT_STORAGE_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from frames.models.tree_manager_storages import StorageCategory, Storage, TreeManagerStorages
from frames.edit_storage_frame import EditStorageFrame
import api.data.storage
import api.data.part_storage
import helper.filter
from helper.log import log
import wx
from helper.exception import print_stack


(EnterEditModeEvent, EVT_ENTER_EDIT_MODE) = wx.lib.newevent.NewEvent()
(ExitEditModeEvent, EVT_EXIT_EDIT_MODE) = wx.lib.newevent.NewEvent()

class StorageListFrame(PanelStorageList): 
    def __init__(self, *args, **kwargs): 
        super(StorageListFrame, self).__init__(*args, **kwargs)

        # storages filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        
        # create storage list
        self.tree_storages_manager = TreeManagerStorages(self.tree_storages, context_menu=self.menu_storage, filters=self.Filters)
        self.tree_storages_manager.OnSelectionChanged = self.onTreeStoragesSelectionChanged
        self.tree_storages_manager.OnItemBeforeContextMenu = self.onTreeStoragesBeforeContextMenu

        # create edit storage panel
        self.panel_storage_parts = frames.storage_parts_frame.StoragePartsFrame(self.splitter_horz)

        # organize panels
        self.splitter_horz.Unsplit()
        self.splitter_horz.SplitHorizontally( self.panel_storage_locations, self.panel_storage_parts)
        self.panel_down.Hide()

        # initial state
        self.toolbar_storage.ToggleTool(self.toggle_storage_path.GetId(), True)
        self.Flat = False
        self.EditMode = False
        
    @property
    def Filters(self):
        return self._filters

    @property
    def Flat(self):
        return self.tree_storages_manager.flat
    
    @Flat.setter
    def Flat(self, value):
        self.tree_storages_manager.flat = value
        self.tree_storages_manager.Clear()
        self.tree_storages_manager.Load()
        self._expand_categories()
    
    @property
    def EditMode(self):
        return self._edit_mode
    
    @EditMode.setter
    def EditMode(self, value):
        self._edit_mode = value
        if self._edit_mode:
            wx.PostEvent(self, EnterEditModeEvent())        
        else:
            wx.PostEvent(self, ExitEditModeEvent())        
            
    def activate(self):
        self.tree_storages_manager.Load()

    def _expand_categories(self):
        if self.Flat==False:
            for category in self.tree_storages_manager.FindCategories():
                self.tree_storages_manager.Expand(category)
    
    def _enable(self, value):
        pass
        

    def SetStorage(self, storage):
        self.panel_storage_parts.Filters.replace(api.data.part_storage.FilterStorage(storage), "storage")
                

    def onToggleCategoryPathClicked( self, event ):
        self.Flat = not self.toolbar_storage.GetToolState(self.toggle_storage_path.GetId())
        event.Skip()

    def onButtonRefreshStoragesClick( self, event ):
        self.tree_storages_manager.Load()
        event.Skip()
        
    def onFilterChanged( self, event ):
        self.tree_storages_manager.Load()
        self._expand_categories()
        event.Skip()

    def onTreeStoragesSelectionChanged( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage):
            self.SetStorage(obj.storage)
        event.Skip()

    def onTreeStoragesBeforeContextMenu( self, event ):
        item = self.tree_storages.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_storages_manager.ItemToObject(item)

        self.menu_storage_add_storage.Enable(True)
        self.menu_storage_edit_storage.Enable(True)
        self.menu_storage_remove_storage.Enable(True)
        if isinstance(obj, Storage)==False:
            self.menu_storage_edit_storage.Enable(False)
            self.menu_storage_remove_storage.Enable(False)
        event.Skip()

    def onMenuStorageAddStorage( self, event ):
        item = self.tree_storages.GetSelection()
        category = None
        if item.IsOk():
            obj = self.tree_storages_manager.ItemToObject(item)
            if isinstance(obj, StorageCategory):
                category = obj.category
            elif isinstance(obj, Storage):
                category = obj.storage.category
        else:
            # add category from filter
            category = None
            if len(self.Filters.get_filters_group('category'))==1:
                category = self.Filters.get_filters_group('category')[0].category

        storage = EditStorageFrame(self).AddStorage(category)
        if storage:
            # add category to item element
            self.tree_storages_manager.Load()
            self.tree_storages_manager.Select(storage)
        event.Skip()

    def onMenuStorageEditStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage)==False:
            return
        storage = EditStorageFrame(self).EditStorage(obj.storage)
        if storage:
            # add category to item element
            self.tree_storages_manager.Load()
            self.tree_storages_manager.Select(storage)
        event.Skip()

    def onMenuStorageRemoveStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage)==False:
            return
        storage = obj.storage
        associated_parts = api.data.part.find([api.data.part.FilterStorage(storage)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                api.data.storage.delete(storage)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error removing %s:'%path, wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return

            self.SetStorage(None)
            self.tree_storages_manager.Load()
        event.Skip()

    def onMenuStorageDuplicateStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage)==False:
            return

        storage = api.data.storage.duplicate(obj.storage)
        self.EditStorage(storage)
        event.Skip()
        
    def onEditStorageApply( self, event ):
        self.tree_storages_manager.Load()

        storage = event.storage
        storageobj = self.tree_storages_manager.FindStorage(storage.id)
        self.tree_storages_manager.Select(storageobj)
        
        self.SetStorage(storage)
        self.EditMode = False
        event.Skip()
      
    def onEditStorageCancel( self, event ):
        self.tree_storages_manager.Load()
        
        # reload the storage after changing it
        item = self.tree_storages.GetSelection()
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, Storage):
            self.SetStorage(obj.storage)
        else:
            self.SetStorage(None)

        self.EditMode = False        
        event.Skip()

