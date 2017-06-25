from dialogs.panel_select_part import PanelSelectPart
from api.queries import PartsQuery, PartCategoriesQuery
import wx
import wx.lib.newevent
import wx.dataview

SelectPartOkEvent, EVT_SELECT_PART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectPartCancelEvent, EVT_SELECT_PART_APPLY_EVENT = wx.lib.newevent.NewEvent()

class PartCategoryList(object):
    def __init__(self):
        self.data = PartCategoriesQuery().get()
        
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

class PartDataModel(wx.dataview.PyDataViewModel):
    def __init__(self):
        super(PartDataModel, self).__init__()
        self.data = PartsQuery().get()
        #self.UseWeakRefs(True)
    
    def Filter(self, part_filter=None):
        if part_filter:
            self.data = PartsQuery(**part_filter).get()
        
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
            for part in self.data:
                # mark root parts to avoid recursion
                part.parent = None
                children.append(self.ObjectToItem(part))
            return len(self.data)
        
        # load childrens
        parent_part = self.ItemToObject(parent)
        for id in parent_part.parts:
            subpart = PartsQuery().get(id)[0]
            subpart.parent = parent_part
            print "subpart", subpart.id
            children.append(self.ObjectToItem(subpart))
        return len(parent_part.parts)
    
    def IsContainer(self, item):
        if not item:
            return True
        part = self.ItemToObject(item)
        return len(part.parts)>0

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        if not item:
            return wx.dataview.NullDataViewItem

        part = self.ItemToObject(item)
        if not part.parent:
            return wx.dataview.NullDataViewItem
        else:
            return self.ObjectToItem(part.parent)
    
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
            
class SelectPartFrame(PanelSelectPart):
    def __init__(self, parent, initial=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectPartFrame, self).__init__(parent)
    
        # create parts list
        self.parts_model = PartDataModel()
        self.tree_parts.AssociateModel(self.parts_model)
        # add default columns
        self.tree_parts.AppendTextColumn("id", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parts.AppendTextColumn("name", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parts.AppendTextColumn("description", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_parts.AppendTextColumn("comment", 3, width=wx.COL_WIDTH_AUTOSIZE)
        
#        self.tree_parts.Select(self.parts_model.PartToItem(initial))
        
        # set result functions
        self.cancel = None
        self.result = None
    
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
        
    # Virtual event handlers, overide them in your derived class
    def onTreePartsSelectionChanged( self, event ):
        event.Skip()
    
    def onButtonCancelClick( self, event ):
        event = SelectPartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        sel = self.tree_parts.GetSelection()
        if not sel:
            return
        part = self.parts_model.ItemToObject(self.tree_parts.GetSelection())
        
        # trigger result event
        event = SelectPartOkEvent(data=part)
        wx.PostEvent(self, event)
        if self.result:
            self.result(part)
            