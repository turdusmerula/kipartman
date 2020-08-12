from dialogs.panel_part_categories import PanelPartCategories
import helper.tree
from api.models import PartCategory

class DataModelCategory(helper.tree.TreeContainerItem):
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

    def GetDragData(self):
        return {'id': self.category.id}

class CategoriesFrame(PanelCategories): 
    def __init__(self, parent, category_class): 
        super(CategoriesFrame, self).__init__(parent)

        self.category_class = category_class
        
        # create categories list
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories, context_menu=self.menu_category)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
#         self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
#         self.tree_categories_manager.DropAccept(DataModelPart, self.onTreeCategoriesDropPart)
#         self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged
#         self.tree_categories_manager.OnItemBeforeContextMenu = self.onTreeCategoriesBeforeContextMenu

    def load(self):
        pass