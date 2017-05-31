from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from frames.select_footprint_frame import SelectFootprintFrame
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from api.queries import PartsQuery, PartCategoriesQuery
from rest_client.exceptions import QueryError
import wx.dataview
import json
from api import models
import copy
from helper.tree_state import TreeState
from helper.tree import Tree
from helper.filter import Filter
from frames.select_octopart_frame import SelectOctopartFrame

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

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
        item, _ = self.frame.tree_categories.HitTest((x, y))
        if item.IsOk():
            target_category = self.frame.tree_categories.GetItemData(item)
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
        # create category drop targets
        pc_dt = PartCategoryDropTarget(self)
        self.tree_categories.SetDropTarget(pc_dt)
        # parts filters
        self.parts_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)
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

        # initial edit state
        self.show_part(None)
        self.edit_state = None
        self.edit_part_object = None
        
        self.load()
        
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
        self.parts_model.Filter(self.parts_filter.query_filter())
        self.tree_parts.AssociateModel(self.parts_model)

    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadCategories()
            self._loadParts()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)


    def show_part(self, part):
        # disable editing
        self.panel_edit_part.Enabled = False
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_parts.Enabled = True
        if part:
            self.edit_part_name.Value = part.name
            self.edit_part_description.Value = part.description
            self.edit_part_comment.Value = part.comment
            if part.footprint:
                self.button_part_footprint.Label = part.footprint.name
            else:
                self.button_part_footprint.Label = "<none>"
            self.button_part_footprint.Value = part.footprint
        else:
            self.edit_part_name.Value = ''
            self.edit_part_description.Value = ''
            self.edit_part_comment.Value = ''
            self.button_part_footprint.Label = "<none>"
    
    def edit_part(self, part):
        self.show_part(part)
        self.edit_part_object = part
        # enable editing
        self.panel_edit_part.Enabled = True
        # disable evrything else
        self.panel_category.Enabled = False
        self.panel_parts.Enabled = False
        
    def new_part(self):
        self.edit_part(models.Part())


    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.parts_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self._loadParts()
    
    def onButtonRefreshCategoriesClick( self, event ):
        try:
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(models.PartCategory)
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                category.parent = None
                if parentitem:
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
            res = wx.MessageDialog(self, "Remove category '"+category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                PartCategoriesQuery().delete(category)
                self._loadCategories()
            else:
                return
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
        self.parts_filter.remove('category')
        if category:
            self.parts_filter.add('category', category.id, category.name)
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
        self.edit_state = 'add'
        self.new_part()

    def onButtonEditPartClick( self, event ):
        if not self.tree_parts.GetSelection():
            return
        part = self.parts_model.ItemToObject(self.tree_parts.GetSelection())
        self.edit_state = 'edit'
        self.edit_part(part)

    def onButtonRemovePartClick( self, event ):
        item = self.tree_parts.GetSelection()
        if not item:
            return 
        part = self.parts_model.ItemToObject(item)
        if part.parent:
            res = wx.MessageDialog(self, "Remove part '"+part.name+"' from '"+part.parent.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # remove selected part from subparts
                part.parent.parts.remove(part.id)
                PartsQuery().update(part.parent)
            else:
                return 
        else:
            res = wx.MessageDialog(self, "Remove part '"+part.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # remove part
                PartsQuery().delete(part)
            else:
                return
        self._loadParts()
        event.Skip()

    def onSearchPartsTextEnter( self, event ):
        # set search filter
        self.parts_filter.remove('search')
        if self.search_parts.Value!='':
            self.parts_filter.add('search', self.search_parts.Value)
        # apply new filter and reload
        self._loadParts()

    def onButtonRefreshPartsClick( self, event ):
        self._loadParts()

    def onTreePartsItemBeginDrag( self, event ):
        part = self.parts_model.ItemToObject(event.GetItem())
        data =  PartDataObject(part)
        event.SetDataObject(data)

        
    def onTreePartsItemDrop( self, event ):
        event.Allow()

    def onTreePartsItemCollapsed( self, event ):
        event.Skip()
    
    def onTreePartsItemExpanded( self, event ):
        event.Skip()
    
    def onTreePartsSelectionChanged( self, event ):
        part = None
        if event.GetItem():
            part = self.parts_model.ItemToObject(event.GetItem())
        self.show_part(part)

    def onButtonPartFootprintClick( self, event ):
        footprint = self.button_part_footprint.Value
        frame = DropdownFrame(self.button_part_footprint, SelectFootprintFrame, footprint)
        frame.Dropdown(self.onSetFootprintCallback)
    
    def onSetFootprintCallback(self, footprint):
        if footprint:
            self.button_part_footprint.Label = footprint.name
        else:
            self.button_part_footprint.Label = "<none>"
        self.button_part_footprint.Value = footprint
        
    def onButtonPartEditApply( self, event ):
        try:
            self.edit_part_object.name = self.edit_part_name.Value
            self.edit_part_object.description = self.edit_part_description.Value
            self.edit_part_object.comment = self.edit_part_comment.Value
            self.edit_part_object.footprint = self.button_part_footprint.Value
            if self.edit_state=='edit':
                # update part on server
                PartsQuery().update(self.edit_part_object)
            elif self.edit_state=='add':
                PartsQuery().create(self.edit_part_object)
            self._loadParts()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        self.edit_state = None
    
    def onButtonPartEditCancel( self, event ):
        part = None
        if self.tree_parts.GetSelection():
            part = self.parts_model.ItemToObject(self.tree_parts.GetSelection())
        self.edit_state = None
        self.show_part(part)

    def onButtonOctopartClick( self, event ):
        search = self.edit_part_name.Value
        frame = DropdownDialog(self.button_part_footprint, SelectOctopartFrame, search)
        frame.Dropdown(self.onSetOctopartCallback)

    def onSetOctopartCallback(self, part):
        if part:
            print part
