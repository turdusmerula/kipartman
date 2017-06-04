from dialogs.panel_footprints import PanelFootprints
from frames.edit_category_frame import EditCategoryFrame
from api.queries import FootprintsQuery, FootprintCategoriesQuery
from rest_client.exceptions import QueryError
import wx.dataview
import json
from api import models
import copy
from helper.tree_state import TreeState
from helper.tree import Tree
from helper.filter import Filter

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class FootprintCategoryDataObject(wx.TextDataObject):
    def __init__(self, category): 
        super(FootprintCategoryDataObject, self).__init__()
        self.category = category
        self.SetText(json.dumps({'model': 'FootprintCategory', 'url': category.path, 'id': category.id}))
        
    
class FootprintCategoryDropTarget(wx.TextDropTarget):
    def __init__(self, frame):
        self.frame = frame
        super(FootprintCategoryDropTarget, self).__init__()
    
    #TODO: set drag cursor depending on accept/reject drop
    def OnDropText(self, x, y, text):
        data = json.loads(text)
        print "FootprintCategoryDropTarget.OnDropText", data, x, y
        item, _ = self.frame.tree_categories.HitTest((x, y))
        if item.IsOk():
            target_category = self.frame.tree_categories.GetItemData(item)
        else:
            target_category = None
        if data['model']=='FootprintCategory':
            source_category = FootprintCategoriesQuery().get(data['id'])[0]
            if source_category:
                source_category.parent = target_category
            FootprintCategoriesQuery().update(source_category)
        elif data['model']=='Footprint':
            source_footprint = FootprintsQuery().get(data['id'])[0]
            if source_footprint:
                source_footprint.category = target_category
                FootprintsQuery().update(source_footprint)
        self.frame.load()
        return wx.DragMove


class FootprintDataObject(wx.TextDataObject):
    def __init__(self, category): 
        super(FootprintDataObject, self).__init__()
        self.category = category
        self.SetText(json.dumps({'model': 'Footprint', 'url': category.path, 'id': category.id}))

class FootprintDropTarget(wx.TextDropTarget):
    def __init__(self, frame):
        self.frame = frame
        super(FootprintDropTarget, self).__init__()
    
    #TODO: set drag cursor depending on accept/reject drop
    def OnDropText(self, x, y, text):
        data = json.loads(text)
        print "FootprintDropTarget.OnDropText", data, x, y
        item, _ = self.frame.tree_footprints.HitTest((x, y))
        if item.IsOk():
            # do a copy to avoid nasty things
            target_footprint = copy.deepcopy(self.frame.footprints_model.ItemToObject(item))
        else:
            target_footprint = None
        if data['model']=='Footprint':
            source_footprint = FootprintsQuery().get(data['id'])[0]
            if source_footprint and target_footprint:
                target_footprint.footprints.append(source_footprint.id)
                FootprintsQuery().update(target_footprint)
        self.frame._loadFootprints()
        return wx.DragMove


class FootprintDataModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(FootprintDataModel, self).__init__()
        self.data = FootprintsQuery().get()
    
    def Filter(self, footprint_filter=None):
        if footprint_filter:
            self.data = FootprintsQuery(**footprint_filter).get()
        
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
            for footprint in self.data:
                children.append(self.ObjectToItem(footprint))
            return len(self.data)
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
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

