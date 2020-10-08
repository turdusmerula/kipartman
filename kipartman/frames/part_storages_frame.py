from dialogs.panel_part_storages import PanelPartStorages
from frames.edit_part_storage_frame import EditPartStorageFrame
import helper.tree
import wx
from helper.exception import print_stack

class PartStorage(helper.tree.TreeContainerItem):
    def __init__(self, part, storage):
        super(PartStorage, self).__init__()
        self.part = part
        self.storage = storage

    def GetValue(self, col):
        if col==0:
            return self.part.id
        elif col==1:
            return self.part.name
        elif col==2:
            return self.storage.storage.name
        elif col==3: 
            return self.storage.quantity
        elif col==4:
            return self.storage.storage.description
        elif col==5: 
            return self.storage.storage.comment

        return ""

class TreeManagerPartStorage(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartStorage, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddIntegerColumn("part id")
        self.AddTextColumn("part")
        self.AddTextColumn("storage name")
        self.AddIntegerColumn("quantity")
        self.AddTextColumn("description")
        self.AddTextColumn("comment")
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for storage in self.part.storages.all():
                storageobj = self.FindStorage(storage)
                if storageobj is None:
                    storageobj = PartStorage(storage.part, storage)
                    self.Append(None, storageobj)
                else:
                    storageobj.part = self.part
                    storageobj.part_storage = storage
                    self.Update(storageobj)

#             # add not yet persisted data
#             for storage in self.part.storages.pendings():
#                 storageobj = self.FindStorage(storage)
#                 if storageobj is None:
#                     storageobj = PartStorage(storage.part, storage)
#                     self.Append(None, storageobj)
#                 else:
#                     storageobj.part = self.part
#                     storageobj.part_storage = storage
#                     self.Update(storageobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindStorage(self, storage):
        for data in self.data:
            if isinstance(data, PartStorage) and data.storage.id==storage.id:
                return data
        return None
            
class PartStoragesFrame(PanelPartStorages):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartStoragesFrame, self).__init__(parent)

        # create storages list
        self.tree_storages_manager = TreeManagerPartStorage(self.tree_storages, context_menu=self.menu_storage)
        self.tree_storages_manager.OnItemBeforeContextMenu = self.onTreeStoragesBeforeContextMenu

        self.tree_storages_manager.Clear()
        self.SetPart(None)

        self._enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.tree_storages_manager.SetPart(part)
        self._enable(False)
        
    def EditPart(self, part):
        self.part = part
        self.tree_storages_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled

    def Save(self, part):
        pass


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
        if isinstance(obj, PartStorage)==False:
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
        storageobj = PartStorage(self.part, storage)
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

