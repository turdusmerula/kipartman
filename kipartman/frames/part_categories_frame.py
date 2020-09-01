from dialogs.panel_part_categories import PanelPartCategories
from api.data import part_category
from api.models import PartCategory
import wx
import wx.lib.newevent
import helper.tree

class DataModelCategory(helper.tree.TreeContainerLazyItem):
    def __init__(self, category):
        super(DataModelCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        if col==0:
            return self.category.name 
        elif col==1:
            return self.category.description
        return ""

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def Load(self, manager):
        childs = part_category.find_childs(self.category)
        for child in childs:
            manager.AppendPartCategory(parent=self, category=child)

    def IsContainer(self):
        if self.category.is_leaf_node()==False:
            return True
        return False

    def GetDragData(self):
        return {'id': self.category.id}

class TreeManagerPartCategory(helper.tree.TreeManager):
    def __init__(self, *args, **kwargs):
        super(TreeManagerPartCategory, self).__init__(*args, **kwargs)

    def AppendPartCategory(self, parent, category):
        categoryobj = DataModelCategory(category)
        self.AppendItem(parent, categoryobj)
        return categoryobj

(ReloadEvent, EVT_RELOAD) = wx.lib.newevent.NewEvent()
(SelectEvent, EVT_SELECT) = wx.lib.newevent.NewEvent()

class PartCategoriesFrame(PanelPartCategories): 
    def __init__(self, *args, **kwargs): 
        super(PartCategoriesFrame, self).__init__(*args, **kwargs)

        # create categories list
        self.tree_categories_manager = TreeManagerPartCategory(self.tree_categories, context_menu=self.menu_category)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
#         self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
#         self.tree_categories_manager.DropAccept(DataModelPart, self.onTreeCategoriesDropPart)
#         self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged
#         self.tree_categories_manager.OnItemBeforeContextMenu = self.onTreeCategoriesBeforeContextMenu

        self.loaded = False
        
    def activate(self):
        if self.loaded==False:
            self.load()
        self.loaded = True

    def load(self):
        childs = part_category.find_childs()
        for child in childs:
            self.tree_categories_manager.AppendPartCategory(parent=None, category=child)

        evt = ReloadEvent()
        wx.QueueEvent(self, evt)
