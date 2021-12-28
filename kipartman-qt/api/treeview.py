from PyQt6.QtCore import Qt, QObject, pyqtSignal, QSize, QVariant
from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import Qt6

class TreeManager(QObject):
    def __init__(self, tree_view, model=None, context_menu=None):
        super(TreeManager, self).__init__()
        
        self.tree_view = tree_view
        self.model = model
        self.context_menu = context_menu

        if model==None:
            self.model = TreeModel()
        else:
            self.model = model
        self.tree_view.setModel(self.model)
        
        # self.sort_order = []
        # self.tree_view.header().sortIndicatorChanged.connect(self.onSortIndicatorChanged)
        # self.tree_view.header().setStyleSheet("QHeaderView::down-arrow { image: url(:/shared/empty); }"
        #                                 "QHeaderView::up-arrow { image: url(:/shared/empty); } ")


    def onSortIndicatorChanged(self, n, order):
        # self.tree_view.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        # self.tree_view.header().setSortIndicator(1, Qt.SortOrder.AscendingOrder)
        # print("onSortIndicatorChanged",  n, order)
        # self.tree_view.header().setSortIndicatorShown(False) 
        # try:
        #     self.sort_order.remove(n)
        # except ValueError:
        #     pass
        # self.sort_order.insert(0, n)
        # self.tree_view.sortByColumn(n, order)
        pass
    
# https://www.riverbankcomputing.com/pipermail/pyqt/2009-April/022729.html

class Column(object):
    def __init__(self, header=None, type=str):
        self.header = header
    
class Node(object):
    def __init__(self, parent=None):
        self.children = []
        
        # this list is maintained when children is modified to speed up search from node
        # append at end of children list is at no costs, inserts necessitate a recompute
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
                self.child_to_row[child] = len(self.children)
                self.children.append(child)
                child.parent = self
        else:
            for child in self.children[row:]:
                self.child_to_row[child] += len(childs)

            for child in childs:
                self.child_to_row[child] = row
                self.children.insert(row, child)
                child.parent = self
                row += 1
        
    def child_from_row(self, row):
        return self.children[row]
   
    def row_from_child(self, child):
        return self.child_to_row[child]
   
    def remove_child(self, child):
        row = self.row_from_child(child)
        del self.child_to_row[child]
        if row<len(self.children)-1:
            for child in self.children[row:]:
                self.child_to_row[child] -= 1
        self.children.pop(row) 
        return True
    
    def __len__(self):
        return len(self.children)

class TreeModel(QAbstractItemModel):
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

    # https://coderedirect.com/questions/402089/qtreeview-qabstractitemmodel-insertrow

    ### Overloaded from QAbstractItemModel ###

    # def buddy (index)

    # def canDropMimeData (data, action, row, column, parent)

    def canFetchMore(self, parent):
        return self.CanFetchMore(self.node_from_id(parent.internalId()))
    #
    # def clearItemData (index)
    #
    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)
 
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role==Qt.ItemDataRole.DecorationRole:
            return QVariant()
        elif role==Qt.ItemDataRole.TextAlignmentRole:
            return QVariant(int(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft))
        # elif role==Qt.ItemDataRole.SizeHintRole:
        #     return QSize(70, 80)
        # elif role== Qt.DecorationRole:
        #     return QVariant(QIcon(self.ListItemData[index.row()]['iconPath']))
               
        if index.isValid():
            node = self.id_to_node[index.internalId()]
        else:
            node = self.rootNode
        
        if role==Qt.ItemDataRole.DisplayRole:
            return QVariant(self.GetValue(node, index.column()))
        if role==Qt.ItemDataRole.EditRole:
            # when in edition then fill the edit zone with the cell content
            return QVariant(self.GetValue(node, index.column()))
            
        #return super(TreeModel, self).data(index, role)
        return QVariant()

    # def dropMimeData (data, action, row, column, parent)

    def fetchMore(self, parent):
        self.Fetch(self.node_from_id(parent.internalId()))
        
    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
       
        if index.isValid():
            node = self.id_to_node[index.internalId()]
            flags = Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | defaultFlags
            return self.GetFlags(node, index.column(), flags)
        else:
            return Qt.ItemFlag.ItemIsDropEnabled | defaultFlags
    #
    def hasChildren(self, parent=QModelIndex()):
        return self.HasChildren(self.node_from_id(parent.internalId()))
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
    #    
        if row>=len(parentNode):
            return QModelIndex()
        
        node = parentNode.child_from_row(row)
        return self.createIndex(row, column, self.node_to_id[node]);
        
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
            return self.node_to_index(node.parent)
        return QModelIndex()

    # def removeColumns (column, count[, parent=QModelIndex()])

    # def removeRows (row, count[, parent=QModelIndex()])

    # def resetInternalData ()

    # def revert ()

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

    # def setItemData (index, roles)

    # def sibling (row, column, idx)

    def sort(self, column, order=Qt.SortOrder.AscendingOrder):
        print("sort", column, order)
    #     return self.Sort(self.node_from_id(parent.internalId()), order)

    # def span (index)

    # def submit ()

    # def supportedDragActions ()

    # def supportedDropActions ()

    ### Private functions ###
    
    def id_from_node(self, node):
        if node is None:
            return QModelIndex().indernalId()
        else:
            return self.node_to_id[node]
    
    def node_from_id(self, id):
        return self.id_to_node[id]

    def node_to_index(self, node):
        if node is self.rootNode or node is None:
            return QModelIndex()
        row = node.parent.row_from_child(node)
        id = self.id_from_node(node)
        return self.createIndex(row, 0, node)
        # parent_id = self.id_from_node(node.parent)
        # return self.createIndex(row, 0, parent_id)
        
    ### Overloadable functions ###
    
    def InsertNodes(self, nodes, pos=None, parent=None):
        if parent is None:
            parent = self.rootNode
        if pos is None:
            pos = len(parent.children)
        
        self.layoutAboutToBeChanged.emit()

        parentIndex = self.node_to_index(parent)
        self.beginInsertRows(parentIndex, pos, pos+len(nodes))
        
        row = len(parent.children)
        for node in nodes:
            node_index = self.createIndex(row, 0, node)
            self.id_to_node[node_index.internalId()] = node
            self.node_to_id[node] = node_index.internalId()
            row += 1
        parent.insert_childs(nodes)
        
        self.endInsertRows()
        self.layoutChanged.emit()

    def InsertNode(self, node, pos=None, parent=None):
        self.InsertNodes([node], pos, parent)

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
        """ Overload to provide values """
        return None
    
    def SetValue(self, node, column, value):
        return False
    
    def GetFlags(self, node, column, flags):
        return flags
    
    def HasChildren(self, parent):
        if len(parent.children)>0:
            return True
        return False

    def Update(self):
        self.layoutChanged.emit()

