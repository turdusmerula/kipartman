from dialogs.panel_part_list import PanelPartList
from api.data import part as data_part
from api.data import part_category as data_part_category
import api.models
import helper.tree
import helper.filter
from helper.log import log
from helper.profiler import Trace
import os
import wx

class PartCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(PartCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        if col==0:
            return self.category.id
        elif col==1:
            return self.category.path

        return ""

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
        return True

    def IsEnabled(self, col):
        return False

class Part(helper.tree.TreeContainerLazyItem):
    def __init__(self, part):
        self.part = part
        
        super(Part, self).__init__()
        
    def GetValue(self, col):
        if col==0:
            return self.part.id
        elif col==1:
            return self.part.name
        elif col==2:
            return self.part.description
        elif col==3:
            return self.part.comment
        elif col==4:
            symbol = ""
            if self.part.symbol:
                symbol = os.path.basename(self.part.symbol.source_path).replace('.mod', '')
            return symbol
        elif col==5:
            footprint = ""
            if self.part.footprint:
                footprint = os.path.basename(self.part.footprint.source_path).replace('.kicad_mod', '')
            return footprint

        return ""

    def Load(self):
        for child in data_part.find([data_part.FilterChilds(self.part)]):
            self.AddChild(Part(child))
    
    def IsContainer(self):
        if self.part.child_count>0:
            return True
        return False
    
class TreeManagerParts(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, filters, **kwargs):
        model = TreeModelPart()
        super(TreeManagerParts, self).__init__(tree_view, model, *args, **kwargs)

        self.filters = filters
        
        self.flat = False
        self.categories = []
        self.parts = []  # flat part list

        self.id_to_category = {}
        self.id_to_part = {}

    def Load(self):
        
        self.SaveState()
        
        if self.flat:
            self.LoadFlat()
        else:
            self.LoadTree()
        
        self.PurgeState()


    def LoadFlat(self):
        for part in data_part.find(filters=self.filters.get_filters()):
            partobj = self.FindPart(part.id)
            if partobj is None:
                partobj = Part(part)
                self.Append(None, partobj)
            else:
                self.Update(partobj)
            
    def LoadTree(self):
        for part in data_part.find(filters=self.filters.get_filters()):
            partobj = self.FindPart(part.id)
            categoryobj = self.FindCategory(part.category.id)
             
            if categoryobj is None:
                categoryobj = PartCategory(part.category)
                self.Append(None, categoryobj)
            else:
                self.Update(categoryobj)
 
            if partobj is None:
                partobj = Part(part)
                self.Append(categoryobj, partobj)
            else:
                self.Update(partobj)
    
    def FindPart(self, id):
        for data in self.data:
            if isinstance(data, Part) and ( isinstance(data.parent, PartCategory) or data.parent is None ) and data.part.id==id:
                return data
        return None
    
    def FindCategory(self, id):
        for data in self.data:
            if isinstance(data, PartCategory) and data.category.id==id:
                return data
        return None

    def FindCategories(self,):
        res = []
        for data in self.data:
            if isinstance(data, PartCategory):
                res.append(data)
        return res

class TreeModelPart(helper.tree.TreeModel):
    def __init__(self, flat=False):
        super(TreeModelPart, self).__init__()

(SelectPartEvent, EVT_SELECT_PART) = wx.lib.newevent.NewEvent()

class PartListFrame(PanelPartList): 
    def __init__(self, *args, filters, **kwargs): 
        super(PartListFrame, self).__init__(*args, **kwargs)

        self.filters = filters
        self.filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFilterChanged )
        
        # create part list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts, context_menu=self.menu_part, filters=self.filters)
        self.tree_parts_manager.AddIntegerColumn("id")
        self.tree_parts_manager.AddTextColumn("name")
        self.tree_parts_manager.AddTextColumn("description")
        self.tree_parts_manager.AddIntegerColumn("comment")
        self.tree_parts_manager.AddTextColumn("symbol")
        self.tree_parts_manager.AddTextColumn("footprint")
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged

        self.toolbar_part.ToggleTool(self.toggle_part_path.GetId(), True)
        self.flat = False
    
    @property
    def flat(self):
        return self.tree_parts_manager.flat
    
    @flat.setter
    def flat(self, value):
        self.tree_parts_manager.flat = value
        self.tree_parts_manager.Clear()
        self.tree_parts_manager.Load()
        self.expand_categories()
        
    def activate(self):
        pass

    def expand_categories(self):
        if self.flat==False:
            for category in self.tree_parts_manager.FindCategories():
                self.tree_parts_manager.Expand(category)


    def onToggleCategoryPathClicked( self, event ):
        self.flat = not self.toolbar_part.GetToolState(self.toggle_part_path.GetId())
        event.Skip()

    def onButtonRefreshPartsClick( self, event ):
        self.tree_parts_manager.Load()
        event.Skip()
        
    def onFilterChanged( self, event ):
        self.tree_parts_manager.Load()
        self.expand_categories()
        event.Skip()

    def onTreePartsSelChanged( self, event ):
        item = self.tree_parts.GetSelection()
        if item.IsOk()==False:
            return
        obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, Part)==False:
            return
        wx.PostEvent(self, SelectPartEvent(part=obj.part))
        event.Skip()
