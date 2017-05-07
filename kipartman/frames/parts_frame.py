from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from api.queries import PartsQuery, PartCategoriesQuery

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)

    def _loadCategories(self):
#         cat = PartCategory(name="toto", parent=None, id=1, path="http://localhost:8100/parts/1")
#         cat2 = PartCategory(name="tata", parent=cat, id=2, path="http://localhost:8100/parts/2")
#         cat3 = PartCategory(name="tutu", parent="http://localhost:8100/api/parts/categories/4", id=2, path="http://localhost:8100/parts/2")
# #        cat3 = PartCategory(name="tata", parent="http://localhost:8100/api/parts/categories/4", id=3, path="http://localhost:8100/api/parts/categories/3")
# 
#         print "---"
#         cat.id = 100
#         cat2.id = 200
#         cat3.id = 300
#         print "---"
#         
#         print "cat: ", cat.id, cat.path, cat.name
#         print "cat2: ", cat2.id, cat2.path, cat2.name, cat2.parent.name
#         print "cat3: ", cat3.id, cat3.path, cat3.name, cat3.parent.name
        self.category_items = {}
        self.tree_categories.AddRoot('root')
        self.category_items[None] = self.tree_categories.RootItem
        categories = PartCategoriesQuery().get()
        for category in categories:
            print "Category: ", type(category), category.name
            if category.parent==None:
                self.category_items[category.id] = self.tree_categories.AppendItem(parent=self.category_items[None], text=category.name)
            else:
                self.category_items[category.id] = self.tree_categories.AppendItem(parent=self.category_items[category.parent.id], text=category.name)


    def _loadParts(self):
        parts = PartsQuery().get()
        for part in parts:
            print "Part: ", type(part), part.name


    # Virtual event handlers, overide them in your derived class
    def load(self): 
        self._loadCategories()
        self._loadParts()


    def onCategoriesRefreshClick( self, event ):
        self.tree_categories.DeleteAllItems()
        self._loadCategories()

    def onCategoriesAddClick( self, event ):
        category = EditCategoryFrame(self).addCategory()
        if not category is None:
            item = self.tree_categories.AppendItem(parent=self.tree_categories.GetSelection(), text=category.name)

    
    def onCategoriesRemoveClick( self, event ):
        category = EditCategoryFrame(self).editCategory()
        if not category is None:
            item = self.tree_categories.AppendItem(parent=self.tree_categories.GetSelection(), text=category.name)
