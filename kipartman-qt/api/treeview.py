from PyQt6.QtCore import Qt, QObject, pyqtSignal, QSize, QVariant
from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, QItemSelectionModel
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor, QIcon, QFont
from PyQt6.QtWidgets import QAbstractItemView, QAbstractItemDelegate, QTreeView
from PyQt6 import Qt6

# https://www.riverbankcomputing.com/pipermail/pyqt/2009-April/022729.html

class Column(object):
    def __init__(self, header=None, type=str):
        self.header = header
    
class Node(object):
    """ Base class for nodes, handles childs management """

    def __init__(self, parent=None):
        self.childs = []
        
        # This list is maintained when children is modified to speed up search from node.
        # Append at end of children list is at no costs, inserts necessitate a recompute.
        self.child_to_row = {} 
       
        self.set_parent(parent)

    def set_parent(self, parent):
        if parent!=None:
            self.parent = parent
            self.parent.insert_child(self)
        else:
            self.parent = None
           
    def insert_child(self, child, row=None):
        self.insert_childs([child], row)
        
    def insert_childs(self, childs, row=None):
        if row is None:
            for child in childs:
                self.child_to_row[child] = len(self.childs)
                self.childs.append(child)
                child.parent = self
        else:
            for child in self.childs[row:]:
                self.child_to_row[child] += len(childs)

            for child in childs:
                self.child_to_row[child] = row
                self.childs.insert(row, child)
                child.parent = self
                row += 1
        
    def child_from_row(self, row):
        return self.childs[row]
   
    def row_from_child(self, child):
        return self.child_to_row[child]
   
    def remove_child(self, child):
        row = self.row_from_child(child)
        del self.child_to_row[child]
        if row<len(self.childs)-1:
            for child in self.childs[row+1:]:
                self.child_to_row[child] -= 1
        self.childs.pop(row) 
        return True
    
    def remove_rows(self, row, count):
        for child in self.childs[row+count:]:
            self.child_to_row[child] -= count
            
        childs = self.childs[row:row+count-1]
        del self.childs[row:row+count-1]
        for child in childs:
            del self.child_to_row[child]
    
    def clear(self):
        self.childs.clear()
        self.child_to_row.clear() 
        
    def GetValue(self, column):
        """ Overload to provide values """
        return None

    def GetDecoration(self, column):
        """ Overload to provide custom decoration """
        # return QIcon() or QColor()
        return None

    def GetBackground(self, column):
        """ Overload to provide custom background """
        # return QColor() or QBrush()
        return None

    def GetForeground(self, column):
        """ Overload to provide custom foreground """
        # return QColor()
        return None

    def GetTextAlignment(self, column):
        """ Overload to provide custom text alignment """
        return Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
    
    def GetFont(self, column):
        """ Overload to provide custom font """
        # font = QFont()
        # font.setBold(True)
        return None
    
    def GetCheckState(self, column):
        """ Overload to provide custom check state """
        # return Qt.CheckState.Checked
        return None

    def GetToolTip(self, column):
        """ Overload to provide custom tooltip """
        return None

    def GetSizeHint(self, column):
        """ Overload to provide custom size hint """
        # return QSize
        return None

    def SetValue(self, column, value):
        """ Overload to set values """
        return False

    def GetFlags(self, column, flags):
        """ Overload to provide custom flags """
        return flags

    def HasChildren(self):
        """ Overload to provide custom children flag """
        if len(self.childs)>0:
            return True
        return False

    def __len__(self):
        return len(self.childs)

    def debug(self, level=0):
        if len(self.child_to_row)>0:
            print(f"{'  '*level}child_to_row:")
            for child in self.child_to_row:
                print(f"{'  '*level}- {child}: {self.child_to_row[child]}")
        
        if len(self.childs)>0:
            print(f"{'  '*level}childs:")
            for i in range(len(self.childs)):
                print(f"{'  '*level}- {i}: {self.childs[i]}")
                self.childs[i].debug(level+1)


