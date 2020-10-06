from dialogs.panel_storage_parts import PanelStorageParts
from frames.models.tree_manager_storages import TreeManagerStorages
import api.data.part_storage
import api.models
import wx
import wx.lib.newevent
import helper.tree
from helper.exception import print_stack

class PartStorage(helper.tree.TreeItem):
    def __init__(self, part_storage):
        super(PartStorage, self).__init__()
        self.part_storage = part_storage
         
    def GetValue(self, col):
        if col==0:
            return str(self.part_storage.part.id)
        elif col==1:
            return self.part_storage.part.name
        elif col==2:
            return str(self.part_storage.quantity)
        elif col==3:
            return self.part_storage.part.description

        return ""
 
#     def GetDragData(self):
#         if isinstance(self.parent, DataModelStoragePartPath):
#             return {'id': self.storage.id}
#         return None

class TreeManagerPartStorage(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerPartStorage, self).__init__(tree_view, *args, **kwargs)

        self.filters = filters
        
        self.AddIntegerColumn("id")
        self.AddTextColumn("name")
        self.AddIntegerColumn("quantity")
        self.AddTextColumn("description")

    def Load(self):

        self.SaveState()

        for part_storage in api.data.part_storage.find(filters=self.filters.get_filters()):
            part_storageobj = self.FindStoragePart(part_storage.id)
            if part_storageobj is None:
                part_storageobj = PartStorage(part_storage)
                self.Append(None, part_storageobj)
            else:
                part_storageobj.part = part_storage.part
                self.Update(part_storageobj)
        
        self.PurgeState()
    
    def FindStoragePart(self, id):
        for data in self.data:
            if isinstance(data, PartStorage) and data.part_storage.id==id:
                return data
        return None


class StoragePartsFrame(PanelStorageParts): 
    def __init__(self, *args, **kwargs): 
        super(StoragePartsFrame, self).__init__(*args, **kwargs)

        # storages filters
        self._filters = helper.filter.FilterSet(self)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create storage parts list
        self.tree_storage_parts_manager = TreeManagerPartStorage(self.tree_storage_parts, context_menu=self.menu_part_storage, filters=self.Filters)
#         self.tree_categories_manager.DropAccept(DataModelStoragePart, self.onTreeStoragePartsDropStoragePart)
#         self.tree_categories_manager.DropAccept(DataModelStorage, self.onTreeStoragePartsDropStorage)
        self.tree_storage_parts_manager.OnSelectionChanged = self.onTreeStoragePartsSelectionChanged
        self.tree_storage_parts_manager.OnItemBeforeContextMenu = self.onTreeStoragePartsBeforeContextMenu

        self.tree_storage_parts_manager.Clear()
        
    @property
    def Filters(self):
        return self._filters

    def activate(self):
        self.tree_storage_parts_manager.Load()

    def onFilterChanged( self, event ):
        self.tree_storage_parts_manager.Load()
        event.Skip()

    def onTreeStoragePartsSelectionChanged( self, event ):
        item = self.tree_categories.GetSelection()
        if item.IsOk()==False:
            return
        event.Skip()

    def onTreeStoragePartsBeforeContextMenu( self, event ):
        item = self.tree_categories.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_storage_parts_manager.ItemToObject(item)
        
        self.menu_part_storage_add_stock.Enable(False)
        self.menu_part_storage_remove_stock.Enable(False)
        if isinstance(obj, PartStorage):
            self.menu_part_storage_add_stock.Enable(True)
            self.menu_part_storage_remove_stock.Enable(True)

    def onMenuPartStorageAddStock( self, event ):
        event.Skip()

    def onMenuPartStorageRemoveStock( self, event ):
        event.Skip()

