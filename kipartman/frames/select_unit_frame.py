from dialogs.panel_select_unit import PanelSelectUnit
import helper.tree
import wx
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

        return ""


class TreeManagerUnits(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerUnits, self).__init__(tree_view, *args, **kwargs)

        self.AddTextColumn("Name")
        self.AddTextColumn("Symbol")

        self.filters = filters

    def Load(self):
        
        self.SaveState()
        
        for unit in api.data.unit.find(filters=self.filters.get_filters()):
            unitobj = self.FindUnit(unit.id)
            if unitobj is None:
                unitobj = Unit(unit)
                self.Append(None, unitobj)
            else:
                unitobj.unit = unit
                self.Update(unitobj)
        
        self.PurgeState()

    def FindUnit(self, id):
        for data in self.data:
            if isinstance(data, Unit) and data.unit.id==id:
                return data
        return None


class SelectUnitFrame(PanelSelectUnit):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: unit name to select by default
        """
        super(SelectUnitFrame, self).__init__(parent)
        
        # units filters
        self.filters = helper.filter.FilterSet(self)
        self.filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        if initial is not None:
            self.filters.replace(api.data.unit.FilterSearchText(initial), 'search')
            
        # create units list
        self.tree_units_manager = TreeManagerUnits(self.tree_units, filters=self.filters)
        self.tree_units_manager.OnSelectionChanged = self.onTreeUnitsSelectionChanged
        
        if initial:
            self.tree_units.Select(self.tree_units_manager.ObjectToItem(self.tree_units_manager.FindPartUnit(initial)))
        
        # set result functions
        self.cancel = None
        self.result = None

        # initial state
        self.button_select_unitOK.Enabled = False            
        self.tree_units_manager.Clear()

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
        
    def onTreeUnitsSelectionChanged( self, event ):
        item = self.tree_units.GetSelection()
        if item.IsOk():
            self.button_select_unitOK.Enabled = True
        else:
            self.button_select_unitOK.Enabled = False            
        event.Skip()
        
    def onFilterChanged( self, event ):
        self.tree_units_manager.Load()
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        unit = self.tree_units_manager.ItemToObject(self.tree_units.GetSelection())
        if isinstance(unit, Unit) and self.result:
            self.result(unit.unit)

    def onSearchUnitCancel( self, event ):
        self.filters.remove_group('search')

    def onSearchUnitButton( self, event ):
        self.filters.replace(api.data.unit.FilterSearchText(self.search_unit.Value), 'search')
        
    def onSearchUnitEnter( self, event ):
        self.filters.replace(api.data.unit.FilterSearchText(self.search_unit.Value), 'search')
        event.Skip()
