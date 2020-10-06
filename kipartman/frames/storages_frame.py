import dialogs.panel_storages
import frames.storage_categories_frame
import frames.storage_list_frame
import helper.filter
import api.data.storage
import wx
from helper.exception import print_stack


class StoragesFrame(dialogs.panel_storages.PanelStorages): 
    def __init__(self, parent): 
        super(StoragesFrame, self).__init__(parent)
        

        # add categories panel
        self.panel_categories = frames.storage_categories_frame.StorageCategoriesFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_categories.Bind( frames.storage_categories_frame.EVT_SELECT_CATEGORY, self.onStorageCategoriesSelectionChanged )
         
        # add storage list panel
        self.panel_storage_list = frames.storage_list_frame.StorageListFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_storage_list.Bind( frames.storage_list_frame.EVT_ENTER_EDIT_MODE, self.onStoragesEnterEditMode )
        self.panel_storage_list.Bind( frames.storage_list_frame.EVT_EXIT_EDIT_MODE, self.onStoragesExitEditMode )
        self.panel_storage_list.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onStoragesFilterChanged )
# 
        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_categories, self.panel_storage_list)
        self.panel_left.Hide()
        self.panel_right.Hide()

    def activate(self):
        self.panel_categories.activate()
        self.panel_storage_list.activate()

    
    def GetMenus(self):
        return None
    
    def onStorageCategoriesSelectionChanged( self, event ):
        self.panel_storage_list.Filters.replace(api.data.storage.FilterCategory(event.category), 'category')
        event.Skip()

    def onStoragesFilterChanged( self, event ):
        if len(self.panel_storage_list.Filters.get_filters_group('category'))==0:
            self.panel_categories.UnselectAll()
        event.Skip()

    def onStoragesEnterEditMode( self, event ):
        self.panel_categories.Enabled = False
        event.Skip()

    def onStoragesExitEditMode( self, event ):
        self.panel_categories.Enabled = True
        event.Skip()
