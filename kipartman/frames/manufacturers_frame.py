from dialogs.panel_manufacturers import PanelManufacturers
import frames.edit_manufacturer_frame
import wx
import helper.tree
from helper.exception import print_stack
import api.data.manufacturer

class Manufacturer(helper.tree.TreeItem):
    def __init__(self, manufacturer):
        super(Manufacturer, self).__init__()
        self.manufacturer = manufacturer
            
    def GetValue(self, col):
        if col==0:
            return self.manufacturer.name

        return ''


class TreeManagerManufacturers(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerManufacturers, self).__init__(tree_view, *args, **kwargs)

        self.filters = filters

        self.AddTextColumn("name")

    def Load(self):
         
        self.SaveState()
        
        filters = self.filters.get_filters()

        for manufacturer in api.data.manufacturer.find(filters):
            manufacturerobj = self.FindManufacturer(manufacturer.id)
            if manufacturerobj is None:
                manufacturerobj = self.AppendManufacturer(manufacturer)
            else:
                manufacturerobj.manufacturer = manufacturer
                self.Update(manufacturerobj)
        
        self.PurgeState()

    def FindManufacturer(self, manufacturer_id):
        for data in self.data:
            if isinstance(data, Manufacturer) and data.manufacturer.id==manufacturer_id:
                return data
        return None

    def AppendManufacturer(self, manufacturer):
        manufacturerobj = Manufacturer(manufacturer)
        self.Append(None, manufacturerobj)
        return manufacturerobj


class ManufacturersFrame(PanelManufacturers): 
    def __init__(self, parent):
        super(ManufacturersFrame, self).__init__(parent)
        
        # manufacturers filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create manufacturers list
        self.tree_manufacturers_manager = TreeManagerManufacturers(self.tree_manufacturers, context_menu=self.menu_manufacturer, filters=self.Filters)
        self.tree_manufacturers_manager.OnSelectionChanged = self.onTreeManufacturersSelectionChanged
        self.tree_manufacturers_manager.OnItemBeforeContextMenu = self.onTreeManufacturersBeforeContextMenu

        # create edit manufacturer panel
        self.panel_edit_manufacturer = frames.edit_manufacturer_frame.EditManufacturerFrame(self.splitter_vert)
        self.panel_edit_manufacturer.Bind( frames.edit_manufacturer_frame.EVT_EDIT_MANUFACTURER_APPLY_EVENT, self.onEditManufacturerApply )
        self.panel_edit_manufacturer.Bind( frames.edit_manufacturer_frame.EVT_EDIT_MANUFACTURER_CANCEL_EVENT, self.onEditManufacturerCancel )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_manufacturer_list, self.panel_edit_manufacturer)
        self.panel_right.Hide()
        
        self.tree_manufacturers_manager.Clear()
        
    @property
    def Filters(self):
        return self._filters


    def activate(self):
        self.tree_manufacturers_manager.Load()

    def _enable(self, value):
        self.panel_manufacturer_list.Enabled = value


    def GetMenus(self):
        return None


    def SetManufacturer(self, manufacturer):
        self.panel_edit_manufacturer.SetManufacturer(manufacturer)
        self._enable(True)
        
    def EditManufacturer(self, manufacturer):
        self.panel_edit_manufacturer.EditManufacturer(manufacturer)
        self._enable(False)

    def AddManufacturer(self):
        self.panel_edit_manufacturer.AddManufacturer()
        self._enable(False)


    def onButtonRefreshManufacturersClick( self, event ):
        self.tree_manufacturers_manager.Load()
        event.Skip()

    def onFilterChanged( self, event ):
        self.tree_manufacturers_manager.Load()
        event.Skip()

    def onTreeManufacturersSelectionChanged( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_manufacturers_manager.ItemToObject(item)
        if isinstance(obj, Manufacturer):
            self.panel_edit_manufacturer.SetManufacturer(obj.manufacturer)
        else:
            self.panel_edit_manufacturer.SetManufacturer(None)
        event.Skip()

    def onTreeManufacturersBeforeContextMenu( self, event ):
        item = self.tree_manufacturers.GetSelection()
 
        self.menu_manufacturer_add.Enable(True)
        self.menu_manufacturer_duplicate.Enable(False)
        self.menu_manufacturer_remove.Enable(False)
        self.menu_manufacturer_edit.Enable(False)

        if item.IsOk()==False:
            return 
        obj = self.tree_manufacturers_manager.ItemToObject(item)

        if isinstance(obj, Manufacturer):
            self.menu_manufacturer_duplicate.Enable(True)
            self.menu_manufacturer_remove.Enable(True)
            self.menu_manufacturer_edit.Enable(True)

    def onMenuManufacturerAdd( self, event ):
        self.AddManufacturer()
        event.Skip()

    def onMenuManufacturerDuplicate( self, event ):
        # TODO
        event.Skip()

    def onMenuManufacturerEdit( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_manufacturers_manager.ItemToObject(item)
        if isinstance(obj, Manufacturer)==False:
            return
        self.EditManufacturer(obj.manufacturer)
        event.Skip()

    def onMenuManufacturerRemove( self, event ):
        item = self.tree_manufacturers.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_manufacturers_manager.ItemToObject(item)
         
        associated_parts = api.data.part.find([api.data.part.FilterManufacturer(obj.manufacturer)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                api.data.manufacturer.delete(obj.manufacturer)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), f"Error removing manufacturer '{obj.manufacturer.name}'", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return
 
            self.tree_manufacturers_manager.Load()
 
        dlg.Destroy()
        event.Skip()

    def onEditManufacturerApply( self, event ):
        self.tree_manufacturers_manager.Load()

        manufacturer = event.data
        manufacturerobj = self.tree_manufacturers_manager.FindManufacturer(manufacturer.id)
        self.tree_manufacturers_manager.Select(manufacturerobj)

        self.SetManufacturer(manufacturer)
        event.Skip()

    def onEditManufacturerCancel( self, event ):
        self.tree_manufacturers_manager.Load()

        item = self.tree_manufacturers.GetSelection()
        obj = self.tree_manufacturers_manager.ItemToObject(item)
        if isinstance(obj, Manufacturer):
            self.SetManufacturer(obj.manufacturer)
        else:
            self.SetManufacturer(None)
        event.Skip()

    def onSearchManufacturersCancel( self, event ):
        self._filters.remove_group('search')
        event.Skip()

    def onSearchManufacturersButton( self, event ):
        self._filters.replace(api.data.manufacturer.FilterSearchText(self.search_manufacturers.Value), 'search')
        event.Skip()

    def onSearchManufacturersTextEnter( self, event ):
        self._filters.replace(api.data.manufacturer.FilterSearchText(self.search_manufacturers.Value), 'search')
        event.Skip()

