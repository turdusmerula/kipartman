from dialogs.panel_parameters import PanelParameters
import frames.edit_parameter_frame
from frames.merge_parameters_dialog import MergeParametersDialog, EVT_SELECT_PARAMETER_OK_EVENT
import wx
import helper.filter
from helper.exception import print_stack
import api.data.parameter
import api.data.part

class Parameter(helper.tree.TreeItem):
    def __init__(self, parameter):
        super(Parameter, self).__init__()
        self.parameter = parameter
 
    def GetValue(self, col):
        if col==0:
            return self.parameter.name
        elif col==1:
            return self.parameter.description
        elif col==2:
            return self.parameter.value_type
        elif col==3:
            if self.parameter.unit is not None:
                return self.parameter.unit.name
        return ''
 
#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.parameter.id}
#        return None


class TreeManagerParameters(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, filters, **kwargs):
        super(TreeManagerParameters, self).__init__(tree_view, *args, **kwargs)

        self.filters = filters
        
        self.AddTextColumn("name")
        self.AddTextColumn("description")
        self.AddTextColumn("type")
        self.AddTextColumn("unit")

    def Load(self):
         
        self.SaveState()
        
        filters = self.filters.get_filters()

        for parameter in api.data.parameter.find(filters):
            parameterobj = self.FindParameter(parameter)
            if parameterobj is None:
                parameterobj = self.AppendParameter(parameter)
            else:
                parameterobj.parameter = parameter
                self.Update(parameterobj)
        
        self.PurgeState()
    
    def FindParameter(self, parameter):
        for data in self.data:
            if isinstance(data, Parameter) and data.parameter.name==parameter.name:
                return data
        return None

    def AppendParameter(self, parameter):
        parameterobj = Parameter(parameter)
        self.Append(None, parameterobj)
        return parameterobj

