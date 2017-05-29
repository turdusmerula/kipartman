from dialogs.panel_select_footprint import PanelSelectFootprint
from api.queries import FootprintsQuery, FootprintCategoriesQuery
import wx
import wx.dataview

class FootprintDataModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(FootprintDataModel, self).__init__()
        self.data = FootprintsQuery().get()
    
    def Filter(self, footprint_filter=None):
        if footprint_filter:
            self.data = FootprintsQuery(**footprint_filter).get()
        
    def GetColumnCount(self):
        return 4

    def GetColumnType(self, col):
        mapper = { 
            0 : 'long',
            1 : 'string',
            2 : 'string',
            3 : 'string'
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for footprint in self.data:
                children.append(self.ObjectToItem(footprint))
            return len(self.data)
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : str(obj.id),
            1 : obj.name,
            2 : obj.description,
            3 : obj.comment
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        if col == 0:
            attr.Bold = True
            return True
        return False

class SelectFootprintFrame(PanelSelectFootprint):
    def __init__(self, parent): 
        super(SelectFootprintFrame, self).__init__(parent)
    