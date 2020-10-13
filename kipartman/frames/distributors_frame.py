from dialogs.panel_distributors import PanelDistributors
import frames.edit_distributor_frame
import wx
import helper.tree
from helper.exception import print_stack
import api.data.distributor
import api.data.part_offer

class Distributor(helper.tree.TreeItem):
    def __init__(self, distributor):
        super(Distributor, self).__init__()
        self.distributor = distributor
            
    def GetValue(self, col):
        if col==0:
            return self.distributor.allowed
        elif col==1:
            return self.distributor.name

        return ''

    def SetValue(self, value, col):
        if col==0:
            self.distributor.allowed = value
            self.distributor.save()
            return True
        return False

class TreeManagerDistributors(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerDistributors, self).__init__(tree_view, *args, **kwargs)

        self.filters = filters

        self.AddToggleColumn("Allowed")
        self.AddTextColumn("Name")

    def Load(self):
         
        self.SaveState()
        
        filters = self.filters.get_filters()

        for distributor in api.data.distributor.find(filters):
            distributorobj = self.FindDistributor(distributor.id)
            if distributorobj is None:
                distributorobj = self.AppendDistributor(distributor)
            else:
                distributorobj.distributor = distributor
                self.Update(distributorobj)
        
        self.PurgeState()

    def FindDistributor(self, distributor_id):
        for data in self.data:
            if isinstance(data, Distributor) and data.distributor.id==distributor_id:
                return data
        return None

    def AppendDistributor(self, distributor):
        distributorobj = Distributor(distributor)
        self.Append(None, distributorobj)
        return distributorobj

class DistributorsFrame(PanelDistributors): 
    def __init__(self, parent):
        super(DistributorsFrame, self).__init__(parent)
        
        # distributors filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create distributors list
        self.tree_distributors_manager = TreeManagerDistributors(self.tree_distributors, context_menu=self.menu_distributor, filters=self.Filters)
        self.tree_distributors_manager.OnSelectionChanged = self.onTreeDistributorsSelectionChanged
        self.tree_distributors_manager.OnItemBeforeContextMenu = self.onTreeDistributorsBeforeContextMenu

        # create edit distributor panel
        self.panel_edit_distributor = frames.edit_distributor_frame.EditDistributorFrame(self.splitter_vert)
        self.panel_edit_distributor.Bind( frames.edit_distributor_frame.EVT_EDIT_DISTRIBUTOR_APPLY_EVENT, self.onEditDistributorApply )
        self.panel_edit_distributor.Bind( frames.edit_distributor_frame.EVT_EDIT_DISTRIBUTOR_CANCEL_EVENT, self.onEditDistributorCancel )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_distributor_list, self.panel_edit_distributor)
        self.panel_right.Hide()
        
        self.tree_distributors_manager.Clear()
        
    @property
    def Filters(self):
        return self._filters


    def activate(self):
        self.tree_distributors_manager.Load()

    def _enable(self, value):
        self.panel_distributor_list.Enabled = value


    def GetMenus(self):
        return None


    def SetDistributor(self, distributor):
        self.panel_edit_distributor.SetDistributor(distributor)
        self._enable(True)
        
    def EditDistributor(self, distributor):
        self.panel_edit_distributor.EditDistributor(distributor)
        self._enable(False)

    def AddDistributor(self):
        self.panel_edit_distributor.AddDistributor()
        self._enable(False)


    def onButtonRefreshDistributorsClick( self, event ):
        self.tree_distributors_manager.Load()
        event.Skip()

    def onFilterChanged( self, event ):
        self.tree_distributors_manager.Load()
        event.Skip()

    def onTreeDistributorsSelectionChanged( self, event ):
        item = self.tree_distributors.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(obj, Distributor):
            self.panel_edit_distributor.SetDistributor(obj.distributor)
        else:
            self.panel_edit_distributor.SetDistributor(None)
        event.Skip()

    def onTreeDistributorsBeforeContextMenu( self, event ):
        item = self.tree_distributors.GetSelection()
 
        self.menu_distributor_add.Enable(True)
        self.menu_distributor_duplicate.Enable(False)
        self.menu_distributor_remove.Enable(False)
        self.menu_distributor_edit.Enable(False)

        if item.IsOk()==False:
            return 
        obj = self.tree_distributors_manager.ItemToObject(item)

        if isinstance(obj, Distributor):
            self.menu_distributor_duplicate.Enable(True)
            self.menu_distributor_remove.Enable(True)
            self.menu_distributor_edit.Enable(True)

    def onMenuDistributorAdd( self, event ):
        self.AddDistributor()
        event.Skip()

    def onMenuDistributorDuplicate( self, event ):
        # TODO
        event.Skip()

    def onMenuDistributorEdit( self, event ):
        item = self.tree_distributors.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(obj, Distributor)==False:
            return
        self.EditDistributor(obj.distributor)
        event.Skip()

    def onMenuDistributorRemove( self, event ):
        item = self.tree_distributors.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_distributors_manager.ItemToObject(item)
         
        associated_parts = api.data.part.find([api.data.part.FilterDistributor(obj.distributor)])
        if len(associated_parts.all())>0:
            dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with selection, remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        else:
            dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_YES:
            try:
                api.data.distributor.delete(obj.distributor)
            except Exception as e:
                print_stack()
                wx.MessageBox(format(e), f"Error removing distributor '{obj.distributor.name}'", wx.OK | wx.ICON_ERROR)
                dlg.Destroy()
                return
 
            self.tree_distributors_manager.Load()
 
        dlg.Destroy()
        event.Skip()

    def onEditDistributorApply( self, event ):
        self.tree_distributors_manager.Load()

        distributor = event.data
        distributorobj = self.tree_distributors_manager.FindDistributor(distributor.id)
        self.tree_distributors_manager.Select(distributorobj)

        self.SetDistributor(distributor)
        event.Skip()

    def onEditDistributorCancel( self, event ):
        self.tree_distributors_manager.Load()

        item = self.tree_distributors.GetSelection()
        obj = self.tree_distributors_manager.ItemToObject(item)
        if isinstance(obj, Distributor):
            self.SetDistributor(obj.distributor)
        else:
            self.SetDistributor(None)
        event.Skip()

    def onSearchDistributorsCancel( self, event ):
        self._filters.remove_group('search')
        event.Skip()

    def onSearchDistributorsButton( self, event ):
        self._filters.replace(api.data.distributor.FilterSearchText(self.search_distributors.Value), 'search')
        event.Skip()

    def onSearchDistributorsTextEnter( self, event ):
        self._filters.replace(api.data.distributor.FilterSearchText(self.search_distributors.Value), 'search')
        event.Skip()