class ParametersFrame(PanelParameters): 
    def __init__(self, parent):
        super(ParametersFrame, self).__init__(parent)

        # parameters filters
        self._filters = helper.filter.FilterSet(self, self.toolbar_filters)
        self.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )

        # create parameter list
        self.tree_parameters_manager = TreeManagerParameters(self.tree_parameters, context_menu=self.menu_parameter, filters=self.Filters)
        self.tree_parameters_manager.OnSelectionChanged = self.onTreeParametersSelectionChanged
        self.tree_parameters_manager.OnItemBeforeContextMenu = self.onTreeParametersBeforeContextMenu

        # create edit parameter panel
        self.panel_edit_parameter = frames.edit_parameter_frame.EditParameterFrame(self.splitter_vert)
        self.panel_edit_parameter.Bind( frames.edit_parameter_frame.EVT_EDIT_PARAMETER_APPLY_EVENT, self.onEditParameterApply )
        self.panel_edit_parameter.Bind( frames.edit_parameter_frame.EVT_EDIT_PARAMETER_CANCEL_EVENT, self.onEditParameterCancel )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_parameter_list, self.panel_edit_parameter)
        self.panel_right.Hide()

        self.tree_parameters_manager.Clear()
        
    @property
    def Filters(self):
        return self._filters


    def activate(self):
        self.tree_parameters_manager.Load()

    def _enable(self, value):
        self.panel_parameter_list.Enabled = value


    def GetMenus(self):
        return None

    def SetParameter(self, parameter):
        self.panel_edit_parameter.SetParameter(parameter)
        self._enable(True)
        
    def EditParameter(self, parameter):
        self.panel_edit_parameter.EditParameter(parameter)
        self._enable(False)

    def AddParameter(self):
        self.panel_edit_parameter.AddParameter()
        self._enable(False)


    def onButtonRefreshParametersClick( self, event ):
        self.tree_parameters_manager.Load()
        event.Skip()

    def onFilterChanged( self, event ):
        self.tree_parameters_manager.Load()
        event.Skip()

    def onTreeParametersSelectionChanged( self, event ):
        items = self.tree_parameters.GetSelections()
        if len(items)==1:
            item = items[0]
            if item.IsOk()==False:
                return
            obj = self.tree_parameters_manager.ItemToObject(item)
            if isinstance(obj, Parameter):
                self.panel_edit_parameter.SetParameter(obj.parameter)
            else:
                self.panel_edit_parameter.SetParameter(None)
        else:
            self.panel_edit_parameter.SetParameter(None)
            
        event.Skip()

    def onTreeParametersBeforeContextMenu( self, event ):
        items = self.tree_parameters.GetSelections()
 
        self.menu_parameter_add.Enable(True)
        self.menu_parameter_duplicate.Enable(False)
        self.menu_parameter_remove.Enable(False)
        self.menu_parameter_edit.Enable(False)
        self.menu_parameter_merge.Enable(False)

        if len(items)==1:
            item = items[0]
            if item.IsOk()==False:
                return 
            obj = self.tree_parameters_manager.ItemToObject(item)
    
            if isinstance(obj, Parameter):
                self.menu_parameter_duplicate.Enable(True)
                self.menu_parameter_remove.Enable(True)
                self.menu_parameter_edit.Enable(True)
        elif len(items)>1:
            self.menu_parameter_remove.Enable(True)
            self.menu_parameter_merge.Enable(True)
            
    def onMenuParameterAdd( self, event ):
        self.AddParameter()
        event.Skip()

    def onMenuParameterDuplicate( self, event ):
        # TODO
        event.Skip()

    def onMenuParameterEdit( self, event ):
        item = self.tree_parameters.GetSelection()
        if not item.IsOk():
            return
        obj = self.tree_parameters_manager.ItemToObject(item)
        if isinstance(obj, Parameter)==False:
            return
        self.EditParameter(obj.parameter)
        event.Skip()

    def onMenuParameterRemove( self, event ):
        items = self.tree_parameters.GetSelections()
        for item in items:
            if item.IsOk()==False:
                return
            obj = self.tree_parameters_manager.ItemToObject(item)
             
            associated_parts = api.data.part.find([api.data.part.FilterParameter(obj.parameter)])
            if len(associated_parts.all())>0:
                dlg = wx.MessageDialog(self, f"There is {len(associated_parts.all())} parts associated with parameter '{obj.parameter.name}', remove anyway?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
            else:
                dlg = wx.MessageDialog(self, f"Remove selection?", 'Remove', wx.YES_NO | wx.ICON_EXCLAMATION)
            if dlg.ShowModal()==wx.ID_YES:
                try:
                    api.data.parameter.delete(obj.parameter)
                except Exception as e:
                    print_stack()
                    wx.MessageBox(format(e), f"Error removing parameter '{obj.parameter.name}'", wx.OK | wx.ICON_ERROR)
                    dlg.Destroy()
                    return
 
        self.tree_parameters_manager.Load()
 
        dlg.Destroy()
        event.Skip()

    def onMenuParameterMerge( self, event ):
        items = self.tree_parameters.GetSelections()
        parameters = []
        for item in items:
            obj = self.tree_parameters_manager.ItemToObject(item)
            parameters.append(obj.parameter)
        merge_dialog = MergeParametersDialog(self, parameters)
        merge_dialog.Bind( EVT_SELECT_PARAMETER_OK_EVENT, self.onMergeParameterCallback )
        merge_dialog.ShowModal()
        
        event.Skip()
    
    def onMergeParameterCallback(self, event):
        items = self.tree_parameters.GetSelections()
        parameters = []
        merge_parameter = event.data
        for item in items:
            obj = self.tree_parameters_manager.ItemToObject(item)
            if obj.parameter.name!=merge_parameter.name:
                parameters.append(obj.parameter)
        
        for parameter in parameters:
            # merge part_parameters
            associated_part_parameters = api.data.part_parameter.find([api.data.part_parameter.FilterParameter(parameter)])
            for part_parameter in associated_part_parameters.all():
                part_parameter.parameter = merge_parameter
                part_parameter.save()
            # add merged parameter as alias
            parameter_alias = api.data.parameter_alias.create()
            parameter_alias.name = parameter.name
            merge_parameter.alias.add_pending(parameter_alias)
            # remove merged parameters
            parameter.delete()
        merge_parameter.save()
        
        self.tree_parameters_manager.Load()

    def onEditParameterApply( self, event ):
        self.tree_parameters_manager.Load()

        parameter = event.data
        parameterobj = self.tree_parameters_manager.FindParameter(parameter)
        self.tree_parameters_manager.Select(parameterobj)

        self.SetParameter(parameter)
        event.Skip()

    def onEditParameterCancel( self, event ):
        self.tree_parameters_manager.Load()

        item = self.tree_parameters.GetSelection()
        obj = self.tree_parameters_manager.ItemToObject(item)
        if isinstance(obj, Parameter):
            self.SetParameter(obj.parameter)
        else:
            self.SetParameter(None)
        event.Skip()

    def onSearchParametersCancel( self, event ):
        self._filters.remove_group('search')
        event.Skip()

    def onSearchParametersButton( self, event ):
        self._filters.replace(api.data.parameter.FilterSearchText(self.search_parameters.Value), 'search')
        event.Skip()

    def onSearchParametersTextEnter( self, event ):
        self._filters.replace(api.data.parameter.FilterSearchText(self.search_parameters.Value), 'search')
        event.Skip()
