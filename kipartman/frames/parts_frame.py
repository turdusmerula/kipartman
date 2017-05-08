from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from api.queries import PartsQuery, PartCategoriesQuery
from rest_client.exceptions import QueryError
import wx


class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        
    def _loadCategories(self):
        path_to_item = {}
        self.tree_categories.AddRoot('root')
        path_to_item[None] = self.tree_categories.RootItem
        # retrieve all categories
        categories = PartCategoriesQuery().get()
        # first loop to initialize a category stack
        # the stack allows to load parents before childrens
        category_stack = []
        for category in categories:
            category_stack.append(category)
        # create items
        while len(category_stack)>0:
            for category in category_stack:
                if category.parent is None:
                    parent_path = None
                else:
                    parent_path = category.parent.path
                # check if parent already loaded in tree
                if path_to_item.has_key(parent_path):
                    newitem = self.tree_categories.AppendItem(parent=path_to_item[parent_path], text=category.name)
                    path_to_item[category.path] = newitem
                    # remove treated item from stack
                    category_stack.remove(category)
                    # add category to item element
                    self.tree_categories.SetItemPyData(newitem, category)
            
    def _loadParts(self):
        parts = PartsQuery().get()
        for part in parts:
            print "Part: ", type(part), part.name

            
    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadCategories()
            self._loadParts()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onCategoriesRefreshClick( self, event ):
        self.tree_categories.DeleteAllItems()
        try:
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            

    def onCategoriesAddClick( self, event ):
        category = EditCategoryFrame(self).addCategory()
        if not category is None:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                category.parent = self.tree_categories.GetItemPyData(parentitem)
                # create category on server
                category = PartCategoriesQuery().create(category)
                # create category on treeview
                newitem = self.tree_categories.AppendItem(parent=parentitem, text=category.name) 
                # add category to item element
                self.tree_categories.SetItemPyData(newitem, category)
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)


    def onCategoriesRemoveClick( self, event ):
        category = EditCategoryFrame(self).editCategory()
        if not category is None:
            item = self.tree_categories.AppendItem(parent=self.tree_categories.GetSelection(), text=category.name)

    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = self.tree_categories.GetItemPyData(item)
        print category.path