class TreeModel(QAbstractItemModel):
    submitted = pyqtSignal()
    reverted = pyqtSignal()
        
    def __init__(self, parent=None, *args, **kwargs):
        super(TreeModel, self).__init__(parent, *args, **kwargs)

        self.treeView = parent
        
        # add columns
        self.columns = []
       
        # create item maps
        self.id_to_node = {}
        self.node_to_id = {}

        # Create root item
        self.rootNode = Node(parent=None)
        self.id_to_node[QModelIndex().internalId()] = self.rootNode
        self.node_to_id[self.rootNode] = QModelIndex().internalId()

        # fetch can be called during remove phase but it's not okay as id maps are not yet consistents
        self._prevent_fetch = False

    # https://coderedirect.com/questions/402089/qtreeview-qabstractitemmodel-insertrow

    ### Overloaded from QAbstractItemModel ###

    def buddy(self, index):
        res = self.Buddy(index)
        if res is None:
            return super(TreeModel, self).buddy(index)
        return res

    # def canDropMimeData (data, action, row, column, parent)

    def canFetchMore(self, parent):
        return self.CanFetchMore(self.node_from_id(parent.internalId()))
    #
    # def clearItemData (index)
    #
    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)
 
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if index.internalId() not in self.id_to_node:
                # There is a problem that should never happen
                print("Error in data model", self, index, index.internalId(), role)
                return QVariant()
            node = self.id_to_node[index.internalId()]
        else:
            node = self.rootNode
        
        if role==Qt.ItemDataRole.DisplayRole or role==Qt.ItemDataRole.EditRole:
            # when in edition then prefill the edit zone with the cell content
            return QVariant(self.GetValue(node, index.column()))
        elif role==Qt.ItemDataRole.DecorationRole:
            return QVariant(self.GetDecoration(node, index.column()))
        elif role==Qt.ItemDataRole.TextAlignmentRole:
            return QVariant(self.GetTextAlignment(node, index.column()))
        elif role==Qt.ItemDataRole.BackgroundRole:
            return QVariant(self.GetBackground(node, index.column()))
        elif role==Qt.ItemDataRole.ForegroundRole:
            return QVariant(self.GetForeground(node, index.column()))
        elif role==Qt.ItemDataRole.FontRole:
            return QVariant(self.GetFont(node, index.column()))
        elif role==Qt.ItemDataRole.CheckStateRole:
            return QVariant(self.GetCheckState(node, index.column()))
        elif role==Qt.ItemDataRole.ToolTipRole:
            return QVariant(self.GetToolTip(node, index.column()))
        elif role==Qt.ItemDataRole.SizeHintRole:
            return QVariant(self.GetSizeHint(node, index.column()))

        # DONE
        # DisplayRole
        # EditRole
        # DecorationRole
        # TextAlignmentRole
        # BackgroundRole
        # ForegroundRole
        # FontRole
        # ToolTipRole
        # SizeHintRole
        # CheckStateRole
        
        # TODO
        # StatusTipRole
        # WhatsThisRole
        # AccessibleTextRole
        # AccessibleDescriptionRole
        # InitialSortOrderRole
        # UserRole
        
        #return super(TreeModel, self).data(index, role)
        return QVariant()

    # def dropMimeData (data, action, row, column, parent)

    def fetchMore(self, parent):
        if self._prevent_fetch:
            return 
        self.Fetch(self.node_from_id(parent.internalId()))
        
    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
       
        if index.isValid() and index.internalId() in self.id_to_node:
            node = self.id_to_node[index.internalId()]
            flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | defaultFlags
            return self.GetFlags(node, index.column(), flags)
        else:
            return Qt.ItemFlag.ItemIsDropEnabled | defaultFlags
    #
    def hasChildren(self, parent=QModelIndex()):
        node = self.node_from_id(parent.internalId())
        return self.HasChildren(node)
    #
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation==Qt.Orientation.Horizontal and role==Qt.ItemDataRole.DisplayRole:
            return self.columns[section].header
        return super(TreeModel, self).headerData(section, orientation, role)

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid():
            parentNode = self.id_to_node[parent.internalId()]
        else:
            parentNode = self.rootNode

        # print(f"index1 row={row} column={column} parent={self.node_to_id[parentNode]}")
        if row>=len(parentNode):
            return QModelIndex()
        
        node = parentNode.child_from_row(row)
        index = self.createIndex(row, column, self.node_to_id[node])
        # print(f"index2 index={index} row={index.row()}")
        
        return index
        
    # def insertColumns (column, count[, parent=QModelIndex()]) 

    # def insertRows(self, row, count, parent=QModelIndex()):

    # def itemData (index)

    # def match (start, role, value[, hits=1[, flags=Qt.MatchFlags(Qt.MatchStartsWith|Qt.MatchWrap)]])

    # def mimeData (indexes)

    # def mimeTypes ()

    # def moveColumns (sourceParent, sourceColumn, count, destinationParent, destinationChild)

    # def moveRows (sourceParent, sourceRow, count, destinationParent, destinationChild)

    def parent(self, child):
        if child.isValid()==False:
            return QModelIndex()
        
        if child.internalId() in self.id_to_node:
            node = self.id_to_node[child.internalId()]
            return self.index_from_node(node.parent)
        return QModelIndex()

    # def removeColumns (column, count[, parent=QModelIndex()])

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row+count-1)
        
        for r in range(row, row+count-1):
            node = parent.child_from_row(r)
            id = self.node_to_id[node]
            del self.id_to_node[id]
            del self.node_to_id[node]
        node = self.node_from_id(parent.internalId())
        parent.remove_rows(row, count)
        
        self.endRemoveRows()
        self.layoutChanged.emit()
        
    # def resetInternalData ()

    def revert(self):
        self.reverted.emit()
        return super(TreeModel, self).revert()

    # def roleNames ()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            node = self.id_to_node[parent.internalId()]
            return len(node)
        else:
            return len(self.rootNode)
        
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        print("setData", index.row(), index.column(), value, role)
        if index.isValid() and role==Qt.ItemDataRole.EditRole:
            node = self.id_to_node[index.internalId()]
            if self.SetValue(node, index.column(), value):
                self.dataChanged.emit(index, index, [role])
                return True
            return False
        return False

    # def setHeaderData (section, orientation, value[, role=Qt.EditRole])

    def setItemData(self, index, roles):
        print("setItemData", index.row(), roles)
        return super(TreeModel, self).setItemData(index, roles)
        
    # def sibling (row, column, idx)

    def sort(self, column, order=Qt.SortOrder.AscendingOrder):
        print("sort", column, order)
    #     return self.Sort(self.node_from_id(parent.internalId()), order)

    # def span (index)

    def submit(self):
        self.submitted.emit()
        return super(TreeModel, self).submit()

    # def supportedDragActions ()

    # def supportedDropActions ()

    ### Private functions ###
    
    def id_from_node(self, node):
        if node is None:
            return QModelIndex().indernalId()
        else:
            return self.node_to_id[node]
    
    def node_from_id(self, id):
        if id not in self.id_to_node:
            return None
        return self.id_to_node[id]

    def index_from_node(self, node, column=0):
        if node is self.rootNode or node is None:
            return QModelIndex()
        row = node.parent.row_from_child(node)
        return self.createIndex(row, column, node)
    
    ### Overloadable functions ###
    
    def InsertNodes(self, nodes, pos=None, parent=None):
        if parent is None:
            parent = self.rootNode
        if pos is None:
            pos = len(parent.childs)
        
        self.layoutAboutToBeChanged.emit()

        parentIndex = self.index_from_node(parent)
        self.beginInsertRows(parentIndex, pos, pos)
        
        row = pos #len(parent.childs)
        for node in nodes:
            node_index = self.createIndex(row, 0, node)
            self.id_to_node[node_index.internalId()] = node
            self.node_to_id[node] = node_index.internalId()
            row += 1
        parent.insert_childs(nodes, pos)

        self.endInsertRows()
        self.layoutChanged.emit()

    def InsertNode(self, node, pos=None, parent=None):
        self.InsertNodes([node], pos, parent)

    def RemoveNodes(self, nodes):
        self._prevent_fetch = True
        self.layoutAboutToBeChanged.emit() #parents=[self.index_from_node(parent)])

        def is_leaf_node(node):
            return len(node.childs)==0
        
        def has_leaf_nodes(node):
            if is_leaf_node(node):
                return False
            for child in node.childs:
                if is_leaf_node(child)==False:
                    return False
            return True
        
        def remove_childs(node):
            nonlocal nodes
            # exclude childs we're going to remove from input and remove it from internal indexes 
            for child in node.childs:
                if child in nodes:
                    nodes.remove(child)
                    index = self.index_from_node(child)
                    del self.id_to_node[index.internalId()]
                    del self.node_to_id[child]
            
            index = self.index_from_node(node)
            self.beginRemoveRows(index, 0, len(node.childs)-1)
            node.clear()
            self.endRemoveRows()
        
        def remove_node(node):
            parent = node.parent
            parent_index = self.index_from_node(parent)
            row = parent.row_from_child(node)
            index = self.index_from_node(node) #self.createIndex(row, 0, node)
            
            self.beginRemoveRows(parent_index, row, row)
            parent.remove_child(node)
            del self.id_to_node[index.internalId()]
            del self.node_to_id[node]
            self.endRemoveRows()

        while len(nodes)>0:
            node = nodes.pop(0)
            if has_leaf_nodes(node):
                remove_childs(node)
                nodes.append(node)
            else:
                if is_leaf_node(node):
                    remove_node(node)
                else:
                    for child in node.childs:
                        if is_leaf_node(child)==False:
                            nodes.insert(child, 0)
                    nodes.append(node)

        self._prevent_fetch = False
        
        self.layoutChanged.emit()

    def RemoveNode(self, node):
        self.RemoveNodes([node])

    def InsertColumn(self, column, pos=None):
        # self.beginInsertColumns(parent, first, last)
        if pos is None:
            self.columns.append(column)
        else:
            self.columns.insert(pos, column)
        # self.layoutChanged(parents, hint)
    
    def CanFetchMore(self, parent):
        """ Called each time user scrolls out of tree, overload to indicate if there is more data"""
        return False

    def Fetch(self, parent):
        """ Called each time user scrolls out of tree, overload to provide nodes """
        pass
    
    def GetValue(self, node, column):
        """ Overload here or inside Node to provide values """
        return node.GetValue(column)
    
    def GetDecoration(self, node, column):
        """ Overload here or inside Node to provide custom decoration """
        """ The decoration is the item at the left of text (icon, checkbox ...) """
        return node.GetDecoration(column)

    def GetTextAlignment(self, node, column):
        """ Overload here or inside Node to provide custom text alignment """
        return node.GetTextAlignment(column)

    def GetBackground(self, node, column):
        """ Overload here or inside Node to provide custom background """
        return node.GetBackground(column)

    def GetForeground(self, node, column):
        """ Overload here or inside Node to provide custom foreground """
        return node.GetForeground(column)

    def GetFont(self, node, column):
        """ Overload here or inside Node to provide custom font """
        return node.GetFont(column)

    def GetCheckState(self, node, column):
        """ Overload here or inside Node to provide check state """
        return node.GetCheckState(column)

    def GetToolTip(self, node, column):
        """ Overload here or inside Node to provide tooltip"""
        return node.GetToolTip(column)

    def GetSizeHint(self, node, column):
        """ Overload here or inside Node to provide size hint"""
        return node.GetSizeHint(column)

    def SetValue(self, node, column, value):
        """ Overload here or inside Node to set value """
        return node.SetValue(column, value)
    
    def GetFlags(self, node, column, flags):
        """ Overload here or inside Node to provide custom flags """
        return node.GetFlags(column, flags)
    
    def HasChildren(self, parent):
        """ Overload here or inside Node to provide custom children flag """
        return parent.HasChildren()

    def Buddy(self, index):
        return None

    def Update(self):
        self.layoutChanged.emit()

    def CreateEditNode(self, parent):
        """ Overload to provide a node for editNew """
        return None

    def Clear(self):
        """ Overload to provide a clear method """
        self.beginResetModel()
        self.id_to_node.clear()
        self.node_to_id.clear()
        self.resetInternalData()
        self.endResetModel()

        # Create root item
        self.rootNode = Node(parent=None)
        self.id_to_node[QModelIndex().internalId()] = self.rootNode
        self.node_to_id[self.rootNode] = QModelIndex().internalId()

        self.modelReset.emit()
        self.layoutChanged.emit()

    def debug(self):
        print("id_to_node:")
        for id in self.id_to_node:
            print(f"- {id}: {self.id_to_node[id]}")
        print("node_to_id")
        for node in self.node_to_id:
            print(f"- {node}: {self.node_to_id[node]}")
    
    def debug_nodes(self):
        print("rootNode:")
        self.rootNode.debug(level=1)


