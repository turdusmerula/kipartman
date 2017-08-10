from dialogs.panel_select_footprint import PanelSelectFootprint
import helper.tree
import rest
import wx

class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==0   :
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False
    
class DataModelFootprint(helper.tree.TreeItem):
    def __init__(self, footprint):
        super(DataModelFootprint, self).__init__()
        self.footprint = footprint
            
    def GetValue(self, col):
        vMap = { 
            0 : self.footprint.name,
            1 : self.footprint.description,
        }
        return vMap[col]


class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerFootprints, self).__init__(tree_view)

    def FindFootprint(self, footprint_id):
        for data in self.data:
            if isinstance(data, DataModelFootprint) and data.footprint.id==footprint_id:
                return data
        return None


class SelectFootprintFrame(PanelSelectFootprint):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectFootprintFrame, self).__init__(parent)
        
        # create footprints list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints)
        self.tree_footprints_manager.AddTextColumn("Name")
        self.tree_footprints_manager.AddTextColumn("Description")
        
        self.search_filter = None
        self.search_footprint.Value = ''
        self.load()
        
        if initial:
            self.tree_footprints.Select(self.tree_footprints_manager.ObjectToItem(self.tree_footprints_manager.FindFootprint(initial.id)))
        
        # set result functions
        self.cancel = None
        self.result = None

    def load(self):
        try:
            self.loadFootprints()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def loadFootprints(self):
        # clear all
        self.tree_footprints_manager.ClearItems()
        
        # load parts
        if self.search_filter:
            footprints = rest.api.find_footprints(search=self.search_filter)
        else:
            footprints = rest.api.find_footprints()
            
        # load categories
        categories = {}
        for footprint in footprints:
            if footprint.category:
                category_name = footprint.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(footprint.category)
                self.tree_footprints_manager.AppendItem(None, categories[category_name])
            self.tree_footprints_manager.AppendItem(categories[category_name], DataModelFootprint(footprint))
        
        for category in categories:
            self.tree_footprints_manager.Expand(categories[category])

    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreeFootprintsSelectionChanged( self, event ):
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        footprint = self.tree_footprints_manager.ItemToObject(self.tree_footprints.GetSelection())
        if isinstance(footprint, DataModelFootprint) and self.result:
            self.result(footprint.footprint)

    def onSearchFootprintCancel( self, event ):
        self.search_filter = None
        self.load()
    
    def onSearchFootprintButton( self, event ):
        self.search_filter = self.search_footprint.Value
        self.load()
    
    def onSearchFootprintEnter( self, event ):
        self.search_filter = self.search_footprint.Value
        self.load()
