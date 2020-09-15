from dialogs.panel_select_part import PanelSelectPart
import wx
import wx.lib.newevent
import wx.dataview
from frames.part_list_frame import PartCategory, Part, TreeManagerParts
from frames.part_parameters_frame import PartParameter, TreeManagerPartParameter
import helper.tree

SelectPartOkEvent, EVT_SELECT_PART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectPartCancelEvent, EVT_SELECT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()

            
class SelectPartFrame(PanelSelectPart):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectPartFrame, self).__init__(parent)
    
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
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelectionChanged

        # create parameters list
        self.tree_parameters_manager = TreeManagerPartParameter(self.tree_parameters, context_menu=self.menu_parameter)
        self.tree_parameters_manager.AddToggleColumn("*")
        self.tree_parameters_manager.AddTextColumn("Parameter")
        self.tree_parameters_manager.AddTextColumn("Value")
        self.tree_parameters_manager.AddTextColumn("Min")
        self.tree_parameters_manager.AddTextColumn("Max")
        self.tree_parameters_manager.AddTextColumn("Unit")
        self.tree_parameters_manager.AddTextColumn("Description")

        # set result functions
        self.cancel = None
        self.result = None
        
        # initial state
        self.button_part_selectOK.Enabled = False            

        self.tree_parts_manager.Clear()
        self.tree_parameters_manager.Load()
        
        self.tree_parameters_manager.Clear()


    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    def onTreePartsSelectionChanged( self, event ):
        item = self.tree_parts.GetSelection()
        if item.IsOk()==False:
            return
        partobj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(partobj, Part)==False:
            self.button_part_selectOK.Enabled = False
            return
        
        self.button_part_selectOK.Enabled = True
#         partobj.part = rest.api.find_part(partobj.part.id, with_parameters=True)
#         self.showParameters(partobj.part)
        
    def onButtonCancelClick( self, event ):
        event = SelectPartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        item = self.tree_parts.GetSelection()
        if item.IsOk()==False:
            return
        partobj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(partobj, DataModelPart)==False:
            return
        
        # trigger result event
        event = SelectPartOkEvent(data=partobj.part)
        wx.PostEvent(self, event)
        if self.result:
            self.result(partobj.part)

    def onSearchPartCancelButton( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchPartSearchButton( self, event ):
        self.search_filter = self.search_part.Value
        self.load()
    
    def onSearchPartTextEnter( self, event ):
        self.search_filter = self.search_part.Value
        self.load()
