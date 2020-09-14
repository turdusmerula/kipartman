from dialogs.panel_part_categories import PanelPartCategories
from frames.edit_category_frame import EditCategoryFrame
import api.data.part_category
import api.models
import wx
import wx.lib.newevent
import helper.tree
from helper.exception import print_stack

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

    def Load(self, manager):
        print("~~ Load", self.category.id, self.category.name)
        
#         for childcategory in api.data.part_category.find_childs(self.category):
#             childcategoryobj = self.FindCategoryChild(childcategory)
#             print("~~~", childcategoryobj)
#             if childcategoryobj is None:
#                 self.AddChild(PartCategory(childcategory))
#             else:
#                 childcategoryobj.category = childcategory

        for childcategory in api.data.part_category.find_childs(self.category):
            childcategoryobj = manager.FindCategory(childcategory.id)
            print("~~~", childcategoryobj)
            if childcategoryobj is None:
                manager.Append(self, PartCategory(childcategory))
            else:
                childcategoryobj.category = childcategory
                manager.Update(childcategoryobj)
                
    def HasChilds(self):
        if self.category.is_leaf_node()==False:
            return True
        return False

    def GetDragData(self):
        return {'id': self.category.id}

    def FindCategoryChild(self, category):
        for child in self.childs:
            if isinstance(child, PartCategory) and child.category.id==category.id:
                return child
        return None
        
    def __repr__(self):
        return '%d: %s' % (self.category.id, self.category.name)

class TreeManagerPartCategory(helper.tree.TreeManager):
    def __init__(self, *args, **kwargs):
        super(TreeManagerPartCategory, self).__init__(*args, **kwargs)

    def Load(self):
        print("----")

        self.SaveState()

        for category in api.data.part_category.find_childs():
            print("**", category.name)
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
        
    def onButtonRefreshCategoriesClick( self, event ):
        self.tree_categories_manager.Load()
        event.Skip()

    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        if item.IsOk()==False:
            return
        categoryobj = self.tree_categories_manager.ItemToObject(item)
        print("###", categoryobj.IsContainer(), categoryobj.category.name, categoryobj.category.id)
        if categoryobj.childs is not None:
            print("####", categoryobj.childs)
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

    def onMenuCategoryAddCategory( self, event ):
        category = EditCategoryFrame(self).addCategory(api.data.part_category.create())
        if category is not None:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                parentobj = None
                category.parent = None
                if parentitem.IsOk():
                    parentobj = self.tree_categories_manager.ItemToObject(parentitem)
                    category.parent = parentobj.category
                      
                # create category
                category = api.data.part_category.save(category)
                
                # update categories
                self.tree_categories_manager.Load()

                if parentobj is not None:
                    self.tree_categories_manager.Expand(parentobj)
                    
                # select created item
                categoryobj = self.tree_categories_manager.FindCategory(category.id)
                if categoryobj is not None:
                    self.tree_categories_manager.Select(categoryobj)
                
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
 
    def onMenuCategoryEditCategory( self, event ):
        sel = self.tree_categories.GetSelection()
        if sel.IsOk()==False:
            return
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        category = EditCategoryFrame(self).editCategory(categoryobj.category)
        if not category is None:
            try:
                # create category
                api.data.part_category.save(category)
                
                # update categories
                self.tree_categories_manager.Load()                
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
 
    def onMenuCategoryRemoveCategory( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        try:
            res = wx.MessageDialog(self, "Remove category '"+categoryobj.category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # create category
                api.data.part_category.delete(categoryobj.category)
                # update categories
                self.tree_categories_manager.Load()                
            else:
                return
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
