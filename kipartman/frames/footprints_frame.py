from dialogs.panel_footprints import PanelFootprints
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_footprint_frame import EditFootprintFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
import helper.tree
from helper.filter import Filter
import rest
import wx

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

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

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def GetDragData(self):
        return {'id': self.category.id}


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

class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerFootprints, self).__init__(tree_view)

    def FindFootprint(self, footprint_id):
        for data in self.data:
            if isinstance(data, DataModelFootprint) and data.footprint.id==footprint_id:
                return data
        return None
    
    def FindCategoryPath(self, category):
        if category:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category.id==category.id:
                    return data
        else:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category is None:
                    return data
        return None
    
    def DeleteFootprint(self, footprint):
        footprintobj = self.FindFootprint(footprint.id)
        if footprintobj is None:
            return
        categoryobj = footprintobj.parent
        self.DeleteItem(footprintobj.parent, footprintobj)
        if categoryobj and len(categoryobj.childs)==0:
            self.DeleteItem(categoryobj.parent, categoryobj)

    def UpdateFootprint(self, footprint):
        footprintobj = self.FindFootprint(footprint.id)
        if footprintobj is None:
            return
        self.UpdateItem(footprintobj)

    def AppendCategoryPath(self, category):
        categoryobj = self.FindCategoryPath(category)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryPath(category)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendFootprint(self, footprint):
        categoryobj = self.AppendCategoryPath(footprint.category)
        footprintobj = DataModelFootprint(footprint)
        self.AppendItem(categoryobj, footprintobj)
        self.Expand(categoryobj)
        return footprintobj
    

class DataModelFootprint(helper.tree.TreeItem):
    def __init__(self, footprint):
        super(DataModelFootprint, self).__init__()
        self.footprint = footprint
            
    def GetValue(self, col):
        vMap = { 
            0 : str(self.footprint.id),
            1 : self.footprint.name,
            2 : self.footprint.description,
            3 : self.footprint.comment
        }
        return vMap[col]

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.footprint.id}
        return None


