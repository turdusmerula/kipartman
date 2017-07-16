from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_part_frame import EditPartFrame, EVT_EDIT_PART_APPLY_EVENT, EVT_EDIT_PART_CANCEL_EVENT
import wx.dataview
import json
import copy
import helper.tree
from helper.filter import Filter
import rest

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


class DataModelCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        vMap = { 
            0 : self.category.name,
            1 : self.category.description,
        }
        return vMap[col]


class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==1:
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False
    
class DataModelPart(helper.tree.TreeContainerLazyItem):
    def __init__(self, part):
        super(DataModelPart, self).__init__()
        self.part = part
        if part.has_childs:
            # add a fake item
            self.childs.append(None)
            
    def GetValue(self, col):
        vMap = { 
            0 : str(self.part.id),
            1 : self.part.name,
            2 : self.part.description,
            3 : self.part.comment
        }
        return vMap[col]

    def Load(self, manager):
        print "Lazy load"
        if self.part.has_childs==False:
            return
        part = rest.api.find_part(self.part.id, with_childs=True)
        
        for child in part.childs:
            manager.AppendItem(self, DataModelPart(child))

class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        
        # create categories list
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")

        # parts filters
        self.parts_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)
        
        # create parts list
        self.tree_parts_manager = helper.tree.TreeManager(self.tree_parts)
        self.tree_parts_manager.AddIntegerColumn("id")
        self.tree_parts_manager.AddTextColumn("name")
        self.tree_parts_manager.AddTextColumn("description")
        self.tree_parts_manager.AddIntegerColumn("comment")
        # 
#         # create parts drag and drop targets
#         self.tree_parts.EnableDragSource(wx.DataFormat(wx.TextDataObject().GetFormat()))
#         p_dt = PartDropTarget(self)
#         self.tree_parts.EnableDropTarget(wx.DataFormat(wx.DF_TEXT))
#         self.tree_parts.SetDropTarget(p_dt)

        # create edit part panel
        self.panel_edit_part = EditPartFrame(self.part_splitter)
        self.part_splitter.SplitHorizontally(self.part_splitter.Window1, self.panel_edit_part, 400)
        self.panel_edit_part.Bind( EVT_EDIT_PART_APPLY_EVENT, self.onEditPartApply )
        self.panel_edit_part.Bind( EVT_EDIT_PART_CANCEL_EVENT, self.onEditPartCancel )

        # initial edit state
        self.show_part(None)
        self.edit_state = None
        
        self.load()
        
    def loadCategories(self):
        # clear all
        self.tree_categories_manager.ClearItems()
        
        # load categories
        categories = rest.api.find_parts_categories()

        # load tree
        to_add = []
        id_category_map = {}
        for category in categories:
            to_add.append(category)
        while len(to_add)>0:
            category = to_add[0]
            id_category_map[category.id] = DataModelCategory(category)
            to_add.pop(0)
            
            # add to model
            if category.parent:
                self.tree_categories_manager.AppendItem(id_category_map[category.parent.id], id_category_map[category.id])
            else:
                self.tree_categories_manager.AppendItem(None, id_category_map[category.id])
            
            # load childs
            if category.childs:
                for child in category.childs:
                    to_add.append(child)
        
    def loadParts(self):
        # clear all
        self.tree_parts_manager.ClearItems()
        
        # load parts
        parts = rest.api.find_parts()

        # load categories
        categories = {}
        for part in parts:
            if part.category:
                category_name = part.category.path
                print part.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(part.category)
                self.tree_parts_manager.AppendItem(None, categories[category_name])
            self.tree_parts_manager.AppendItem(categories[category_name], DataModelPart(part))
        
    def load(self):
        try:
            self.loadCategories()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        try:
            self.loadParts()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def show_part(self, part):
        # disable editing
        self.panel_edit_part.enable(False)
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_parts.Enabled = True
        # set part
        self.panel_edit_part.SetPart(part)
        
    def edit_part(self, part):
        self.show_part(part)
        # enable editing
        self.panel_edit_part.enable(True)
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
            self.loadCategories()
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

#     def onTreeCategoriesOnChar( self, event ):
#         keycode = event.GetKeyCode()
#         if keycode == wx.WXK_SPACE:
#             sel = self.tree_categories.GetSelection()
#             # unselect current item
#             self.tree_categories.SelectItem(self.tree_categories.RootItem)
#             # update state
#             self.part_categories_state.update(sel)
#             self.part_categories_state.update(self.tree_categories.RootItem)            
#         event.Skip()
# 
#     def onTreeCategoriesSelChanging( self, event ):
#         item = self.tree_categories.GetSelection()
#         self.part_categories_state.update(item, selected=False)
#         
#     def onTreeCategoriesSelChanged( self, event ):
#         item = self.tree_categories.GetSelection()
#         category = self.tree_categories.GetItemData(item)
#         self.part_categories_state.update(item, selected=True)
#         self.part_categories_state.debug()
#         # set category filter
#         self.parts_filter.remove('category')
#         if category:
#             self.parts_filter.add('category', category.id, category.name)
#         # apply new filter and reload
#         self._loadParts()
# 
# 
#     def onTreeCategoriesCollapsed( self, event ):
#         self.part_categories_state.update(event.GetItem(), expanded=False)
#         event.Skip()
#     
#     def onTreeCategoriesExpanded( self, event ):
#         self.part_categories_state.update(event.GetItem(), expanded=True)
#         event.Skip()
#         
#     def onTreeCategoriesBeginDrag( self, event ):
#         category = self.tree_categories.GetItemData(event.GetItem())
#         data = PartCategoryDataObject(category)
#         dropSource = wx.DropSource(self)
#         dropSource.SetData(data)
#         result = dropSource.DoDragDrop(flags=wx.Drag_DefaultMove)
#         print type(result)
#         if result==wx.DragCopy:
# #            CopyPartCategory()
#             pass
#         elif result==wx.DragMove:
# #            MoveMyData()
#             pass
# 
#     def onTreeCategoriesEndDrag( self, event ):
#         event.Allow()


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
        self.loadParts()

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

    def onTreePartsItemExpanding( self, event ):
        item = event.GetItem()
        print type(item)
        if item:
            obj = self.parts_model.ItemToObject(item)
        if isinstance(obj, DataModelPart) and obj.part.has_childs and obj.childs_loaded==False:
            print "Loading childs", obj.part.id
            part = rest.api.find_part(obj.part.id, with_childs=True)
            obj.part.childs = part.childs
            
            for child in obj.part.childs:
                for part in obj.part.childs:
                    item. children.append(self.ObjectToItem(DataModelPart(part, obj)))
            self.parts_model.ItemsChanged(item)
            
    
    def onTreePartsSelectionChanged( self, event ):
        part = None
        if event.GetItem():
            part = self.parts_model.ItemToObject(event.GetItem())
        self.show_part(part)

    def onEditPartApply( self, event ):
        part = event.data
        try:
            if self.edit_state=='edit':
                # update part on server
                PartsQuery().update(part)
            elif self.edit_state=='add':
                part = PartsQuery().create(part)
            
            # apply changes on readonly parameters, this is not made through the previous request 
            self.panel_edit_part.ApplyChanges(part)
            
            self._loadParts()
        except QueryError as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        self.edit_state = None
    
    def onEditPartCancel( self, event ):
        part = None
        if self.tree_parts.GetSelection():
            part = self.parts_model.ItemToObject(self.tree_parts.GetSelection())
        self.edit_state = None
        self.show_part(part)
