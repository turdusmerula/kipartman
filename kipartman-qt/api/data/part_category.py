from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import Qt

from api.treeview import TreeModel, Node, Column
from api.command import CommandUpdateDatabaseField, CommandAddDatabaseObject, commands
from api.events import events
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

class PartCategoryNode(Node):
    def __init__(self, part_category):
        super(PartCategoryNode, self).__init__()
        self.part_category = part_category
        
class PartCategoryModel(TreeModel):
    def __init__(self):
        super(PartCategoryModel, self).__init__()

        self.InsertColumn(Column("Name"))
        self.InsertColumn(Column("Description"))

        self.id_to_part_category = {}
        self.loaded = {
            self.rootNode: False
        }
        self.has_child = {
            self.rootNode: True
        }
        
        events.on_object_update.connect(self.on_object_update)

    def CanFetchMore(self, parent):
        return not self.loaded[parent]

    def Fetch(self, parent):
        nodes = []
        if parent is self.rootNode:
            self.find_childs(parent=None)
        else:
            self.find_childs(parent=parent)
            
    def find_childs(self, parent):
        if parent is None:
            parent_part_category = None
        else:
            parent_part_category = parent.part_category
            
        for part_category in database.data.part_category.find_childs(parent_part_category):
            nodes = []
            if part_category.id not in self.id_to_part_category:
                node = PartCategoryNode(part_category)
                self.id_to_part_category[part_category.id] = node

                # if there is no child then mark category as already loaded
                if part_category.is_leaf_node():
                    self.loaded[node] = True
                    self.has_child[node] = False
                else:
                    self.loaded[node] = False
                    self.has_child[node] = True
                    
                nodes.append(node)
            self.InsertNodes(nodes, parent=parent)

        self.loaded[self.rootNode] = True
        
    def HasChildren(self, parent):
        return self.has_child[parent]

    def GetValue(self, node, column):
        if column==0:
            return node.part_category.name
        elif column==1:
            return node.part_category.description
        
    def SetValue(self, node, column, value):
        field = {
            0: "name",
            1: "description"
        }
        if column in field and getattr(node.part_category, field[column])!=value:
            commands.Do(CommandUpatePartCategory, part_category=node.part_category, field=field[column], value=value)
            return True

        return False

    # def AddPartCategory(self, part_category):
    #     parent_node = None
    #     if part_category.parent is not None:
    #         parent_node = self.id_to_part_category[part_category.parent.id]
    #
    #     node = PartCategoryNode(part_category)
    #     self.loaded[node] = True
    #     self.has_child[node] = False
    #
    #     self.InsertNode(node)

        
    def on_object_update(self, object):
        if isinstance(object, PartCategory)==False:
            return 
        part_category = object
        if part_category.id in self.id_to_part_category:
            self.id_to_part_category[part_category.id].part_category.refresh_from_db()
            self.layoutChanged.emit()

    def on_object_add(self, object):
        pass
    
    def on_object_delete(self, object):
        pass
    
# class PartCategoryModel(TreeModel):
#     def __init__(self):
#         super(PartCategoryModel, self).__init__()
#
#         self.InsertColumn(Column("ID"))
#         self.InsertColumn(Column("Name"))
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