class FootprintsFrame(PanelFootprints): 
    def __init__(self, parent):
        super(FootprintsFrame, self).__init__(parent)
        # create categories data
        self.footprint_categories_state = TreeState(self.tree_categories)
        self.footprint_categories_tree = Tree(self.tree_categories)
        # create footprints data
        self.footprint_state = TreeState(self.tree_footprints)
        # create category drop targets
        pc_dt = FootprintCategoryDropTarget(self)
        self.tree_categories.SetDropTarget(pc_dt)
        # footprints filters
        self.footprints_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)
        # create footprints list
        self.footprints_model = FootprintDataModel()
        self.tree_footprints.AssociateModel(self.footprints_model)
        # add default columns
        self.tree_footprints.AppendTextColumn("id", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_footprints.AppendTextColumn("name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_footprints.AppendTextColumn("description", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_footprints.AppendTextColumn("comment", 3, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_footprints.Columns:
            c.Sortable = True
            c.Reorderable = True

        # create footprints drag and drop targets
        self.tree_footprints.EnableDragSource(wx.DataFormat(wx.TextDataObject().GetFormat()))
        p_dt = FootprintDropTarget(self)
        self.tree_footprints.EnableDropTarget(wx.DataFormat(wx.DF_TEXT))
        self.tree_footprints.SetDropTarget(p_dt)

        # initial edit state
        self.show_footprint(None)
        self.edit_state = None
        self.edit_footprint_object = None

        self.load() 
        
    def _loadCategories(self):
        self.tree_categories.DeleteAllItems()
        
        # path to tree item map
        path_to_item = {}
        
        # root node
        self.tree_categories.AddRoot('root')
        self.footprint_categories_state.update(self.tree_categories.GetRootItem())
        path_to_item[None] = self.tree_categories.GetRootItem()

        # retrieve categories
        categories = FootprintCategoriesQuery().get()

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
            if path and self.footprint_categories_state.expanded(path):
                self.tree_categories.Expand(path_to_item[path])
            if self.footprint_categories_state.selected(path):
                self.tree_categories.SelectItem(path_to_item[path])

        self.footprint_categories_tree.sort()

    def _loadFootprints(self):
        # apply new filter and reload
        self.footprints_model.Cleared()
        self.footprints_model = FootprintDataModel()
        self.footprints_model.Filter(self.footprints_filter.query_filter())
        self.tree_footprints.AssociateModel(self.footprints_model)

    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self._loadCategories()
            self._loadFootprints()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)


    def show_footprint(self, footprint):
        # disable editing
        self.panel_edit_footprint.Enabled = False
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_footprints.Enabled = True
        if footprint:
            self.edit_footprint_name.Value = footprint.name
            self.edit_footprint_description.Value = footprint.description
            self.edit_footprint_comment.Value = footprint.comment
        else:
            self.edit_footprint_name.Value = ''
            self.edit_footprint_description.Value = ''
            self.edit_footprint_comment.Value = ''
            
    
    def edit_footprint(self, footprint):
        self.show_footprint(footprint)
        self.edit_footprint_object = footprint
        # enable editing
        self.panel_edit_footprint.Enabled = True
        # disable evrything else
        self.panel_category.Enabled = False
        self.panel_footprints.Enabled = False
        
    def new_footprint(self):
        self.edit_footprint(models.Footprint())


    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.footprints_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self._loadFootprints()
    
    def onButtonRefreshCategoriesClick( self, event ):
        try:
            self._loadCategories()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(models.FootprintCategory)
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                category.parent = None
                if parentitem:
                    category.parent = self.tree_categories.GetItemData(parentitem)
                # create category on server
                category = FootprintCategoriesQuery().create(category)
                # create category on treeview
                newitem = self.tree_categories.AppendItem(parent=parentitem, text=category.name) 
                # add category to item element
                self.tree_categories.SetItemData(newitem, category)
                self.tree_categories.SelectItem(newitem)
                self.footprint_categories_tree.sort(parentitem)
                # set node state
                self.footprint_categories_state.update(newitem)
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
                category = FootprintCategoriesQuery().update(category)
                self.tree_categories.SetItemData(sel, category)
                self.tree_categories.SetItemText(sel, category.name)
                self.footprint_categories_tree.sort(self.tree_categories.GetItemParent(sel))
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
                FootprintCategoriesQuery().delete(category)
                self._loadCategories()
            else:
                return
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        # remove category status
        self.footprint_categories_state.remove(category.path)        

    def onTreeCategoriesOnChar( self, event ):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            sel = self.tree_categories.GetSelection()
            # unselect current item
            self.tree_categories.SelectItem(self.tree_categories.RootItem)
            # update state
            self.footprint_categories_state.update(sel)
            self.footprint_categories_state.update(self.tree_categories.RootItem)            
        event.Skip()

    def onTreeCategoriesSelChanging( self, event ):
        item = self.tree_categories.GetSelection()
        self.footprint_categories_state.update(item, selected=False)
        
    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = self.tree_categories.GetItemData(item)
        self.footprint_categories_state.update(item, selected=True)
        self.footprint_categories_state.debug()
        # set category filter
        self.footprints_filter.remove('category')
        if category:
            self.footprints_filter.add('category', category.id, category.name)
        # apply new filter and reload
        self._loadFootprints()


    def onTreeCategoriesCollapsed( self, event ):
        self.footprint_categories_state.update(event.GetItem(), expanded=False)
        event.Skip()
    
    def onTreeCategoriesExpanded( self, event ):
        self.footprint_categories_state.update(event.GetItem(), expanded=True)
        event.Skip()
        
    def onTreeCategoriesBeginDrag( self, event ):
        category = self.tree_categories.GetItemData(event.GetItem())
        data = FootprintCategoryDataObject(category)
        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)
        print type(result)
        if result==wx.DragCopy:
