from dialogs.panel_select_storage import PanelSelectStorage
import wx
import wx.lib.newevent
import wx.dataview
import rest
#from frames.storages_frame import DataModelCategory, DataModelCategoryPath, DataModelStorage, TreeManagerStorages
#from part_storages_frame import DataModelOffer
import helper.tree

SelectStorageOkEvent, EVT_SELECT_STORAGE_OK_EVENT = wx.lib.newevent.NewEvent()
SelectStorageCancelEvent, EVT_SELECT_STORAGE_APPLY_EVENT = wx.lib.newevent.NewEvent()

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

class DataModelStorage(helper.tree.TreeItem):
    def __init__(self, storage):
        super(DataModelStorage, self).__init__()
        self.storage = storage
            
    def GetValue(self, col):
        vMap = { 
            0 : self.storage.name,
            1 : self.storage.description,
            2 : self.storage.comment
        }
        return vMap[col]

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.storage.id}
        return None

class SelectStorageFrame(PanelSelectStorage):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectStorageFrame, self).__init__(parent)
    
        # create storages list
        self.tree_storages_manager = helper.tree.TreeManager(self.tree_storages)
        self.tree_storages_manager.AddTextColumn("Name")
        self.tree_storages_manager.AddTextColumn("Description")
        self.tree_storages_manager.AddTextColumn("Comment")

        # init filter
        self.search_filter = None
        self.search_storage.Value = ''
        self.load()

        # set result functions
        self.cancel = None
        self.result = None
        
    def load(self):
        # clear all
        self.tree_storages_manager.ClearItems()
        
        # load storages
        if self.search_filter:
            storages = rest.api.find_storages(search=self.search_filter)
        else:
            storages = rest.api.find_storages()

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

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
                
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
        if isinstance(storageobj, DataModelStorage)==False:
            return
        
        # trigger result event
        event = SelectStorageOkEvent(data=storageobj.storage)
        wx.PostEvent(self, event)
        if self.result:
            self.result(storageobj.storage)

    def onSearchStorageCancelButton( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchStorageSearchButton( self, event ):
        self.search_filter = self.search_storage.Value
        self.load()
    
    def onSearchStorageTextEnter( self, event ):
        self.search_filter = self.search_storage.Value
        self.load()
