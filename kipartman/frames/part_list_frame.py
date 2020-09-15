from dialogs.panel_part_list import PanelPartList
import frames.edit_part_frame
import api.data.part
import helper.tree
import helper.filter
from helper.log import log
from helper.profiler import Trace
import os
import wx
from helper.exception import print_stack

class PartCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(PartCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        if col==0:
            return self.category.id
        elif col==1:
            return self.category.path

        return ""

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
        return True

    def IsEnabled(self, col):
        return False

class Part(helper.tree.TreeContainerLazyItem):
    def __init__(self, part):
        self.part = part
        
        super(Part, self).__init__()
        
    def GetValue(self, col):
        if col==0:
            return self.part.id
        elif col==1:
            return self.part.name
        elif col==2:
            return self.part.description
        elif col==3:
            return self.part.comment
        elif col==4:
            if self.part.symbol:
                return self.part.symbol.name
        elif col==5:
            footprint = ""
            if self.part.footprint:
                footprint = os.path.basename(self.part.footprint.source_path).replace('.kicad_mod', '')
            return footprint

        return ""

    def Load(self, manager):
        for child in api.data.part.find([api.data.part.FilterChilds(self.part)]):
            manager.Append(self, Part(child))
    
    def HasChilds(self):
        if self.part.child_count>0:
            return True
        return False
    
class TreeManagerParts(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, filters, **kwargs):
        model = TreeModelPart()
        super(TreeManagerParts, self).__init__(tree_view, model, *args, **kwargs)

        self.filters = filters
        
        self.flat = False

    def Load(self):
        
        self.SaveState()
        
        if self.flat:
            self.LoadFlat()
        else:
            self.LoadTree()
        
        self.PurgeState()


    def LoadFlat(self):
        for part in api.data.part.find(filters=self.filters.get_filters()):
            partobj = self.FindPart(part.id)
            if partobj is None:
                partobj = Part(part)
                self.Append(None, partobj)
            else:
                partobj.part = part
                self.Update(partobj)
            
    def LoadTree(self):
        for part in api.data.part.find(filters=self.filters.get_filters()):
            partobj = self.FindPart(part.id)
            
            if part.category is not None:
                categoryobj = self.FindCategory(part.category.id)
                 
                if categoryobj is None:
                    categoryobj = PartCategory(part.category)
                    self.Append(None, categoryobj)
                else:
                    categoryobj.category = part.category
                    self.Update(categoryobj)
            else:
                categoryobj = None
                
            if partobj is None:
                partobj = Part(part)
                self.Append(categoryobj, partobj)
            else:
                partobj.part = part
                self.Update(partobj)
    
    def FindPart(self, id):
        for data in self.data:
            if isinstance(data, Part) and ( isinstance(data.parent, PartCategory) or data.parent is None ) and data.part.id==id:
                return data
        return None
    
    def FindCategory(self, id):
        for data in self.data:
            if isinstance(data, PartCategory) and data.category.id==id:
                return data
        return None

    def FindCategories(self,):
        res = []
        for data in self.data:
            if isinstance(data, PartCategory):
                res.append(data)
        return res

class TreeModelPart(helper.tree.TreeModel):
    def __init__(self):
        super(TreeModelPart, self).__init__()

(EnterEditModeEvent, EVT_ENTER_EDIT_MODE) = wx.lib.newevent.NewEvent()
(ExitEditModeEvent, EVT_EXIT_EDIT_MODE) = wx.lib.newevent.NewEvent()

class PartListFrame(PanelPartList): 
    def __init__(self, *args, **kwargs): 
        super(PartListFrame, self).__init__(*args, **kwargs)

        # parts filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        
        # create part list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts, context_menu=self.menu_part, filters=self.Filters)
        self.tree_parts_manager.AddIntegerColumn("id")
        self.tree_parts_manager.AddTextColumn("name")
        self.tree_parts_manager.AddTextColumn("description")
        self.tree_parts_manager.AddIntegerColumn("comment")
        self.tree_parts_manager.AddTextColumn("symbol")
        self.tree_parts_manager.AddTextColumn("footprint")
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged
        self.tree_parts_manager.OnItemBeforeContextMenu = self.onTreePartsBeforeContextMenu

        # create edit part panel
        self.panel_edit_part = frames.edit_part_frame.EditPartFrame(self.splitter_horz)
        self.panel_edit_part.Bind( frames.edit_part_frame.EVT_EDIT_PART_APPLY_EVENT, self.onEditPartApply )
        self.panel_edit_part.Bind( frames.edit_part_frame.EVT_EDIT_PART_CANCEL_EVENT, self.onEditPartCancel )

        # organize panels
        self.splitter_horz.Unsplit()
        self.splitter_horz.SplitHorizontally( self.panel_up, self.panel_edit_part)
        self.panel_down.Hide()

        # initial state
        self.toolbar_part.ToggleTool(self.toggle_part_path.GetId(), True)
        self.Flat = False
        self.EditMode = False
        
    @property
    def Filters(self):
        return self._filters

    @property
    def Flat(self):
        return self.tree_parts_manager.flat
    
    @Flat.setter
    def Flat(self, value):
        self.tree_parts_manager.flat = value
        self.tree_parts_manager.Clear()
        self.tree_parts_manager.Load()
        self._expand_categories()
    
    @property
    def EditMode(self):
        return self._edit_mode
    
    @Flat.setter
    def EditMode(self, value):
        self._edit_mode = value
        if self._edit_mode:
            wx.PostEvent(self, EnterEditModeEvent())        
        else:
            wx.PostEvent(self, ExitEditModeEvent())        
            
    def activate(self):
        pass

    def _expand_categories(self):
        if self.Flat==False:
            for category in self.tree_parts_manager.FindCategories():
                self.tree_parts_manager.Expand(category)
    
    def _enable(self, value):
        self.panel_up.Enabled = value
        
    def SetPart(self, part):
        self.panel_edit_part.SetPart(part)
        self._enable(True)
        
    def EditPart(self, part):
        self.EditMode = True
        self.panel_edit_part.EditPart(part)
        self._enable(False)
                
    def onToggleCategoryPathClicked( self, event ):
        self.Flat = not self.toolbar_part.GetToolState(self.toggle_part_path.GetId())
        event.Skip()

    def onButtonRefreshPartsClick( self, event ):
        self.tree_parts_manager.Load()
        event.Skip()
        
    def onFilterChanged( self, event ):
        self.tree_parts_manager.Load()
        self._expand_categories()
        event.Skip()

    def onTreePartsSelChanged( self, event ):
        item = self.tree_parts.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part):
            self.SetPart(obj.part)
        event.Skip()

    def onTreePartsBeforeContextMenu( self, event ):
        item = self.tree_parts.GetSelection()
        obj = None
        if item.IsOk():
            obj = self.tree_parts_manager.ItemToObject(item)

        self.menu_part_add_part.Enable(True)
        self.menu_part_edit_part.Enable(True)
        self.menu_part_remove_part.Enable(True)
        self.menu_part_duplicate_part.Enable(True)
        self.menu_part_append_equivalent.Enable(True)
        if isinstance(obj, Part)==False:
            self.menu_part_edit_part.Enable(False)
            self.menu_part_remove_part.Enable(False)
            self.menu_part_duplicate_part.Enable(False)
            self.menu_part_append_equivalent.Enable(False)
        event.Skip()

    def onMenuPartAddPart( self, event ):
        part = api.data.part.create()
        
        item = self.tree_parts.GetSelection()
        part.category = None
        if item.IsOk():
            obj = self.tree_parts_manager.ItemToObject(item)
            if isinstance(obj, PartCategory):
                part.category = obj.category
            elif isinstance(obj, Part):
                part.category = obj.part.category
        else:
            # add category from filter
            part.category = None
            if len(self.Filters.get_filters_group('category'))==1:
                part.category = self.Filters.get_filters_group('category')[0].category

        self.EditPart(part)
        event.Skip()

    def onMenuPartEditPart( self, event ):
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part)==False:
            return
        self.EditPart(obj.part)
        event.Skip()

    def onMenuPartRemovePart( self, event ):
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part)==False:
            return
        part = obj.part
        if isinstance(obj.parent, Part):
            parent = obj.parent.part
            res = wx.MessageDialog(self, "Remove part '"+part.name+"' from '"+parent.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                # remove selected part from subparts
                parent = rest.api.find_part(parent.id, with_childs=True)
                for child in parent.childs:
                    if child.id==part.id:
                        parent.childs.remove(child)
 
                #parent.childs.remove(part)
                rest.api.update_part(parent.id, parent)
                self.tree_parts_manager.DeleteChildPart(parent, part)
            else:
                return 
        else:
            res = wx.MessageDialog(self, "Remove part '"+part.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                try:
                    # remove part
                    api.data.part.delete(part)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), 'Error updating stock', wx.OK | wx.ICON_ERROR)
                    return
            else:
                return
        self.SetPart(None)
        
        self.tree_parts_manager.Load()
        event.Skip()

    def onMenuPartDuplicatePart( self, event ):
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part)==False:
            return

        part = api.data.part.duplicate(obj.part)
        self.EditPart(part)
        event.Skip()

    def onMenuPartAppendEquivalentPart( self, event ):
        event.Skip()

    def onEditPartApply( self, event ):
        part = event.part
        new_part = part.id is None

        try:
            api.data.part.save(part)
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return
        
        if new_part:
            partobj = Part(part)
            categoryobj = self.tree_parts_manager.FindCategory(part.category.id)
            self.tree_parts_manager.Append(categoryobj, partobj)
            
        self.tree_parts_manager.Load()

        # reload the part after changing it
        item = self.tree_parts.GetSelection()
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part):
            self.SetPart(obj.part)
        else:
            self.SetPart(None)
            
        self.EditMode = False
        event.Skip()
      
    def onEditPartCancel( self, event ):
        self.tree_parts_manager.Load()
        
        # reload the part after changing it
        item = self.tree_parts.GetSelection()
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part):
            self.SetPart(obj.part)
        else:
            self.SetPart(None)

        self.EditMode = False        
        event.Skip()

