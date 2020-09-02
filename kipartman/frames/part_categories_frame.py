from dialogs.panel_part_categories import PanelPartCategories
import api.data.part_category
import api.models
import wx
import wx.lib.newevent
import helper.tree

class PartCategory(helper.tree.TreeContainerLazyItem):
    def __init__(self, category):
        super(PartCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        if col==0:
            return self.category.name 
        elif col==1:
            return self.category.description
        return ""

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def Load(self):
        for child in api.data.part_category.find_childs(self.category):
            self.AddChild(PartCategory(child))

    def IsContainer(self):
        if self.category.is_leaf_node()==False:
            return True
        return False

    def GetDragData(self):
        return {'id': self.category.id}

    def __repr__(self):
        return '%d: %s' % (self.category.id, self.category.name)

class TreeManagerPartCategory(helper.tree.TreeManager):
    def __init__(self, *args, **kwargs):
        super(TreeManagerPartCategory, self).__init__(*args, **kwargs)

    def Load(self):
        
        self.SaveState()

        for category in api.data.part_category.find_childs():
            categoryobj = self.FindCategory(category.id)
            
            if categoryobj is None:
                categoryobj = self.AppendCategory(None, category)
            else:
                categoryobj.category = category
                self.Update(categoryobj)
        
        self.PurgeState()
    
    def FindCategory(self, id):
        for data in self.data:
            if isinstance(data, PartCategory) and data.category.id==id:
                return data
        return None
    
    def AppendCategory(self, parent, category):
        categoryobj = PartCategory(category)
        self.Append(parent, categoryobj)
        return categoryobj

(SelectCategoryEvent, EVT_SELECT_CATEGORY) = wx.lib.newevent.NewEvent()

class PartCategoriesFrame(PanelPartCategories): 
    def __init__(self, *args, **kwargs): 
        super(PartCategoriesFrame, self).__init__(*args, **kwargs)

        # create categories list
        self.tree_categories_manager = TreeManagerPartCategory(self.tree_categories, context_menu=self.menu_category)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
#         self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
#         self.tree_categories_manager.DropAccept(DataModelPart, self.onTreeCategoriesDropPart)
        self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged
        self.tree_categories_manager.OnItemBeforeContextMenu = self.onTreeCategoriesBeforeContextMenu

        self.loaded = False

    def activate(self):
        if self.loaded==False:
            self.tree_categories_manager.Clear()
            self.tree_categories_manager.Load()
            
        self.loaded = True

    def UnselectAll(self):
        self.tree_categories.UnselectAll()
        
    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        if item.IsOk()==False:
            return
        categoryobj = self.tree_categories_manager.ItemToObject(item)
        wx.PostEvent(self, SelectCategoryEvent(category=categoryobj.category))
        event.Skip()

    def onTreeCategoriesBeforeContextMenu( self, event ):
        item = self.tree_categories.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_categories_manager.ItemToObject(item)

        self.menu_category_add_category.Enable(True)
        self.menu_category_edit_category.Enable(True)
        self.menu_category_remove_category.Enable(True)
        if isinstance(obj, PartCategory)==False:
            self.menu_category_edit_category.Enable(False)
            self.menu_category_remove_category.Enable(False)
        event.Skip()
