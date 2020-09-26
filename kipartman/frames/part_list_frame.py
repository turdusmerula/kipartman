from dialogs.panel_part_list import PanelPartList
import frames.edit_part_frame
from frames.select_part_frame import SelectPartFrame, EVT_SELECT_PART_OK_EVENT
from frames.dropdown_dialog import DropdownDialog
from frames.models.tree_manager_parts import PartCategory, Part, TreeManagerParts
import api.data.part
import helper.filter
from helper.log import log
from helper.profiler import Trace
import wx
from helper.exception import print_stack


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
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelectionChanged
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
    
    @EditMode.setter
    def EditMode(self, value):
        self._edit_mode = value
        if self._edit_mode:
            wx.PostEvent(self, EnterEditModeEvent())        
        else:
            wx.PostEvent(self, ExitEditModeEvent())        
            
    def activate(self):
        self.tree_parts_manager.Load()

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

    def onTreePartsSelectionChanged( self, event ):
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
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part)==False:
            return

        dropdown = DropdownDialog(self, SelectPartFrame, "")
        dropdown.panel.Bind( EVT_SELECT_PART_OK_EVENT, self.onSelectEquivalentPartCallback )
        dropdown.Dropdown()

    def onSelectEquivalentPartCallback(self, event):
        print("---", event.data)
        item = self.tree_parts.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part)==False:
            return

        try:
            child = event.data
            obj.part.childs.add_pending(child)
            api.data.part.save(obj.part)
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
            return

        self.tree_parts_manager.Load()
        
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

