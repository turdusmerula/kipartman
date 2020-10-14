from dialogs.panel_units import PanelUnits
import frames.edit_unit_frame
import wx
import helper.filter
from helper.exception import print_stack
import api.data.unit

class Unit(helper.tree.TreeItem):
    def __init__(self, unit):
        super(Unit, self).__init__()
        self.unit = unit
 
    def GetValue(self, col):
        if col==0:
            return self.unit.name
        elif col==1:
            return self.unit.symbol
        elif col==2:
            if self.unit.prefixable:
                return "true"
            else:
                return "false"
        return ''
 
#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.unit.id}
#        return None


class TreeManagerUnits(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerUnits, self).__init__(tree_view, *args, **kwargs)

        self.filters = filters
        
        self.AddTextColumn("name")
        self.AddTextColumn("symbol")
        self.AddTextColumn("prefixable")

    def Load(self):
         
        self.SaveState()
        
        filters = self.filters.get_filters()

        for unit in api.data.unit.find(filters):
            unitobj = self.FindUnit(unit)
            if unitobj is None:
                unitobj = self.AppendUnit(unit)
            else:
                unitobj.unit = unit
                self.Update(unitobj)
        
        self.PurgeState()
    
    def FindUnit(self, unit):
        for data in self.data:
            if isinstance(data, Unit) and data.unit.name==unit.name:
                return data
        return None

    def AppendUnit(self, unit):
        unitobj = Unit(unit)
        self.Append(None, unitobj)
        return unitobj

class UnitsFrame(PanelUnits): 
    def __init__(self, parent):
        super(UnitsFrame, self).__init__(parent)

        # units filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create unit list
        self.tree_units_manager = TreeManagerUnits(self.tree_units, context_menu=self.menu_unit, filters=self.Filters)
        self.tree_units_manager.OnSelectionChanged = self.onTreeUnitsSelectionChanged
        self.tree_units_manager.OnItemBeforeContextMenu = self.onTreeUnitsBeforeContextMenu

        # create edit unit panel
        self.panel_edit_unit = frames.edit_unit_frame.EditUnitFrame(self.splitter_vert)
        self.panel_edit_unit.Bind( frames.edit_unit_frame.EVT_EDIT_UNIT_APPLY_EVENT, self.onEditUnitApply )
        self.panel_edit_unit.Bind( frames.edit_unit_frame.EVT_EDIT_UNIT_CANCEL_EVENT, self.onEditUnitCancel )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_unit_list, self.panel_edit_unit)
        self.panel_right.Hide()

    @property
    def Filters(self):
        return self._filters


    def activate(self):
        self.tree_units_manager.Load()

    def _enable(self, value):
        self.panel_unit_list.Enabled = value


    def GetMenus(self):
        return None

    def SetUnit(self, unit):
        self.panel_edit_unit.SetUnit(unit)
        self._enable(True)
        
    def EditUnit(self, unit):
        self.panel_edit_unit.EditUnit(unit)
        self._enable(False)

    def AddUnit(self):
        self.panel_edit_unit.AddUnit()
        self._enable(False)


    def onButtonRefreshUnitsClick( self, event ):
        self.tree_units_manager.Load()
        event.Skip()

    def onFilterChanged( self, event ):
        self.tree_units_manager.Load()
        event.Skip()

    def onTreeUnitsSelectionChanged( self, event ):
        item = self.tree_units.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_units_manager.ItemToObject(item)
        if isinstance(obj, Unit):
            self.panel_edit_unit.SetUnit(obj.unit)
        else:
            self.panel_edit_unit.SetUnit(None)
        event.Skip()

    def onTreeUnitsBeforeContextMenu( self, event ):
        item = self.tree_units.GetSelection()
 
        self.menu_unit_add.Enable(True)
        self.menu_unit_duplicate.Enable(False)
        self.menu_unit_remove.Enable(False)
        self.menu_unit_edit.Enable(False)

        if item.IsOk()==False:
            return 
        obj = self.tree_units_manager.ItemToObject(item)

        if isinstance(obj, Unit):
            self.menu_unit_duplicate.Enable(True)
            self.menu_unit_remove.Enable(True)
            self.menu_unit_edit.Enable(True)

    def onMenuUnitAdd( self, event ):
        self.AddUnit()
        event.Skip()

    def onMenuUnitDuplicate( self, event ):
        # TODO
        event.Skip()

    def onMenuUnitEdit( self, event ):
        item = self.tree_units.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_units_manager.ItemToObject(item)
        if isinstance(obj, Unit)==False:
            return
        self.EditUnit(obj.unit)
        event.Skip()

    def onMenuUnitRemove( self, event ):
        item = self.tree_units.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_units_manager.ItemToObject(item)
         
        associated_parts = api.data.part.find([api.data.part.FilterUnit(obj.unit)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                api.data.unit.delete(obj.unit)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), f"Error removing unit '{obj.unit.name}'", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return
 
            self.tree_units_manager.Load()
 
        dlg.Destroy()
        event.Skip()

    def onEditUnitApply( self, event ):
        self.tree_units_manager.Load()

        unit = event.data
        unitobj = self.tree_units_manager.FindUnit(unit)
        self.tree_units_manager.Select(unitobj)

        self.SetUnit(unit)
        event.Skip()

    def onEditUnitCancel( self, event ):
        self.tree_units_manager.Load()

        item = self.tree_units.GetSelection()
        obj = self.tree_units_manager.ItemToObject(item)
        if isinstance(obj, Unit):
            self.SetUnit(obj.unit)
        else:
            self.SetUnit(None)
        event.Skip()

    def onSearchUnitsCancel( self, event ):
        self._filters.remove_group('search')
        event.Skip()

    def onSearchUnitsEnter( self, event ):
        self._filters.replace(api.data.unit.FilterSearchText(self.search_units.Value), 'search')
        event.Skip()