class FootprintsFrame(PanelFootprints): 
    def __init__(self, parent):
        super(FootprintsFrame, self).__init__(parent)
        
        # create categories data
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
        self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
        self.tree_categories_manager.DropAccept(DataModelFootprint, self.onTreeCategoriesDropFootprint)
        self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged

        # footprints filters
        self.footprints_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create footprint list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints)
        self.tree_footprints_manager.AddIntegerColumn("id")
        self.tree_footprints_manager.AddTextColumn("name")
        self.tree_footprints_manager.AddTextColumn("description")
        self.tree_footprints_manager.AddIntegerColumn("comment")
        self.tree_footprints_manager.OnSelectionChanged = self.onTreeFootprintsSelChanged
        
        # create edit footprint panel
        self.panel_edit_footprint = EditFootprintFrame(self.footprint_splitter)
        self.footprint_splitter.SplitHorizontally(self.footprint_splitter.Window1, self.panel_edit_footprint, 400)
        self.panel_edit_footprint.Bind( EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditFootprintApply )
        self.panel_edit_footprint.Bind( EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditFootprintCancel )
        
        # initial edit state
        self.show_footprint(None)
        self.edit_state = None

        self.load() 
        
    def loadCategories(self):
        # clear all
        self.tree_categories_manager.ClearItems()
        
        # load categories
        categories = rest.api.find_footprints_categories()

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

    def loadFootprints(self):
        # clear all
        self.tree_footprints_manager.ClearItems()
        
        # load footprints
        footprints = rest.api.find_footprints(**self.footprints_filter.query_filter())

        # load categories
        categories = {}
        for footprint in footprints:
            if footprint.category:
                category_name = footprint.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(footprint.category)
                self.tree_footprints_manager.AppendItem(None, categories[category_name])
            self.tree_footprints_manager.AppendItem(categories[category_name], DataModelFootprint(footprint))
        
        for category in categories:
            self.tree_footprints_manager.Expand(categories[category])

    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self.loadCategories()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        try:
            self.loadFootprints()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def show_footprint(self, footprint):
        # disable editing
        self.panel_edit_footprint.enable(False)
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_footprints.Enabled = True
        # set part
        self.panel_edit_footprint.SetFootprint(footprint)

    def edit_footprint(self, footprint):
        self.show_footprint(footprint)
        # enable editing
        self.panel_edit_footprint.enable(True)
        # disable evrything else
        self.panel_category.Enabled = False
        self.panel_footprints.Enabled = False
        
    def new_footprint(self):
        footprint = rest.model.FootprintNew()
        
        # set category
        item = self.tree_categories.GetSelection()
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
            if category.category:
                footprint.category = category.category

        self.edit_footprint(footprint)


    def onButtonRefreshCategoriesClick( self, event ):
        self.loadCategories()

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(rest.model.FootprintCategoryNew)
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                parentobj = None
                category.parent = None
                if parentitem:
                    parentobj = self.tree_categories_manager.ItemToObject(parentitem)
                    category.parent = parentobj.category
                    
                # create category on server
                category = rest.api.add_footprints_category(category)
                # create category on treeview
                newitem = self.tree_categories_manager.AppendItem(parentobj, DataModelCategory(category)) 
                # add category to item element
                self.tree_categories_manager.SelectItem(newitem)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonEditCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        category = EditCategoryFrame(self).editCategory(categoryobj.category)
        if not category is None:
            try:
                categoryobj.category = rest.api.update_footprints_category(categoryobj.category.id, category)
                self.tree_categories_manager.UpdateItem(categoryobj)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        try:
            res = wx.MessageDialog(self, "Remove category '"+categoryobj.category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                rest.api.delete_footprints_category(categoryobj.category.id)
                self.tree_categories_manager.DeleteItem(categoryobj.parent, categoryobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.footprints_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self.loadFootprints()

    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = None
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
        # set category filter
        self.footprints_filter.remove('category')
        if category:
            self.footprints_filter.add('category', category.category.id, category.category.name)
        # apply new filter and reload
        self.loadFootprints()

    def onTreeCategoriesDropCategory(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
        try:
            source_category_id = data['id']
            source_category = rest.api.find_footprints_category(source_category_id)
            source_categoryitem = helper.tree.TreeManager.drag_item
            source_categoryobj = self.tree_categories_manager.ItemToObject(source_categoryitem)
    
            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                if source_category_id==dest_category.id:
                    return wx.DragError
                source_category.parent = rest.model.FootprintCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_category.parent = None
            
            # update on server
            category = rest.api.update_footprints_category(source_category.id, source_category)

            # update tree model
            if source_categoryobj:
                self.tree_categories_manager.MoveItem(source_categoryobj.parent, dest_categoryobj, source_categoryobj)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        return wx.DragMove

    def onTreeCategoriesDropFootprint(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))

        try:
            source_footprint_id = data['id']
            source_footprint = rest.api.find_footprint(source_footprint_id)

            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                source_footprint.category = rest.model.FootprintCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_footprint.category = None
            
            # update on server
            footprint = rest.api.update_footprint(source_footprint.id, source_footprint)
            
            # update tree model
            self.tree_footprints_manager.DeleteFootprint(source_footprint)
            self.tree_footprints_manager.AppendFootprint(footprint)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        return wx.DragMove

    def onTreeFootprintsSelChanged( self, event ):
        item = self.tree_footprints.GetSelection()
        footprint = None
        if not item.IsOk():
            return
        
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, DataModelFootprint):
            footprint = obj.footprint
        self.show_footprint(footprint)

    def onEditFootprintApply( self, event ):
        footprint = event.data
        try:
            if self.edit_state=='edit':
                # update part on server
                footprint = rest.api.update_footprint(footprint.id, footprint)
                self.tree_footprints_manager.UpdateFootprint(footprint)
            elif self.edit_state=='add':
                footprint = rest.api.add_footprint(footprint)
                self.tree_footprints_manager.AppendFootprint(footprint)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        self.edit_state = None
        self.show_footprint(footprint)
     
    def onEditFootprintCancel( self, event ):
        footprint = None
        item = self.tree_footprints.GetSelection()
        if item.IsOk():
            footprintobj = self.tree_footprints_manager.ItemToObject(item)
            footprint = footprintobj.footprint
        self.edit_state = None
        self.show_footprint(footprint)

    def onButtonAddFootprintClick( self, event ):
        self.edit_state = 'add'
        self.new_footprint()
        
    def onButtonEditFootprintClick( self, event ):
        item = self.tree_footprints.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, DataModelCategoryPath):
            return
        self.edit_state = 'edit'
        self.edit_footprint(obj.footprint)
        # 
    def onButtonRemoveFootprintClick( self, event ):
        item = self.tree_footprints.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(obj, DataModelCategoryPath):
            return
        footprint = obj.footprint
        res = wx.MessageDialog(self, "Remove footprint '"+footprint.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
        if res==wx.ID_OK:
            # remove part
            rest.api.delete_footprint(footprint.id)
            self.tree_footprints_manager.DeleteFootprint(footprint)
        else:
            return
        self.show_footprint(None)

    def onButtonRefreshFootprintsClick( self, event ):
        self.loadFootprints()

    def onSearchFootprintsTextEnter( self, event ):
        # set search filter
        self.footprints_filter.remove('search')
        if self.search_footprints.Value!='':
            self.footprints_filter.add('search', self.search_footprints.Value)
        # apply new filter and reload
        self.loadFootprints()

    def onSearchFootprintsButton(self, event):
        return self.onSearchFootprintsTextEnter(event)
    