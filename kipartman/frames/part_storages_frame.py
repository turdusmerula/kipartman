from dialogs.panel_part_storages import PanelPartStorages
from frames.edit_part_storage_frame import EditPartStorageFrame
import helper.tree
import wx
from helper.exception import print_stack
import api.data.part_storage

class PartStorage(helper.tree.TreeContainerItem):
    def __init__(self, part, part_storage):
        super(PartStorage, self).__init__()
        self.part = part
        self.part_storage = part_storage

    def GetValue(self, col):
        if col==0:
            return self.part.id
        elif col==1:
            return self.part.name
        elif col==2:
            return self.part_storage.storage.name
        elif col==3: 
            return self.part_storage.quantity
        elif col==4:
            return self.part_storage.storage.description
        elif col==5: 
            return self.part_storage.storage.comment

        return ""

    def GetAttr(self, col, attr):
        res = False
        if self.part_storage.id is None:
            attr.SetColour(helper.colors.GREEN_NEW_ITEM)
            res = True
        if self.part_storage.removed_pending():
            attr.SetStrikethrough(True)
            res = True
        return res

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
            for part_storage in self.part.storages.all():
                part_storageobj = self.FindPartStorage(part_storage)
                if part_storageobj is None:
                    part_storageobj = PartStorage(part_storage.part, part_storage)
                    self.Append(None, part_storageobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(part_storageobj)

            # add not yet persisted data
            for part_storage in self.part.storages.pendings():
                part_storageobj = self.FindPartStorage(part_storage)
                if part_storageobj is None:
                    part_storageobj = PartStorage(part_storage.part, part_storage)
                    self.Append(None, part_storageobj)
                else:
                    self.Update(part_storageobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Clear()
        self.Load()
        
    def FindPartStorage(self, part_storage):
        for data in self.data:
            if isinstance(data, PartStorage) and data.part_storage.id==part_storage.id:
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
        EditPartStorageFrame(self).AddStorage(self.part)
        self.tree_storages_manager.Load()

    def onMenuStorageEditStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return 
        part_storageobj = self.tree_storages_manager.ItemToObject(item)
        EditPartStorageFrame(self).EditStorage(self.part, part_storageobj.part_storage)
        self.tree_storages_manager.Load()

    def onMenuStorageRemoveStorage( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)
        self.part.storages.remove_pending(storageobj.part_storage)
        self.tree_storages_manager.Load()

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
                if self.enabled:
                    part_storage = storageobj.part_storage
                else:
                    part_storage = api.data.part_storage.find([api.data.part_storage.FilterPartStorage(storageobj.part_storage.id)])[0]
                
                part_storage.quantity += int(dlg.GetValue())
                
                if self.enabled:
                    self.part.storages.add_pending(part_storage)
                    self.tree_storages_manager.Load()
                else:
                    part_storage.save()
                    self.tree_storages_manager.SetPart(self.part)
                    
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
                if self.enabled:
                    part_storage = storageobj.part_storage
                else:
                    part_storage = api.data.part_storage.find([api.data.part_storage.FilterPartStorage(storageobj.part_storage.id)])[0]
                
                part_storage.quantity -= int(dlg.GetValue())
                
                if self.enabled:
                    self.part.storages.add_pending(part_storage)
                    self.tree_storages_manager.Load()
                else:
                    part_storage.save()
                    self.tree_storages_manager.SetPart(self.part)
                
                self.tree_storages_manager.Load()
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error updating stock', wx.OK | wx.ICON_ERROR)
            
        dlg.Destroy()

