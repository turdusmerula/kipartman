from dialogs.panel_part_storages import PanelPartStorages
from frames.edit_part_storage_frame import EditPartStorageFrame
import helper.tree
import rest
import wx
from helper.exception import print_stack

class DataModelStorage(helper.tree.TreeContainerItem):
    def __init__(self, part, storage):
        super(DataModelStorage, self).__init__()
        self.part = part
        self.storage = storage

    def GetValue(self, col):
        vMap = { 
            0 : str(self.part.id),
            1 : self.part.name,
            2 : self.storage.name,
            3 : str(self.storage.quantity),
            4 : self.storage.description,
            5 : self.storage.comment,
        }
        return vMap[col]


class TreeManagerStorage(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerStorage, self).__init__(tree_view, *args, **kwargs)
        
    def FindStorage(self, part_id, storage_name):
        for data in self.data:
            if data.part.id==part_id and data.storage.name==storage_name:
                return data
        return None
            
    def DeleteStorage(self, part, storage):
        storageobj = self.FindStorage(part.id, storage.name)
        if storageobj is None:
            return
        self.DeleteItem(None, storageobj)

    def UpdateStorage(self, part, storage):
        storageobj = self.FindStorage(part.id, storage.name)
        if storageobj is None:
            return
        self.UpdateItem(storageobj)
    
    def AppendStorage(self, part, storage):
        storageobj = self.FindStorage(part.id, storage.name)
        if storageobj is None:
            storageobj = DataModelStorage(part, storage)
            self.AppendItem(None, storageobj)
        return storageobj
            
class PartStoragesFrame(PanelPartStorages):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartStoragesFrame, self).__init__(parent)

        # create storages list
        self.tree_storages_manager = TreeManagerStorage(self.tree_storages, context_menu=self.menu_storage)
        self.tree_storages_manager.AddIntegerColumn("Part id")
        self.tree_storages_manager.AddTextColumn("Part")
        self.tree_storages_manager.AddTextColumn("Storage name")
        self.tree_storages_manager.AddIntegerColumn("Quantity")
        self.tree_storages_manager.AddTextColumn("Description")
        self.tree_storages_manager.AddTextColumn("Comment")
        self.tree_storages_manager.OnItemBeforeContextMenu = self.onTreeStoragesBeforeContextMenu

        self.enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.showStorages()

    def enable(self, enabled=True):
        self.enabled = enabled
    
    def showStorages(self):
        self.tree_storages_manager.ClearItems()

        to_add = []
        if self.part:
            to_add.append(self.part)
        while len(to_add)>0:
            part = to_add[0]
            to_add.remove(part)

            if part.storages:
                for storage in part.storages:
                    self.tree_storages_manager.AppendStorage(part, storage)
            
            if part.childs:
                for child in part.childs:
                    to_add.append(child)


    def onTreeStoragesBeforeContextMenu( self, event ):
        item = self.tree_storages.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_storages_manager.ItemToObject(item)

        self.menu_storage_add_storage.Enable(self.enabled)
        self.menu_storage_edit_storage.Enable(self.enabled)
        self.menu_storage_remove_storage.Enable(self.enabled)
        self.menu_storage_add_stock.Enable(True)
        self.menu_storage_remove_stock.Enable(True)
        if isinstance(obj, DataModelStorage)==False:
            self.menu_storage_edit_storage.Enable(False)
            self.menu_storage_remove_storage.Enable(False)
            self.menu_storage_add_stock.Enable(False)
            self.menu_storage_remove_stock.Enable(False)


    def onMenuStorageAddStorage( self, event ):
        storage = EditPartStorageFrame(self).AddStorage(self.part)
        if storage is None:
            return
        if self.part.storages is None:
            self.part.storages = []
        self.part.storages.append(storage)
        storageobj = DataModelStorage(self.part, storage)
        self.tree_storages_manager.AppendItem(None, storageobj)

    def onMenuStorageEditStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return 
        object = self.tree_storages_manager.ItemToObject(item)

        storage = EditPartStorageFrame(self).EditStorage(self.part, object.storage)
        if storage is None:
            return
        object.storage = storage
        self.tree_storages_manager.UpdateItem(object)

    def onMenuStorageRemoveStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.FindStorage(self.tree_storages_manager.ItemToObject(item).storage.id)
        self.part.storages.remove(storageobj.storage)
        self.tree_storages_manager.DeleteItem(None, storageobj)

    def onMenuStorageAddStock( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)

        # TODO: rafraichissement et storages pas encore en base
        dlg = wx.TextEntryDialog(self, 'Quantity to add', 'Stock')
        dlg.SetValue("1")
        if dlg.ShowModal() == wx.ID_OK:
            try:
                rest.api.update_stock({'part_id': self.part.id, 'storage': storageobj.storage, 'amount': int(dlg.GetValue()), 'reason': ''})
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error updating stock', wx.OK | wx.ICON_ERROR)
            
        dlg.Destroy()


    def onMenuStorageRemoveStock( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)

        dlg = wx.TextEntryDialog(self, 'Quantity to remove', 'Stock')
        dlg.SetValue("1")
        if dlg.ShowModal() == wx.ID_OK:
            try:
                rest.api.update_stock({'part_id': self.part.id, 'storage': storageobj.storage, 'amount': -int(dlg.GetValue()), 'reason': ''})
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error updating stock', wx.OK | wx.ICON_ERROR)
            
        dlg.Destroy()