class TreeState(object):
    def __init__(self):
        self.selected = []
        self.expanded = []

class QTreeViewData(QTreeView):
    endInsertEditNode = pyqtSignal(Node)

    def __init__(self, *args, **kwargs):
        super(QTreeViewData, self).__init__(*args, **kwargs)

        # ### From QTreeView ###
        # self.tree_view.collapsed.connect(self.onCollapsed)
        # self.tree_view.expanded.connect(self.onExpanded)

        self.insert_index = None

    def setModel(self, model):
        super(QTreeViewData, self).setModel(model)
        
        model.submitted.connect(self.submitted)
        model.reverted.connect(self.reverted)
        
        
    def closeEditors(self):
        index = self.currentIndex()
        editor = self.indexWidget(index)

        self.commitData(editor)
        self.closeEditor(editor, QAbstractItemDelegate.EndEditHint.NoHint)
    
    def currentIndex(self):
        index = super(QTreeViewData, self).currentIndex()
        if index.internalId() not in self.model().id_to_node:
            return self.model().index_from_node(self.model().rootNode)
        return index
    
    def editNew(self, parent: QModelIndex=None, column: int=0):
        """ Add a new element in edit mode on the first line of parent """
        self.closeEditors()
        self.submitted()  # nasty hack but it is called too late if sent from model
        
        if parent is None:
            parent_index = self.currentIndex()
            parent_node = self.model().node_from_id(parent_index.internalId())
        else:
            parent_node = self.model().rootNode
        
        node = self.model().CreateEditNode(parent_node)
        if node is None:
            return 
        
        # insert node at first parent position
        self.model().InsertNode(node, pos=0, parent=parent_node)
        insert_index = self.model().index_from_node(node, column)
        
        # edit node 
        self.selectionModel().select(insert_index, 
            QItemSelectionModel.SelectionFlag.ClearAndSelect | 
            QItemSelectionModel.SelectionFlag.Rows)
        self.setCurrentIndex(insert_index)
        self.edit(insert_index)
        
        self.insert_index = insert_index
        self.insert_column = column

    def isSelectedRoot(self):
        if self.currentIndex().internalId()==0:
            return True
        return False
    
    def saveState(self):
        state = TreeState()
        for index in self.selectionModel().selectedRows():
            print("##", index.data())
            state.selected.append(index.internalId())
        
        return state
    
    def loadState(self, state):
        model = self.model()
        selectionModel = self.selectionModel()
        
        def index_from_id(id):
            nonlocal model
            if id not in model.id_to_node:
                return None
            node = model.id_to_node[id]
            
            if node is model.rootNode or node is None:
                return None
            row = node.parent.row_from_child(node)
            return model.createIndex(row, 0, node)
        
        selectionModel.clearSelection()
        flags = QItemSelectionModel.SelectionFlag.Select | QItemSelectionModel.SelectionFlag.Rows
        for id in state.selected:
            index = index_from_id(id)
            if index is not None:
                print("**", index.data())
                selectionModel.select(index, flags)

    ### From TreeModel ###
    
    def submitted(self):
        print("submitted", self.insert_index)
        if self.state()!=QAbstractItemView.State.EditingState and self.insert_index is not None:
            # event comes from an element inserted by InsertEditNode
            node = self.model().node_from_id(self.insert_index.internalId())
            self.insert_index = None
            if self.model().GetValue(node, self.insert_column)=="":
                # node was submitted empty, cancel it
                self.model().RemoveNode(node)
                self.setCurrentIndex(self.rootIndex())
            else:
                self.model().RemoveNode(node)
                self.endInsertEditNode.emit(node)
    
    def reverted(self):
        print("reverted", self.insert_index)
        if self.state()!=QAbstractItemView.State.EditingState and self.insert_index is not None:
            # event comes from a element inserted by InsertEditNode
            node = self.model().node_from_id(self.insert_index.internalId())
            self.insert_index = None
            # node was canceled
            self.model().RemoveNode(node)
            self.setCurrentIndex(self.rootIndex())

