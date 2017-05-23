from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_part_frame import EditPartFrame
from api.queries import PartsQuery, PartCategoriesQuery
from rest_client.exceptions import QueryError
import wx
import wx.dataview
import json
from api import models
import copy

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
        data = self.tree.GetItemData(item)
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
    def __init__(self, frame):
        self.frame = frame
        super(PartCategoryDropTarget, self).__init__()
    
    #TODO: set drag cursor depending on accept/reject drop
    def OnDropText(self, x, y, text):
        data = json.loads(text)
        print "PartCategoryDropTarget.OnDropText", data, x, y
        item, _ = self.frame.part_categories_tree.HitTest((x, y))
        if item.IsOk():
            target_category = self.frame.part_categories_tree.GetItemData(item)
        else:
            target_category = None
        if data['model']=='PartCategory':
            source_category = PartCategoriesQuery().get(data['id'])[0]
            if source_category:
                source_category.parent = target_category
            PartCategoriesQuery().update(source_category)
        elif data['model']=='Part':
            source_part = PartsQuery().get(data['id'])[0]
            if source_part:
                source_part.category = target_category
                PartsQuery().update(source_part)
        self.frame.load()
        return wx.DragMove


class PartDataObject(wx.TextDataObject):
    def __init__(self, category): 
        super(PartDataObject, self).__init__()
        self.category = category
        self.SetText(json.dumps({'model': 'Part', 'url': category.path, 'id': category.id}))

class PartDropTarget(wx.TextDropTarget):
    def __init__(self, frame):
        self.frame = frame
        super(PartDropTarget, self).__init__()
    
    #TODO: set drag cursor depending on accept/reject drop
    def OnDropText(self, x, y, text):
        data = json.loads(text)
        print "PartDropTarget.OnDropText", data, x, y
        item, _ = self.frame.tree_parts.HitTest((x, y))
        if item.IsOk():
            # do a copy to avoid nasty things
            target_part = copy.deepcopy(self.frame.parts_model.ItemToObject(item))
        else:
            target_part = None
        if data['model']=='Part':
            source_part = PartsQuery().get(data['id'])[0]
            if source_part and target_part:
                target_part.parts.append(source_part.id)
                PartsQuery().update(target_part)
        self.frame._loadParts()
        return wx.DragMove



class PartDataModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(PartDataModel, self).__init__()
        self.data = PartsQuery().get()
        #self.UseWeakRefs(True)
    
    def Filter(self, part_filter=None):
        if part_filter:
            self.data = PartsQuery(**part_filter).get()
        
    def GetColumnCount(self):
        return 4

    def GetColumnType(self, col):
        mapper = { 
            0 : 'long',
            1 : 'string',
            2 : 'string',
            3 : 'string'
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for part in self.data:
                # mark root parts to avoid recursion
                part.parent = None
                children.append(self.ObjectToItem(part))
            return len(self.data)
        
        # load childrens
        parent_part = self.ItemToObject(parent)
        for id in parent_part.parts:
            subpart = PartsQuery().get(id)[0]
            subpart.parent = parent_part
            print "subpart", subpart.id
            children.append(self.ObjectToItem(subpart))
        return len(parent_part.parts)
    
    def IsContainer(self, item):
        if not item:
            return True
        part = self.ItemToObject(item)
        return len(part.parts)>0

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        if not item:
            return wx.dataview.NullDataViewItem

        part = self.ItemToObject(item)
        if not part.parent:
            return wx.dataview.NullDataViewItem
        else:
            return self.ObjectToItem(part.parent)
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : str(obj.id),
            1 : obj.name,
            2 : obj.description,
            3 : obj.comment
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        if col == 0:
            attr.Bold = True
            return True
        return False

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        # create categories data
        self.part_categories_state = TreeState(self.tree_categories)
        self.part_categories_tree = Tree(self.tree_categories)
        # create parts data
        self.part_state = TreeState(self.tree_parts)
        self.part_tree = Tree(self.tree_parts)
        # create category drop targets
        pc_dt = PartCategoryDropTarget(self)
        self.tree_categories.SetDropTarget(pc_dt)        
        # parts filters
        self.part_filter={}
        # create parts list
        self.parts_model = PartDataModel()
        self.tree_parts.AssociateModel(self.parts_model)
        # add default columns
        self.tree_parts.AppendTextColumn("id", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parts.AppendTextColumn("name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parts.AppendTextColumn("description", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parts.AppendTextColumn("comment", 3, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_parts.Columns:
            c.Sortable = True
            c.Reorderable = True

        # create parts drag and drop targets
        self.tree_parts.EnableDragSource(wx.DataFormat(wx.TextDataObject().GetFormat()))
        p_dt = PartDropTarget(self)
        self.tree_parts.EnableDropTarget(wx.DataFormat(wx.DF_TEXT))
        self.tree_parts.SetDropTarget(p_dt)

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
                    self.tree_categories.SetItemData(newitem, category)
        # set items status
        for path in path_to_item:
            if path and self.part_categories_state.expanded(path):
                self.tree_categories.Expand(path_to_item[path])
            if self.part_categories_state.selected(path):
                self.tree_categories.SelectItem(path_to_item[path])

        self.part_categories_tree.sort()
        
    def _loadParts(self):
        # apply new filter and reload
        self.parts_model.Cleared()
        self.parts_model = PartDataModel()
        self.parts_model.Filter(self.part_filter)
        self.tree_parts.AssociateModel(self.parts_model)

    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        
    def onButtonRefreshCategoriesClick( self, event ):
        try:
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory()
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                category.parent = self.tree_categories.GetItemData(parentitem)
                # create category on server
                category = PartCategoriesQuery().create(category)
                # create category on treeview
                newitem = self.tree_categories.AppendItem(parent=parentitem, text=category.name) 
                # add category to item element
                self.tree_categories.SetItemData(newitem, category)
                self.tree_categories.SelectItem(newitem)
                self.part_categories_tree.sort(parentitem)
                # set node state
                self.part_categories_state.update(newitem)
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonEditCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        if self.tree_categories.GetItemData(sel) is None:
            return
        # TODO: refresh category from database before edit
        category = EditCategoryFrame(self).editCategory(self.tree_categories.GetItemData(sel))
        if not category is None:
            try:
                category = PartCategoriesQuery().update(category)
                self.tree_categories.SetItemData(sel, category)
                self.tree_categories.SetItemText(sel, category.name)
                self.part_categories_tree.sort(self.tree_categories.GetItemParent(sel))
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            
    def onButtonRemoveCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        category = self.tree_categories.GetItemData(sel)
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
        category = self.tree_categories.GetItemData(item)
        self.part_categories_state.update(item, selected=True)
        self.part_categories_state.debug()
        # set category filter
        if category:
            self.part_filter['category'] = category.id
        else:
            self.part_filter.pop('category')
        # apply new filter and reload
        self._loadParts()


    def onTreeCategoriesCollapsed( self, event ):
        self.part_categories_state.update(event.GetItem(), expanded=False)
        event.Skip()
    
    def onTreeCategoriesExpanded( self, event ):
        self.part_categories_state.update(event.GetItem(), expanded=True)
        event.Skip()
        
    def onTreeCategoriesBeginDrag( self, event ):
        category = self.tree_categories.GetItemData(event.GetItem())
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
        event.Allow()


    def onButtonAddPartClick( self, event ):
        part = EditPartFrame(self).addPart()
        if part:
            try:
                # create part on server
                category_item = self.tree_categories.GetSelection()
                part.category = self.tree_categories.GetItemData(category_item)
                part = PartsQuery().create(part)
                self._loadParts()
            except QueryError as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonEditPartClick( self, event ):
        event.Skip()

    def onButtonRemovePartClick( self, event ):
        event.Skip()

    def onSearchPartsTextEnter( self, event ):
        event.Skip()

    def onButtonRefreshPartsClick( self, event ):
        event.Skip()

    def onTreePartsItemBeginDrag( self, event ):
        print "+ onTreePartsBeginDrag"
        part = self.parts_model.ItemToObject(event.GetItem())
        data =  PartDataObject(part)
        event.SetDataObject(data)

        
    def onTreePartsItemDrop( self, event ):
        print "+ onTreePartsItemDrop"
        event.Allow()
