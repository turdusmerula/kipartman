from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtCore import QModelIndex
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeView, QHeaderView, QAbstractItemView

from api.treeview import TreeModel, Node, TreeColumn, QTreeViewData
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

class PartCategoryNode(Node):
    def __init__(self, part_category):
        super(PartCategoryNode, self).__init__()
        self.part_category = part_category
        
class PartCategoryModel(TreeModel):
    def __init__(self):
        super(PartCategoryModel, self).__init__()

        self.InsertColumn(TreeColumn("Name"))
        self.InsertColumn(TreeColumn("Description"))

        self.id_to_part_category_node = {}
        self.loaded = {
            self.rootNode: False
        }
        self.has_child = {
            self.rootNode: True
        }

    def index_from_part_category(self, part_category):
        if part_category.id not in self.id_to_part_category_node:
            return QModelIndex()
        node = self.id_to_part_category_node[part_category.id]
        return self.index_from_node(node)
        
    def part_category_node_from_id(self, id):
        return self.id_to_part_category_node[id]


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
            parent = self.rootNode
            parent_part_category = None
        else:
            parent_part_category = parent.part_category
            
        for part_category in database.data.part_category.find_childs(parent_part_category):
            nodes = []
            if part_category.id not in self.id_to_part_category_node:
                node = PartCategoryNode(part_category)
                self.id_to_part_category_node[part_category.id] = node

                # if there is no child then mark category as already loaded
                if part_category.is_leaf_node():
                    self.loaded[node] = True
                    self.has_child[node] = False
                else:
                    self.loaded[node] = False
                    self.has_child[node] = True
                    
                nodes.append(node)
            self.InsertNodes(nodes, parent=parent)

        self.loaded[parent] = True
        
    def HasChildren(self, parent):
        # new items may not yet be in has_child
        if isinstance(parent, PartCategoryNode) and parent not in self.has_child:
            return False
        return self.has_child[parent]

    def GetValue(self, node, column):
        if column==0:
            return node.part_category.name
        elif column==1:
            return node.part_category.description
        return None

    def SetValue(self, node, column, value):
        field = {
            0: "name",
            1: "description"
        }
        if node.part_category.id is None:
            # item has not yet be commited at this point and have no id
            # set edited field value
            setattr(node.part_category, field[column], value)
            if node.part_category.name!="":
                # save object in database
                commands.Do(CommandAddPartCategory, part_category=node.part_category)
            return True
        else:
            if column in field and getattr(node.part_category, field[column])!=value:
                commands.Do(CommandUpatePartCategory, part_category=node.part_category, field=field[column], value=value)
                return True

        return False

    def AddPartCategory(self, part_category, pos=None):
        parent_node = None
        if part_category.parent is not None:
            parent_node = self.id_to_part_category_node[part_category.parent.id]
    
        node = PartCategoryNode(part_category)
        self.loaded[node] = True
        self.has_child[node] = False
        self.id_to_part_category_node[part_category.id] = node
        
        self.has_child[parent_node] = True

        self.InsertNode(node, pos=pos, parent=parent_node)

    def RemovePartCategoryId(self, id):
        node = self.part_category_node_from_id(id)
        del self.loaded[node]
        del self.has_child[node]
        del self.id_to_part_category_node[id]
        self.RemoveNode(node)

    def RemovePartCategory(self, part_category):
        node = self.part_category_node_from_id(part_category.id)
        del self.loaded[node]
        del self.has_child[node]
        del self.id_to_part_category_node[part_category.id]
        self.RemoveNode(node)

    def CreateEditNode(self, parent):
        self.has_child[parent] = True
        if isinstance(parent, PartCategoryNode):
            part_category = PartCategory(parent=parent.part_category)
        else:
            part_category = PartCategory()
        return PartCategoryNode(part_category)

    def debug(self):
        super(PartCategoryModel, self).debug()
        print("loaded / has_child")
        for node in self.node_to_id:
            print(f"- {node}: ", end="")
            if node in self.loaded:
                print(f"loaded={self.loaded[node]}\t", end="")
            else:
                print(f"loaded=None\t", end="")
            if node in self.has_child:
                print(f"has_child={self.has_child[node]}\t", end="")
            else:
                print(f"has_child=None\t", end="")
            print("")
        for node in self.loaded:
            if node not in self.node_to_id:
                print(f"- {node}: node does not exist")

        print("id_to_part_category_node:")
        for id in self.id_to_part_category_node:
            node = self.id_to_part_category_node[id]
            print(f"- {id}: {node} - {node.part_category.name}")


class QPartCategoryTreeView(QTreeViewData):
    def __init__(self, *args, **kwargs):
        super(QPartCategoryTreeView, self).__init__(*args, **kwargs)
    
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.endInsertEditNode.connect(self.OnEndInsertEditNode)

        events.objectUpdated.connect(self.OnObjectUpdated)
        events.objectAdded.connect(self.OnObjectAdded)
        events.objectDeleted.connect(self.OnObjectDeleted)

    def setModel(self, model):
        super(QPartCategoryTreeView, self).setModel(model)
        
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)        

    def OnObjectUpdated(self, object):
        if isinstance(object, PartCategory)==False:
            return 
        part_category = object
        if part_category.id in self.model().id_to_part_category_node:
            self.model().id_to_part_category_node[part_category.id].part_category.refresh_from_db()
            self.model().layoutChanged.emit()

    def OnObjectAdded(self, object):
        if isinstance(object, PartCategory)==False:
            return 
        part_category = object
        if part_category.id not in self.model().id_to_part_category_node:
            self.model().AddPartCategory(part_category)
            
    def OnObjectDeleted(self, object, id):
        if isinstance(object, PartCategory)==False:
            return 
        part_category = object
        if id in self.model().id_to_part_category_node:
            node = self.model().id_to_part_category_node[id]
            self.model().RemovePartCategoryId(id)

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
