from dialogs.panel_select_footprint import PanelSelectFootprint
import wx
import wx.dataview

class FootPrintCategoryList(object):
    def __init__(self):
        self.data = FootprintCategoriesQuery().get()
        
        # build a path to category dictionnary
        self.dict = {}
        for category in self.data:
            self.dict[category.path] = category

    def get_path(self, category):
        if not category:
            return "/"
        path = "/"+category.name
        print category.parent._url
        return ""
        parent = self.dict[category.parent._url]
        while parent:
            path = "/"+parent.name+path
            parent = self.dict[parent.parent._url]
        return path

class FootprintDataModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(FootprintDataModel, self).__init__()
        self.data = FootprintsQuery().get()

    def Filter(self, footprint_filter=None):
        if footprint_filter:
            self.data = FootprintsQuery(**footprint_filter).get()
        
    def GetColumnCount(self):
        return 1

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            children.append(self.ObjectToItem(None))
            for footprint in self.data:
                children.append(self.ObjectToItem(footprint))
            return len(self.data)+1
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        if obj:
            vMap = { 
                0 : obj.name,
            }
        else:
            vMap = { 
                0 : "<none>",
            }
            
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False

    def FootprintToItem(self, footprint):
        if not footprint:
            return self.ObjectToItem(footprint)
        for f in self.data:
            if f and f.id==footprint.id:
                return self.ObjectToItem(f)
            
class SelectFootprintFrame(PanelSelectFootprint):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectFootprintFrame, self).__init__(parent)
    
        # create footprints list
        self.footprints_model = FootprintDataModel()
        self.tree_footprints.AssociateModel(self.footprints_model)
        # add default columns
        self.tree_footprints.AppendTextColumn("name", 0, width=wx.COL_WIDTH_AUTOSIZE)
        
        self.tree_footprints.Select(self.footprints_model.FootprintToItem(initial))
        
        # set result functions
        self.cancel = None
        self.result = None
    
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
        footprint = self.footprints_model.ItemToObject(self.tree_footprints.GetSelection())
        if self.result:
            self.result(footprint)