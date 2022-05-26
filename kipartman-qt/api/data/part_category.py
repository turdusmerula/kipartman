from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, LazyNode, TreeColumn, QTreeViewData
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, CommandDeleteDatabaseObjects, commands
from api.event import events
import database.data.part_category
from database.models import PartCategory

class CommandUpatePartCategory(CommandUpdateDatabaseField):
    def __init__(self, part_category, field, value):
        super(CommandUpatePartCategory, self).__init__(object=part_category, field=field, value=value,
                                            description=f"change part category {field} to '{value}'")

class CommandAddPartCategory(CommandAddDatabaseObject):
    def __init__(self, part_category):
        super(CommandAddPartCategory, self).__init__(object=part_category,
                                            description=f"add new part category")
        
# class CommandDeletePartCategory(CommandDeleteDatabaseObject):
#     def __init__(self, part_category):
#         super(CommandDeletePartCategory, self).__init__(object=part_category,
#                                             description=f"delete part category '{part_category.name}'")

class CommandDeletePartCategories(CommandDeleteDatabaseObjects):
    def __init__(self, part_categories):
        if isinstance(part_categories, list) and len(part_categories)>1:
            objects = part_categories
            description = f"delete {len(part_categories)} part categories"
        elif isinstance(part_categories, list) and len(part_categories)==1:
            objects = part_categories
            description = f"delete part category '{part_categories[0].name}'"
        else:
            objects = [part_categories]
            description = f"delete part category '{part_categories.name}'"
        
        super(CommandDeletePartCategories, self).__init__(objects=objects,
                                            description=description)

class PartCategoryColumn():
    NAME = 0
    DESCRIPTION = 1

class PartCategoryNode(LazyNode):
    def __init__(self, part_category, parent=None):
        super().__init__(parent)
        self.part_category = part_category
        
    def GetValue(self, column):
        if self.part_category is None:
            return None
        
        if column==PartCategoryColumn.NAME:
            return self.part_category.name
        elif column==PartCategoryColumn.DESCRIPTION:
            return self.part_category.description
        return None

    def GetEditValue(self, column):
        return self.GetValue(column)

    def SetValue(self, column, value):
        if self.part_category is None:
            return False

        field = {
            0: "name",
            1: "description"
        }
        if self.part_category.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(self.part_category, field[column], value)
            if self.part_category.name!="":
                # save object in database
                commands.Do(CommandAddPartCategory, part_category=self.part_category)
            return True
        else:
            if column in field and getattr(self.part_category, field[column])!=value:
                commands.Do(CommandUpatePartCategory, part_category=self.part_category, field=field[column], value=value)
                return True

        return False

    def HasChildren(self):
        if len(self.childs)>0:
            return True # only here to treat the case node is not loaded but have an edit node
        elif self.loaded==False and self.part_category is not None:
            return not self.part_category.is_leaf_node()
        else:
            return super().HasChildren()
    
    def Load(self, model):
        super().Load(model)
    
    def __str__(self):
        if self.part_category is None:
            return "[None]"
        return f"[id={self.part_category.id}]"
    
