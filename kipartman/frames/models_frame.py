from dialogs.panel_models import PanelModels
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_model_frame import EditModelFrame, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
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

class TreeManagerModels(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerModels, self).__init__(tree_view)

    def FindModel(self, model_id):
        for data in self.data:
            if isinstance(data, DataModelModel) and data.model.id==model_id:
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
    
    def DeleteModel(self, model):
        modelobj = self.FindModel(model.id)
        if modelobj is None:
            return
        categoryobj = modelobj.parent
        self.DeleteItem(modelobj.parent, modelobj)
        if categoryobj and len(categoryobj.childs)==0:
            self.DeleteItem(categoryobj.parent, categoryobj)

    def UpdateModel(self, model):
        modelobj = self.FindModel(model.id)
        if modelobj is None:
            return
        self.UpdateItem(modelobj)

    def AppendCategoryPath(self, category):
        categoryobj = self.FindCategoryPath(category)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryPath(category)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendModel(self, model):
        categoryobj = self.AppendCategoryPath(model.category)
        modelobj = DataModelModel(model)
        self.AppendItem(categoryobj, modelobj)
        self.Expand(categoryobj)
        return modelobj
    

class DataModelModel(helper.tree.TreeItem):
    def __init__(self, model):
        super(DataModelModel, self).__init__()
        self.model = model
            
    def GetValue(self, col):
        vMap = { 
            0 : str(self.model.id),
            1 : self.model.name,
            2 : self.model.description,
            3 : self.model.comment
        }
        return vMap[col]

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.model.id}
        return None


