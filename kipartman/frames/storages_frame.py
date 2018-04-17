from dialogs.panel_storages import PanelStorages
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_storage_frame import EditStorageFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
import helper.tree
from helper.filter import Filter
import rest
import wx
from swagger_client.models.part_storage import PartStorage

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class DataModelCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        vMap = { 
            0 : self.category.name,
            1 : self.category.description,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def GetDragData(self):
        return {'id': self.category.id}


class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==1:
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False

class TreeManagerStorages(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerStorages, self).__init__(tree_view)

    def FindStorage(self, storage_id):
        for data in self.data:
            if isinstance(data, DataModelStorage) and data.storage.id==storage_id:
                return data
        return None
    
    def FindCategoryPath(self, category):
        if category:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category.id==category.id:
                    return data
        else:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category is None:
                    return data
        return None
    
    def DeleteStorage(self, storage):
        storageobj = self.FindStorage(storage.id)
        if storageobj is None:
            return
        categoryobj = storageobj.parent
        self.DeleteItem(storageobj.parent, storageobj)
        if categoryobj and len(categoryobj.childs)==0:
            self.DeleteItem(categoryobj.parent, categoryobj)

    def UpdateStorage(self, storage):
        storageobj = self.FindStorage(storage.id)
        if storageobj is None:
            return
        self.UpdateItem(storageobj)

    def AppendCategoryPath(self, category):
        categoryobj = self.FindCategoryPath(category)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryPath(category)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendStorage(self, storage):
        categoryobj = self.AppendCategoryPath(storage.category)
        storageobj = DataModelStorage(storage)
        self.AppendItem(categoryobj, storageobj)
        self.Expand(categoryobj)
        return storageobj
    

class DataModelStorage(helper.tree.TreeItem):
    def __init__(self, storage):
        super(DataModelStorage, self).__init__()
        self.storage = storage
            
    def GetValue(self, col):
        vMap = { 
            0 : str(self.storage.id),
            1 : self.storage.name,
            2 : self.storage.description,
            3 : self.storage.comment
        }
        return vMap[col]

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.storage.id}
        return None


class DataModelStoragePart(helper.tree.TreeItem):
    def __init__(self, part, quantity):
        super(DataModelStoragePart, self).__init__()
        self.part = part
        self.quantity = quantity
        
    def GetValue(self, col):
        vMap = { 
            0 : str(self.part.id),
            1 : self.part.name,
            2 : str(self.quantity),
            3 : self.part.description,
        }
        return vMap[col]

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.storage.id}
        return None

