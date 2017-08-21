from dialogs.panel_part_storages import PanelPartStorages
from frames.edit_part_storage_frame import EditPartStorageFrame
import helper.tree
import rest

class DataModelStorage(helper.tree.TreeContainerItem):
    def __init__(self, storage):
        super(DataModelStorage, self).__init__()
        self.storage = storage

    def GetValue(self, col):
        vMap = { 
            0 : self.storage.name,
            1 : str(self.storage.quantity),
            2 : self.storage.description,
            3 : self.storage.comment,
        }
        return vMap[col]

            
class PartStoragesFrame(PanelPartStorages):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartStoragesFrame, self).__init__(parent)

        # create storages list
        self.tree_storages_manager = helper.tree.TreeManager(self.tree_storages)
        self.tree_storages_manager.AddTextColumn("Name")
        self.tree_storages_manager.AddIntegerColumn("Quantity")
        self.tree_storages_manager.AddTextColumn("Description")
        self.tree_storages_manager.AddTextColumn("Comment")

        self.enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.showStorages()

    def enable(self, enabled=True):
        self.button_add_storage.Enabled = enabled
        self.button_edit_storage.Enabled = enabled
        self.button_remove_storage.Enabled = enabled

    def showStorages(self):
        self.tree_storages_manager.ClearItems()

        if self.part and self.part.storages:
            for storage in self.part.storages:
                storageobj = DataModelStorage(storage)
                self.tree_storages_manager.AppendItem(None, storageobj)
                    
        
    def onButtonAddStorageClick( self, event ):
        storage = EditPartStorageFrame(self).AddStorage(self.part)
        if storage is None:
            return
        if self.part.storages is None:
            self.part.storages = []
        self.part.storages.append(storage)
        storageobj = DataModelStorage(storage)
        self.tree_storages_manager.AppendItem(None, storageobj)
             
    def onButtonEditStorageClick( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return 
        object = self.tree_storages_manager.ItemToObject(item)

        storage = EditPartStorageFrame(self).EditStorage(self.part, object.storage)
        if storage is None:
            return
        object.storage = storage
        self.tree_storages_manager.UpdateItem(object)

    def FindStorage(self, storage_id):
        for data in self.tree_storages_manager.data:
            if data.storage.id==storage_id:
                return data
        return None

    def onButtonRemoveStorageClick( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.FindStorage(self.tree_storages_manager.ItemToObject(item).storage.id)
        self.part.storages.remove(storageobj.storage)
        self.tree_storages_manager.DeleteItem(None, storageobj)