#            CopyFootprintCategory()
            pass
        elif result==wx.DragMove:
#            MoveMyData()
            pass

    def onTreeCategoriesEndDrag( self, event ):
        event.Allow()


    def onButtonAddFootprintClick( self, event ):
        self.edit_state = 'add'
        self.new_footprint()

    def onButtonEditFootprintClick( self, event ):
        if not self.tree_footprints.GetSelection():
            return
        footprint = self.footprints_model.ItemToObject(self.tree_footprints.GetSelection())
        self.edit_state = 'edit'
        self.edit_footprint(footprint)

    def onButtonRemoveFootprintClick( self, event ):
        item = self.tree_footprints.GetSelection()
        if not item:
            return 
        footprint = self.footprints_model.ItemToObject(item)
        res = wx.MessageDialog(self, "Remove footprint '"+footprint.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
        if res==wx.ID_OK:
            # remove footprint
            FootprintsQuery().delete(footprint)
        else:
            return
        self._loadFootprints()
        event.Skip()

    def onSearchFootprintsTextEnter( self, event ):
        # set search filter
        self.footprints_filter.remove('search')
        if self.search_footprints.Value!='':
            self.footprints_filter.add('search', self.search_footprints.Value)
        # apply new filter and reload
        self._loadFootprints()

    def onButtonRefreshFootprintsClick( self, event ):
        self._loadFootprints()

    def onTreeFootprintsItemBeginDrag( self, event ):
        footprint = self.footprints_model.ItemToObject(event.GetItem())
        data =  FootprintDataObject(footprint)
        event.SetDataObject(data)

        
    def onTreeFootprintsItemDrop( self, event ):
        event.Allow()

    def onTreeFootprintsItemCollapsed( self, event ):
        event.Skip()
    
    def onTreeFootprintsItemExpanded( self, event ):
        event.Skip()
    
    def onTreeFootprintsSelectionChanged( self, event ):
        footprint = None
        if event.GetItem():
            footprint = self.footprints_model.ItemToObject(event.GetItem())
        self.show_footprint(footprint)
    
    def onButtonFootprintEditApply( self, event ):
        try:
            self.edit_footprint_object.name = self.edit_footprint_name.Value
            self.edit_footprint_object.description = self.edit_footprint_description.Value
            self.edit_footprint_object.comment = self.edit_footprint_comment.Value
            if self.edit_state=='edit':
                # update footprint on server
                FootprintsQuery().update(self.edit_footprint_object)
            elif self.edit_state=='add':
                FootprintsQuery().create(self.edit_footprint_object)
            self._loadFootprints()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        self.edit_state = None
    
    def onButtonFootprintEditCancel( self, event ):
        footprint = None
        if self.tree_footprints.GetSelection():
            footprint = self.footprints_model.ItemToObject(self.tree_footprints.GetSelection())
        self.edit_state = None
        self.show_footprint(footprint)

    def onFileFootprintImageChanged( self, event ):
        #self.file_footprint_image.GetPath()
        img = wx.Image(self.file_footprint_image.GetPath(), wx.BITMAP_TYPE_ANY)
        #img = wx.Bitmap(self.file_footprint_image.GetPath(), wx.BITMAP_TYPE_ANY)
        self.PhotoMaxSize = self.bitmap_edit_footprint.GetSize().x
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        img = img.ConvertToBitmap()

        self.bitmap_edit_footprint.SetBitmap(img)
    