class StoragesFrame(PanelStorages): 
    def __init__(self, parent):
        super(StoragesFrame, self).__init__(parent)
        
        # create categories data
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
        self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
        self.tree_categories_manager.DropAccept(DataModelStorage, self.onTreeCategoriesDropStorage)
        self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged

        # storages filters
        self.storages_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create storage list
        self.tree_storages_manager = TreeManagerStorages(self.tree_storages)
        self.tree_storages_manager.AddIntegerColumn("id")
        self.tree_storages_manager.AddTextColumn("name")
        self.tree_storages_manager.AddTextColumn("description")
        self.tree_storages_manager.AddIntegerColumn("comment")
        self.tree_storages_manager.OnSelectionChanged = self.onTreeStoragesSelChanged

        # create storage part list
        self.tree_storage_parts_manager = helper.tree.TreeManager(self.tree_storage_parts)
        self.tree_storage_parts_manager.AddIntegerColumn("id")
        self.tree_storage_parts_manager.AddTextColumn("name")
        self.tree_storage_parts_manager.AddIntegerColumn("quantity")
        self.tree_storage_parts_manager.AddTextColumn("description")
        self.tree_storage_parts_manager.OnSelectionChanged = self.onTreeStoragePartsSelChanged

        # initial edit state
        self.show_storage(None)
        self.edit_state = None

        self.load() 
        
    def loadCategories(self):
        # clear all
        self.tree_categories_manager.ClearItems()
        
        # load categories
        categories = rest.api.find_storages_categories()

        # load tree
        to_add = []
        id_category_map = {}
        for category in categories:
            to_add.append(category)
        while len(to_add)>0:
            category = to_add[0]
            id_category_map[category.id] = DataModelCategory(category)
            to_add.pop(0)
            
            # add to symbol
            if category.parent:
                self.tree_categories_manager.AppendItem(id_category_map[category.parent.id], id_category_map[category.id])
            else:
                self.tree_categories_manager.AppendItem(None, id_category_map[category.id])
            
            # load childs
            if category.childs:
                for child in category.childs:
                    to_add.append(child)

    def loadStorages(self):
        # clear all
        self.tree_storages_manager.ClearItems()
        
        # load storages
        storages = rest.api.find_storages(**self.storages_filter.query_filter())

        # load categories
        categories = {}
        for storage in storages:
            if storage.category:
                category_name = storage.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(storage.category)
                self.tree_storages_manager.AppendItem(None, categories[category_name])
            self.tree_storages_manager.AppendItem(categories[category_name], DataModelStorage(storage))
        
        for category in categories:
            self.tree_storages_manager.Expand(categories[category])

    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self.loadCategories()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        try:
            self.loadStorages()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def show_storage(self, storage):
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_storages.Enabled = True

        self.load_storage_parts(storage)
        
    def load_storage_parts(self, storage):
        if storage is None:
            return 
        parts = rest.api.find_parts(storage=storage.id, with_storages=True)
        
        self.tree_storage_parts_manager.ClearItems()
        for part in parts:
            if part.storages:
                for part_storage in part.storages:
                    if part_storage.id==storage.id:
                        storage_partobj = DataModelStoragePart(part, part_storage.quantity)
                        self.tree_storage_parts_manager.AppendItem(None, storage_partobj)
    
    def onButtonRefreshCategoriesClick( self, event ):
        self.loadCategories()

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(rest.model.StorageCategoryNew)
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                parentobj = None
                category.parent = None
                if parentitem:
                    parentobj = self.tree_categories_manager.ItemToObject(parentitem)
                    category.parent = parentobj.category
                    
                # create category on server
                category = rest.api.add_storages_category(category)
                # create category on treeview
                newitem = self.tree_categories_manager.AppendItem(parentobj, DataModelCategory(category)) 
                # add category to item element
                self.tree_categories_manager.SelectItem(newitem)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonEditCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        category = EditCategoryFrame(self).editCategory(categoryobj.category)
        if not category is None:
            try:
                categoryobj.category = rest.api.update_storages_category(categoryobj.category.id, category)
                self.tree_categories_manager.UpdateItem(categoryobj)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        try:
            res = wx.MessageDialog(self, "Remove category '"+categoryobj.category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                rest.api.delete_storages_category(categoryobj.category.id)
                self.tree_categories_manager.DeleteItem(categoryobj.parent, categoryobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.storages_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self.loadStorages()

    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = None
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
        # set category filter
        self.storages_filter.remove('category')
        if category:
            self.storages_filter.add('category', category.category.id, category.category.name)
        # apply new filter and reload
        self.loadStorages()

    def onTreeCategoriesDropCategory(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
        try:
            source_category_id = data['id']
            source_category = rest.api.find_storages_category(source_category_id)
            source_categoryitem = helper.tree.TreeManager.drag_item
            source_categoryobj = self.tree_categories_manager.ItemToObject(source_categoryitem)
    
            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                if source_category_id==dest_category.id:
                    return wx.DragError
                source_category.parent = rest.model.StorageCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_category.parent = None
            
            # update on server
            category = rest.api.update_storages_category(source_category.id, source_category)

            # update tree symbol
            if source_categoryobj:
                self.tree_categories_manager.MoveItem(source_categoryobj.parent, dest_categoryobj, source_categoryobj)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        return wx.DragMove

    def onTreeCategoriesDropStorage(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))

        try:
            source_storage_id = data['id']
            source_storage = rest.api.find_storage(source_storage_id)

            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                source_storage.category = rest.model.StorageCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_storage.category = None
            
            # update on server
            storage = rest.api.update_storage(source_storage.id, source_storage)
            
            # update tree symbol
            self.tree_storages_manager.DeleteStorage(source_storage)
            self.tree_storages_manager.AppendStorage(storage)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        return wx.DragMove

    def onTreeStoragesSelChanged( self, event ):
        item = self.tree_storages.GetSelection()
        storage = None
        if not item.IsOk():
            return
        
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, DataModelStorage):
            storage = obj.storage
        self.show_storage(storage)

    def onEditStorageApply( self, event ):
        storage = event.data
        try:
            if self.edit_state=='edit':
                # update part on server
                storage = rest.api.update_storage(storage.id, storage)
                self.tree_storages_manager.UpdateStorage(storage)
            elif self.edit_state=='add':
                storage = rest.api.add_storage(storage)
                self.tree_storages_manager.AppendStorage(storage)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        self.edit_state = None
        self.show_storage(storage)
     
    def onEditStorageCancel( self, event ):
        storage = None
        item = self.tree_storages.GetSelection()
        if item.IsOk():
            storageobj = self.tree_storages_manager.ItemToObject(item)
            storage = storageobj.storage
        self.edit_state = None
        self.show_storage(storage)

    def onButtonAddStorageClick( self, event ):
        storage = EditStorageFrame(self).addStorage(rest.model.StorageNew)
        if storage:
            try:
                # retrieve parent item from selection
                categoryitem = self.tree_categories.GetSelection()
                categoryobj = None
                storage.category = None
                if categoryitem:
                    categoryobj = self.tree_categories_manager.ItemToObject(categoryitem)
                    storage.category = categoryobj.category
                    
                # create category on server
                storage = rest.api.add_storage(storage)
                # create category on treeview
                newitem = self.tree_storages_manager.AppendItem(None, DataModelStorage(storage)) 
                # add category to item element
                self.tree_storages_manager.SelectItem(newitem)
                self.onTreeStoragesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        
    def onButtonEditStorageClick( self, event ):
        sel = self.tree_storages.GetSelection()
        if sel.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(sel)
        if storageobj is None:
            return
        storage = EditStorageFrame(self).editStorage(storageobj.storage)
        if not storage is None:
            try:
                storageobj.storage = rest.api.update_storage(storageobj.storage.id, storage)
                self.tree_storages_manager.UpdateItem(storageobj)
                self.onTreeStoragesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        # 
    def onButtonRemoveStorageClick( self, event ):
        sel = self.tree_storages.GetSelection()
        if sel.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(sel)
        if storageobj is None:
            return
        try:
            res = wx.MessageDialog(self, "Remove storage '"+storageobj.storage.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                rest.api.delete_storage(storageobj.storage.id)
                self.tree_storages_manager.DeleteItem(storageobj.parent, storageobj)
                self.onTreeStoragesSelChanged(None)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRefreshStoragesClick( self, event ):
        self.loadStorages()

    def onSearchStoragesTextEnter( self, event ):
        # set search filter
        self.storages_filter.remove('search')
        if self.search_storages.Value!='':
            self.storages_filter.add('search', self.search_storages.Value)
        # apply new filter and reload
        self.loadStorages()

    def onButtonAddStoragePartClick( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(obj, DataModelStorage)==False:
            return
        
        dropdown = DropdownDialog(self.button_add_storage_part, SelectPartFrame, "")
        dropdown.panel.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectPartCallback )
        dropdown.Dropdown()
    
    def onButtonRemoveStoragePartClick( self, event ):
        event.Skip()

    def onSearchStoragesButton(self, event):
        return self.onSearchStoragesTextEnter(event)

    def onTreeStoragePartsSelChanged( self, event ):
        pass
    
    def onButtonAddStorageItemClick( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(storageobj, DataModelStorage)==False:
            return
        
        sel = self.tree_storage_parts.GetSelection()
        if sel.IsOk()==False:
            return
        partobj = self.tree_storage_parts_manager.ItemToObject(sel)
        if partobj is None:
            return
        
        if self.spin_num_parts.Value==0:
            return
        
        try:
            res = wx.MessageDialog(self, "Add %d items of %s to storage?"%(self.spin_num_parts.Value, partobj.part.name), "Add?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                part = rest.api.find_part(partobj.part.id, with_storages=True)
                for part_storage in part.storages:
                    if part_storage.id==storageobj.storage.id:
                        part_storage.quantity = part_storage.quantity+self.spin_num_parts.Value
                        break
            
                partobj.part = rest.api.update_part(part.id, part)
                partobj.quantity = part_storage.quantity
                self.tree_storage_parts_manager.UpdateItem(partobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveStorageItemClick( self, event ):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(storageobj, DataModelStorage)==False:
            return
        
        sel = self.tree_storage_parts.GetSelection()
        if sel.IsOk()==False:
            return
        partobj = self.tree_storage_parts_manager.ItemToObject(sel)
        if partobj is None:
            return
        
        if self.spin_num_parts.Value==0:
            return
        
        try:
            res = wx.MessageDialog(self, "Remove %d items of %s to storage?"%(self.spin_num_parts.Value, partobj.part.name), "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                part = rest.api.find_part(partobj.part.id, with_storages=True)
                for part_storage in part.storages:
                    if part_storage.id==storageobj.storage.id:
                        part_storage.quantity = part_storage.quantity-self.spin_num_parts.Value
                        break
            
                partobj.part = rest.api.update_part(part.id, part)
                if part_storage.quantity<0:
                    part_storage.quantity = 0
                partobj.quantity = part_storage.quantity
                self.tree_storage_parts_manager.UpdateItem(partobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onSelectPartCallback(self, part_event):
        item = self.tree_storages.GetSelection()
        if item.IsOk()==False:
            return
        storageobj = self.tree_storages_manager.ItemToObject(item)
        if isinstance(storageobj, DataModelStorage)==False:
            return

        part = part_event.data
        # check if part already exist
        for data in self.tree_storage_parts_manager.data:
            if data.part.id==part.id:
                wx.MessageDialog(self, "%s already added, skipped" % part_event.data.name, "Error adding part", wx.OK | wx.ICON_ERROR).ShowModal()
                return

        # update storages on part
        part = rest.api.find_part(part.id, with_storages=True)
        if part.storages is None:
            part.storages = []
        part_storage = PartStorage()
        part_storage.id = storageobj.storage.id
        part_storage.quantity = self.spin_num_parts.Value
        part.storages.append(part_storage)
        part = rest.api.update_part(part.id, part)

        partobj = DataModelStoragePart(part, part_storage.quantity)
        self.tree_storage_parts_manager.AppendItem(None, partobj)

