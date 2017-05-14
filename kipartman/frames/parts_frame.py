from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from api.queries import PartsQuery, PartCategoriesQuery
from rest_client.exceptions import QueryError
import wx
from api import models

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        # state of each category node: {selected, expanded}
        self.PartCategoriesState = {}
        self.PartCategoriesState[None] = {False, False}
        
    def _loadCategories(self, parent_item=None):
        
        # get parent
        if parent_item is None:
            self.tree_categories.DeleteAllItems()
            self.tree_categories.AddRoot('root')
            parent_item = self.tree_categories.GetRootItem()
            parent = None
        else:
            parent = self.tree_categories.GetItemPyData(parent_item)
            self.tree_categories.DeleteChildren(parent_item)
        
        # path to tree item map
        path_to_item = {}
        path_to_item[None] = self.tree_categories.GetRootItem()
        if not parent is None:
            path_to_item[parent.path] = parent_item

        # retrieve categories
        if parent is None:
            categories = PartCategoriesQuery().get()
        else:
            categories = PartCategoriesQuery(recursive=True).get(parent.id)
            for category in categories:
                print "--", category.name
        # first loop to initialize a category stack
        # the stack allows to load parents before childrens in case of an unordered request
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
                if path_to_item.has_key(category.path):
                    # check if category already loaded
                    category_stack.remove(category)
                elif path_to_item.has_key(parent_path):
                    # check if parent already loaded in tree
                    print "parent_path:", parent_path
                    newitem = self.tree_categories.AppendItem(parent=path_to_item[parent_path], text=category.name)
                    path_to_item[category.path] = newitem
                    # remove treated item from stack
                    category_stack.remove(category)
                    # add category to item element
                    self.tree_categories.SetItemPyData(newitem, category)
        self._sortCategories()
        
    def _loadParts(self):
        parts = PartsQuery().get()
        for part in parts:
            print "Part: ", type(part), part.name

    def _sortCategories(self, root=None):
        to_sort = []
        if root is None:
            to_sort.append(self.tree_categories.GetRootItem())
        else:
            to_sort.append(root)
        
        for item in to_sort:
            if self.tree_categories.ItemHasChildren(item):
                self.tree_categories.SortChildren(item)
            child, cookie = self.tree_categories.GetFirstChild(item)
            if child and self.tree_categories.ItemHasChildren(child):
                to_sort.append(child)
            while child.IsOk():
                if self.tree_categories.ItemHasChildren(child):
                    to_sort.append(child)
                child, cookie = self.tree_categories.GetNextChild(item, cookie)


    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadCategories()
            self._loadParts()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    
    def onCategoriesRefreshClick( self, event ):
        try:
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            

    def onCategoriesAddClick( self, event ):
        category = EditCategoryFrame(self).addCategory()
        if category:
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
                self.tree_categories.SelectItem(newitem)
                self._sortCategories(parentitem)
                # set node state
                self.PartCategoriesState[category.path] = {self.tree_categories.IsSelected(newitem), self.tree_categories.IsExpanded(newitem)}
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onCategoriesEditClick( self, event ):
        sel = self.tree_categories.GetSelection()
        if self.tree_categories.GetItemPyData(sel) is None:
            return
        # TODO: refresh category from database before edit
        category = EditCategoryFrame(self).editCategory(self.tree_categories.GetItemPyData(sel))
        if not category is None:
            try:
                category = PartCategoriesQuery().update(category)
                self.tree_categories.SetItemPyData(sel, category)
                self.tree_categories.SetItemText(sel, category.name)
                self._sortCategories(self.tree_categories.GetItemParent(sel))
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            
    def onCategoriesRemoveClick( self, event ):
        sel = self.tree_categories.GetSelection()
        category = self.tree_categories.GetItemPyData(sel)
        if category is None:
            return
        try:
            parent = self.tree_categories.GetItemParent(sel) 
            PartCategoriesQuery().delete(category)
            self._loadCategories(parent)
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onTreeCategoriesOnChar( self, event ):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            # unselect current item
            self.tree_categories.SelectItem(self.tree_categories.RootItem)
        event.Skip()

    def onTreeCategoriesSelChanging( self, event ):
        item = self.tree_categories.GetSelection()
        if item.IsOk():
            category = self.tree_categories.GetItemPyData(item)
            if not category is None: 
                print category.path

    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = self.tree_categories.GetItemPyData(item)
        if not category is None: 
            print category.path

    def onTreeCategoriesBeginDrag( self, event ):
        event.Skip()
    
    def onTreeCategoriesEndDrag( self, event ):
        event.Skip()
