import helper.tree
import api.data.part
import os


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
            if self.part.symbol:
                return self.part.symbol.name
        elif col==5:
            if self.part.footprint:
                return self.part.footprint.name

        return ""

    def Load(self, manager):
        if self.part.metapart==True:
            for child in api.data.part.find_metapart_childs(self.part):
                partobj = self.FindPartChild(child.id)
                if partobj is None:
                    manager.Append(self, Part(child))
                else:
                    partobj.part = child
                    manager.Update(partobj)
                
#         for child in api.data.part.find([api.data.part.FilterChilds(self.part)]):
#             partobj = self.FindPartChild(child.id)
#             if partobj is None:
#                 manager.Append(self, Part(child))
#             else:
#                 partobj.part = child
#                 manager.Update(partobj)
        pass
    
    def HasChilds(self):
#         if self.part.child_count>0:
#             return True
        if self.part.metapart==True:
            return True
        return False
    
    def FindPartChild(self, partid):
        for child in self.childs:
            if isinstance(child, Part) and child.part.id==partid:
                return child
        return None
            
class TreeManagerParts(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, filters, **kwargs):
        model = TreeModelPart()
        super(TreeManagerParts, self).__init__(tree_view, model, *args, **kwargs)

        self.filters = filters
        
        self.flat = False

        self.AddIntegerColumn("id")
        self.AddTextColumn("name")
        self.AddTextColumn("description")
        self.AddIntegerColumn("comment")
        self.AddTextColumn("symbol")
        self.AddTextColumn("footprint")

    def Load(self):
        
        self.SaveState()
        
        if self.flat:
            self.LoadFlat()
        else:
            self.LoadTree()
        
        self.PurgeState()


    def LoadFlat(self):
        for part in api.data.part.find(filters=self.filters.get_filters()):
            partobj = self.FindPart(part.id)
            if partobj is None:
                partobj = Part(part)
                self.Append(None, partobj)
            else:
                partobj.part = part
                self.Update(partobj)
            
    def LoadTree(self):
        for part in api.data.part.find(filters=self.filters.get_filters()):
            partobj = self.FindPart(part.id)
            
            if part.category is not None:
                categoryobj = self.FindCategory(part.category.id)
                 
                if categoryobj is None:
                    categoryobj = PartCategory(part.category)
                    self.Append(None, categoryobj)
                else:
                    categoryobj.category = part.category
                    self.Update(categoryobj)
            else:
                categoryobj = None
                
            if partobj is None:
                partobj = Part(part)
                self.Append(categoryobj, partobj)
            else:
                partobj.part = part
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
    def __init__(self):
        super(TreeModelPart, self).__init__()