class ModelsFrame(PanelModels): 
    def __init__(self, parent):
        super(ModelsFrame, self).__init__(parent)
        
        # create categories data
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
        self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
        self.tree_categories_manager.DropAccept(DataModelModel, self.onTreeCategoriesDropModel)
        self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged

        # models filters
        self.models_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create model list
        self.tree_models_manager = TreeManagerModels(self.tree_models)
        self.tree_models_manager.AddIntegerColumn("id")
        self.tree_models_manager.AddTextColumn("name")
        self.tree_models_manager.AddTextColumn("description")
        self.tree_models_manager.AddIntegerColumn("comment")
        self.tree_models_manager.OnSelectionChanged = self.onTreeModelsSelChanged
        
        # create edit model panel
        self.panel_edit_model = EditModelFrame(self.model_splitter)
        self.model_splitter.SplitHorizontally(self.model_splitter.Window1, self.panel_edit_model, 400)
        self.panel_edit_model.Bind( EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditModelApply )
        self.panel_edit_model.Bind( EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditModelCancel )
        
        # initial edit state
        self.show_model(None)
        self.edit_state = None

        self.load() 
        
    def loadCategories(self):
        # clear all
        self.tree_categories_manager.ClearItems()
        
        # load categories
        categories = rest.api.find_models_categories()

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

    def loadModels(self):
        # clear all
        self.tree_models_manager.ClearItems()
        
        # load models
        models = rest.api.find_models(**self.models_filter.query_filter())

        # load categories
        categories = {}
        for model in models:
            if model.category:
                category_name = model.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(model.category)
                self.tree_models_manager.AppendItem(None, categories[category_name])
            self.tree_models_manager.AppendItem(categories[category_name], DataModelModel(model))
        
        for category in categories:
            self.tree_models_manager.Expand(categories[category])

    # Virtual event handlers, overide them in your derived class
    def load(self):
        try:
            self.loadCategories()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        try:
            self.loadModels()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def show_model(self, model):
        # disable editing
        self.panel_edit_model.enable(False)
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_models.Enabled = True
        # set part
        self.panel_edit_model.SetModel(model)

    def edit_model(self, model):
        self.show_model(model)
        # enable editing
        self.panel_edit_model.enable(True)
        # disable evrything else
        self.panel_category.Enabled = False
        self.panel_models.Enabled = False
        
    def new_model(self):
        model = rest.model.ModelNew()
        
        # set category
        item = self.tree_categories.GetSelection()
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
            if category.category:
                model.category = category.category

        self.edit_model(model)


    def onButtonRefreshCategoriesClick( self, event ):
        self.loadCategories()

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(rest.model.ModelCategoryNew)
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
                category = rest.api.add_models_category(category)
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
                categoryobj.category = rest.api.update_models_category(categoryobj.category.id, category)
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
                rest.api.delete_models_category(categoryobj.category.id)
                self.tree_categories_manager.DeleteItem(categoryobj.parent, categoryobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.models_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self.loadModels()

    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = None
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
        # set category filter
        self.models_filter.remove('category')
        if category:
            self.models_filter.add('category', category.category.id, category.category.name)
        # apply new filter and reload
        self.loadModels()

    def onTreeCategoriesDropCategory(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
        try:
            source_category_id = data['id']
            source_category = rest.api.find_models_category(source_category_id)
            source_categoryitem = helper.tree.TreeManager.drag_item
            source_categoryobj = self.tree_categories_manager.ItemToObject(source_categoryitem)
    
            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                if source_category_id==dest_category.id:
                    return wx.DragError
                source_category.parent = rest.model.ModelCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_category.parent = None
            
            # update on server
            category = rest.api.update_models_category(source_category.id, source_category)

            # update tree model
            if source_categoryobj:
                self.tree_categories_manager.MoveItem(source_categoryobj.parent, dest_categoryobj, source_categoryobj)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        return wx.DragMove

    def onTreeCategoriesDropModel(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))

        try:
            source_model_id = data['id']
            source_model = rest.api.find_model(source_model_id)

            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                source_model.category = rest.model.ModelCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_model.category = None
            
            # update on server
            model = rest.api.update_model(source_model.id, source_model)
            
            # update tree model
            self.tree_models_manager.DeleteModel(source_model)
            self.tree_models_manager.AppendModel(model)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        return wx.DragMove

    def onTreeModelsSelChanged( self, event ):
        item = self.tree_models.GetSelection()
        model = None
        if not item.IsOk():
            return
        
        obj = self.tree_models_manager.ItemToObject(item)
        if isinstance(obj, DataModelModel):
            model = obj.model
        self.show_model(model)

    def onEditModelApply( self, event ):
        model = event.data
        try:
            if self.edit_state=='edit':
                # update part on server
                model = rest.api.update_model(model.id, model)
                self.tree_models_manager.UpdateModel(model)
            elif self.edit_state=='add':
                model = rest.api.add_model(model)
                self.tree_models_manager.AppendModel(model)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        self.edit_state = None
        self.show_model(model)
     
    def onEditModelCancel( self, event ):
        model = None
        item = self.tree_models.GetSelection()
        if item.IsOk():
            modelobj = self.tree_models_manager.ItemToObject(item)
            model = modelobj.model
        self.edit_state = None
        self.show_model(model)

    def onButtonAddModelClick( self, event ):
        self.edit_state = 'add'
        self.new_model()
        
    def onButtonEditModelClick( self, event ):
        item = self.tree_models.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_models_manager.ItemToObject(item)
        if isinstance(obj, DataModelCategoryPath):
            return
        self.edit_state = 'edit'
        self.edit_model(obj.model)
        # 
    def onButtonRemoveModelClick( self, event ):
        item = self.tree_models.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_models_manager.ItemToObject(item)
        if isinstance(obj, DataModelCategoryPath):
            return
        model = obj.model
        res = wx.MessageDialog(self, "Remove model '"+model.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
        if res==wx.ID_OK:
            # remove part
            rest.api.delete_model(model.id)
            self.tree_models_manager.DeleteModel(model)
        else:
            return
        self.show_model(None)

    def onButtonRefreshModelsClick( self, event ):
        self.loadModels()

    def onSearchModelsTextEnter( self, event ):
        # set search filter
        self.models_filter.remove('search')
        if self.search_models.Value!='':
            self.models_filter.add('search', self.search_models.Value)
        # apply new filter and reload
        self.loadModels()

    def onSearchModelsButton(self, event):
        return self.onSearchModelsTextEnter(event)
    