class PartCategoryModel(TreeModel):
    def __init__(self):
        super(PartCategoryModel, self).__init__()

        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Description"))

    def CanFetchMore(self, parent):
        return not parent.loaded

    def Fetch(self, parent):
        self.debug()
        
        if parent is self.rootNode:
            self.find_childs(parent=None)
        else:
            self.find_childs(parent=parent)
            
        self.debug()
        
    def find_childs(self, parent):
        if parent is None:
            parent = self.rootNode
            parent_part_category = None
        else:
            
            parent_part_category = parent.part_category
        
        # prevent recursive Fetch
        parent.loaded = True
    
        self.SaveState(node=parent)

        for part_category in database.data.part_category.find_childs(parent_part_category):
            nodes = []
            node = self.FindPartCategoryNode(part_category)
            if node is None:
                node = PartCategoryNode(part_category)
                nodes.append(node)
            else:
                self.UpdateNode(node)
            self.InsertNodes(nodes, parent=parent)

        # remove remaining nodes
        self.PurgeState()

    def FindPartCategoryNode(self, part_category):
        for node in self.node_to_id:
            if isinstance(node, PartCategoryNode) and node.part_category is not None and node.part_category.id==part_category.id:
                return node
        return None

    def AddPartCategory(self, part_category, pos=None):
        parent_node = None
        if part_category.parent is not None:
            parent_node = self.FindPartCategoryNode(part_category.parent) 
    
        node = PartCategoryNode(part_category)
        self.InsertNode(node, pos=pos, parent=parent_node)

    def CreateEditNode(self, parent):
        if parent==self.rootNode:
            part_category = PartCategory()
        else:
            part_category = PartCategory(parent=parent.part_category)
        return PartCategoryNode(part_category)

    def CreateRootNode(self, parent, *args, **kwargs):
        """ Overload to provide a root node """
        return PartCategoryNode(parent=None, part_category=None)
    

    def Update(self):
        for node in self.node_to_id:
            node.loaded = False
        super().Update()
        
    def Clear(self):
        self.rootNode.loaded = False
        super().Clear()

    # def debug(self):
    #     super(PartCategoryModel, self).debug()
    #     print("loaded / has_child")
    #     for node in self.node_to_id:
    #         print(f"- {node}: ", end="")
    #         if node in self.loaded:
    #             print(f"loaded={self.loaded[node]}\t", end="")
    #         else:
    #             print(f"loaded=None\t", end="")
    #         if node in self.has_child:
    #             print(f"has_child={self.has_child[node]}\t", end="")
    #         else:
    #             print(f"has_child=None\t", end="")
    #         print("")
    #     for node in self.loaded:
    #         if node not in self.node_to_id:
    #             print(f"- {node}: node does not exist")
    #
    #     print("id_to_part_category_node:")
    #     for id in self.id_to_part_category_node:
    #         node = self.id_to_part_category_node[id]
    #         print(f"- {id}: {node} - {node.part_category.name}")


class QPartCategoryTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartCategoryTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

        events.objectUpdated.connect(self.objectChanged)
        events.objectAdded.connect(self.objectChanged)
        events.objectDeleted.connect(self.objectChanged)

    def setModel(self, model):
        super(QPartCategoryTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def objectChanged(self, object):
        if isinstance(object, PartCategory):
            self.model().Update()

    def OnEndInsertEditNode(self, node):
        part_category = node.part_category
        self.setCurrentIndex(self.model().index_from_part_category(part_category))
        
        # add code to select item on redo in this current view only
        commands.LastUndo.done.connect(
            lambda treeView=self, part_category=part_category: 
                self.setCurrentIndex(treeView.model().index_from_part_category(part_category))
        )
    


# class PartCategoryModel(TreeModel):
#     def __init__(self):
#         super(PartCategoryModel, self).__init__()
#
#         self.InsertColumn(TreeColumn("ID"))
#         self.InsertColumn(TreeColumn("Name"))
#
#         self.data = [
#                 [1, "a", []],
#                 [2, "b", []],
#                 [3, "c", [
#                     [4, "ca", []],
#                     [5, "cb", [
#                         [6, "cba", [
#                             [7, "cbaa", []],
#                             [8, "cbab", []],
#                             [9, "cbac", []],
#                         ]],
#                         [10, "cba", []],
#                     ]]
#                 ]]
#             ]
#
#         # self.data = [
#         #         [1, "a", [
#         #             [2, "aa", []]
#         #         ]],
#         #     ]
#
#         self.loaded = False
#
#     def CanFetchMore(self, parent):
#         if self.loaded:
#             return False
#         self.loaded = True
#         return True
#
#     def Fetch(self, parent):
#         print("aaa")
#
#         to_load = []
#         nodes = []
#         for category in self.data:
#             node = PartCategoryNode(category)
#             nodes.append(node)
#             to_load.append(node)
#         self.InsertNodes(nodes)
#
#         while len(to_load)>0:
#             parent = to_load.pop()
#             nodes = []
#             for category in parent.category[2]:
#                 node = PartCategoryNode(category)
#                 nodes.append(node)
#                 to_load.append(node)
#             self.InsertNodes(nodes, parent=parent)
#
#     # def HasChildren(self, parent):
#     #     return False
#     #     return len(node.category[2])>0
#
#     def GetValue(self, node, column):
#         if column==0:
#             return node.category[0]
#         elif column==1:
#             return node.category[1]
