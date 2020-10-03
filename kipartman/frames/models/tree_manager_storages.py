import helper.tree
import api.data.storage
import os


class StorageCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(StorageCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        if col==0:
            return self.category.id
        elif col==1:
            return self.category.path

        return ""

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
        return True

    def IsEnabled(self, col):
        return False

class Storage(helper.tree.TreeContainerItem):
    def __init__(self, storage):
        self.storage = storage
        
        super(Storage, self).__init__()
        
    def GetValue(self, col):
        if col==0:
            return self.storage.id
        elif col==1:
            return self.storage.name
        elif col==2:
            return self.storage.description
        elif col==3:
            return self.storage.comment

        return ""

            
class TreeManagerStorages(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, filters, **kwargs):
        model = TreeModelStorage()
        super(TreeManagerStorages, self).__init__(tree_view, model, *args, **kwargs)

        self.filters = filters
        
        self.flat = False

        self.AddIntegerColumn("id")
        self.AddTextColumn("name")
        self.AddTextColumn("description")
        self.AddIntegerColumn("comment")

    def Load(self):
        
        self.SaveState()
        
        if self.flat:
            self.LoadFlat()
        else:
            self.LoadTree()
        
        self.PurgeState()


    def LoadFlat(self):
        for storage in api.data.storage.find(filters=self.filters.get_filters()):
            storageobj = self.FindStorage(storage.id)
            if storageobj is None:
                storageobj = Storage(storage)
                self.Append(None, storageobj)
            else:
                storageobj.storage = storage
                self.Update(storageobj)
            
    def LoadTree(self):
        for storage in api.data.storage.find(filters=self.filters.get_filters()):
            storageobj = self.FindStorage(storage.id)
            
            if storage.category is not None:
                categoryobj = self.FindCategory(storage.category.id)
                 
                if categoryobj is None:
                    categoryobj = StorageCategory(storage.category)
                    self.Append(None, categoryobj)
                else:
                    categoryobj.category = storage.category
                    self.Update(categoryobj)
            else:
                categoryobj = None
                
            if storageobj is None:
                storageobj = Storage(storage)
                self.Append(categoryobj, storageobj)
            else:
                storageobj.storage = storage
                self.Update(storageobj)
    
    def FindStorage(self, id):
        for data in self.data:
            if isinstance(data, Storage) and ( isinstance(data.parent, StorageCategory) or data.parent is None ) and data.storage.id==id:
                return data
        return None
    
    def FindCategory(self, id):
        for data in self.data:
            if isinstance(data, StorageCategory) and data.category.id==id:
                return data
        return None

    def FindCategories(self,):
        res = []
        for data in self.data:
            if isinstance(data, StorageCategory):
                res.append(data)
        return res

class TreeModelStorage(helper.tree.TreeModel):
    def __init__(self):
        super(TreeModelStorage, self).__init__()
