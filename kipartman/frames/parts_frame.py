from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from api.queries import PartsQuery, PartCategoriesQuery
from rest_client.exceptions import QueryError
import wx
import json
from api import models

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class ItemState:
    def __init__(self, selected=False, expanded=True):
        self.selected = selected
        self.expanded = expanded

class TreeState:
    def __init__(self, tree):
        self.tree = tree
        self.state = {}
    
    def update(self, item, selected=None, expanded=None):
        data = self.tree.GetItemPyData(item)
        if data:
            path = data.path
        else:
            path = None
        self.state[path] = ItemState(selected=self.tree.IsSelected(item), expanded=self.tree.IsExpanded(item))
        if not selected is None:
            self.state[path].selected = selected
        if not expanded is None:
            self.state[path].expanded = expanded
        print "state:", self.state[path].selected, self.state[path].expanded 

    def remove(self, path):
        self.state.pop(path)        

    def selected(self, path):
        if self.state.has_key(path):
            return self.state[path].selected
        else:
            return False
    
    def expanded(self, path):
        if self.state.has_key(path):
            return self.state[path].expanded
        else:
            return False
    
    def debug(self):
        print "State:"
        for state in self.state:
            print "    ", state, "selected:", self.state[state].selected, "expanded: ", self.state[state].expanded
    
class Tree:
    def __init__(self, tree):
        self.tree = tree 
        
    def sort(self, root=None):
        to_sort = []
        if root is None:
            to_sort.append(self.tree.GetRootItem())
        else:
            to_sort.append(root)
        
        for item in to_sort:
            if self.tree.ItemHasChildren(item):
                self.tree.SortChildren(item)
            child, cookie = self.tree.GetFirstChild(item)
            if child and self.tree.ItemHasChildren(child):
                to_sort.append(child)
            while child.IsOk():
                if self.tree.ItemHasChildren(child):
                    to_sort.append(child)
                child, cookie = self.tree.GetNextChild(item, cookie)


class PartCategoryDataObject(wx.TextDataObject):
    def __init__(self, category): 
        super(PartCategoryDataObject, self).__init__()
        self.category = category
        self.SetText(json.dumps({'model': 'PartCategory', 'url': category.path, 'id': category.id}))
        
    
class PartCategoryDropTarget(wx.TextDropTarget):
    def __init__(self, tree, frame):
        self.obj = tree
        self.frame = frame
        super(PartCategoryDropTarget, self).__init__()
    
    #TODO: set drag cursor depending on accept/reject drop
    def OnDropText(self, x, y, text):
        data = json.loads(text)
        print "OnDropText", data, x, y
        item, _ = self.obj.HitTest((x, y))
        if item.IsOk():
            target_category = self.obj.GetItemPyData(item)
        else:
            target_category = None
        source_category = PartCategoriesQuery().get(data['id'])[0]
        if source_category:
            source_category.parent = target_category
        PartCategoriesQuery().update(source_category)
        
        self.frame._loadCategories()
        return text
    
class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        self.part_categories_state = TreeState(self.tree_categories)
        self.part_categories_tree = Tree(self.tree_categories)
        # create drop targets
        pc_dt = PartCategoryDropTarget(self.tree_categories, self)
        self.tree_categories.SetDropTarget(pc_dt)
        
    def _loadCategories(self):
        self.tree_categories.DeleteAllItems()
        
        # path to tree item map
        path_to_item = {}
        
        # root node
        self.tree_categories.AddRoot('root')
        self.part_categories_state.update(self.tree_categories.GetRootItem())
        path_to_item[None] = self.tree_categories.GetRootItem()

        # retrieve categories
        categories = PartCategoriesQuery().get()

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
                    newitem = self.tree_categories.AppendItem(parent=path_to_item[parent_path], text=category.name)
                    path_to_item[category.path] = newitem
                    # remove treated item from stack
                    category_stack.remove(category)
                    # add category to item element
                    self.tree_categories.SetItemPyData(newitem, category)
        # set items status
        for path in path_to_item:
            if path and self.part_categories_state.expanded(path):
                self.tree_categories.Expand(path_to_item[path])
            if self.part_categories_state.selected(path):
                self.tree_categories.SelectItem(path_to_item[path])

        self.part_categories_tree.sort()
        
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
                self.part_categories_tree.sort(parentitem)
                # set node state
                self.part_categories_state.update(newitem)
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
                self.part_categories_tree.sort(self.tree_categories.GetItemParent(sel))
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            
    def onCategoriesRemoveClick( self, event ):
        sel = self.tree_categories.GetSelection()
        category = self.tree_categories.GetItemPyData(sel)
        if category is None:
            return
        try:
            PartCategoriesQuery().delete(category)
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        # remove category status
        self.part_categories_state.remove(category.path)        

    def onTreeCategoriesOnChar( self, event ):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            sel = self.tree_categories.GetSelection()
            # unselect current item
            self.tree_categories.SelectItem(self.tree_categories.RootItem)
            # update state
            self.part_categories_state.update(sel)
            self.part_categories_state.update(self.tree_categories.RootItem)            
        event.Skip()

    def onTreeCategoriesSelChanging( self, event ):
        item = self.tree_categories.GetSelection()
        self.part_categories_state.update(item, selected=False)
        
    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        self.part_categories_state.update(item, selected=True)
        self.part_categories_state.debug()

    def onTreeCategoriesCollapsed( self, event ):
        self.part_categories_state.update(event.GetItem(), expanded=False)
        event.Skip()
    
    def onTreeCategoriesExpanded( self, event ):
        self.part_categories_state.update(event.GetItem(), expanded=True)
        event.Skip()
        
    def onTreeCategoriesBeginDrag( self, event ):
        print "+ onTreeCategoriesBeginDrag"
        category = self.tree_categories.GetItemPyData(event.GetItem())
        data = PartCategoryDataObject(category)
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)
        print type(result)
        if result==wx.DragCopy:
#            CopyPartCategory()
            pass
        elif result==wx.DragMove:
#            MoveMyData()
            pass

    def onTreeCategoriesEndDrag( self, event ):
        print "+ onTreeCategoriesEndDrag"
        event.Allow()
