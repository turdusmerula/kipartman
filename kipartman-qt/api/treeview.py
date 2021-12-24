from PyQt6.QtCore import Qt, QObject, pyqtSignal, QSize, QVariant
from PyQt6.QtCore import QRunnable, QThreadPool
from PyQt6.QtCore import QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6 import Qt6

class TreeDataSignal(QObject):
    signal = pyqtSignal(object, object)

class TreeLoader(QObject):
    def __init__(self):
        super().__init__()

class TreeAsyncLoader(QRunnable):
    def __init__(self):
        super(TreeAsyncLoader, self).__init__()
        self.on_data = TreeDataSignal()


class TreeItem(object):
    pass

class TreeModel(QStandardItemModel):
    def __init__(self, loader=None, *args, **kwargs):
        super(TreeModel, self).__init__(*args, **kwargs)

        self.loader = loader
        self.loaded = False

    def Load(self, reload=False, *args, **kwargs):
        if issubclass(self.loader, TreeLoader):
            self.sync_load(self.loader, reload, *args, **kwargs)
        elif issubclass(self.loader, TreeAsyncLoader):
            self.async_load(self.loader, reload, *args, **kwargs)

    def sync_load(self, Loader, reload, *args, **kwargs):
        if reload:
            self.loaded = False
        if self.loaded==False:
            loader = Loader(*args, **kwargs)
            loader.run()
        self.loaded = True
    
    def async_load(self, AsyncLoader, reload, *args, **kwargs):
        if reload:
            self.loaded = False
        if self.loaded==False:
            loader = AsyncLoader()
            loader.on_data.signal.connect(self.OnData)
            QThreadPool.globalInstance().start(loader)
        self.loaded = True

    def OnData(self, parent, items):
        """ Override to provide custom load behavior """
        pass

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

# https://www.riverbankcomputing.com/pipermail/pyqt/2009-April/022729.html

class BaseColumn(object):
    def __init__(self, header=None, type=str):
        self.header = header
    
class BaseNode(object):
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

class BaseTreeModel(QAbstractItemModel):
    def __init__(self, parent=None, loader=None, *args, **kwargs):
        super(BaseTreeModel, self).__init__(parent, *args, **kwargs)

        self.loader = loader
        self.loaded = False

        self.treeView = parent
        
        # add columns
        self.columns = []
       
        # create item maps
        self.id_to_node = {}
        self.node_to_id = {}

        # Create root item
        self.rootNode = BaseNode(parent=None)
        self.id_to_node[QModelIndex().internalId()] = self.rootNode
        self.node_to_id[self.rootNode] = QModelIndex().internalId()
        
    def Load(self, reload=False, *args, **kwargs): 
        if issubclass(self.loader, TreeLoader):
            self.sync_load(self.loader, reload, *args, **kwargs)
        elif issubclass(self.loader, TreeAsyncLoader):
            self.async_load(self.loader, reload, *args, **kwargs)

    def sync_load(self, Loader, reload, *args, **kwargs):
        if reload:
            self.loaded = False
        if self.loaded==False:
            loader = Loader(*args, **kwargs)
            loader.run()
        self.loaded = True
    
    def async_load(self, AsyncLoader, reload, *args, **kwargs):
        if reload:
            self.loaded = False
        if self.loaded==False:
            loader = AsyncLoader()
            loader.on_data.signal.connect(self.OnData)
            QThreadPool.globalInstance().start(loader)
        self.loaded = True

    def OnData(self, parent, items):
        """ Override to provide custom load behavior """
        pass


    # https://coderedirect.com/questions/402089/qtreeview-qabstractitemmodel-insertrow

    ### Overloaded from QAbstractItemModel ###
    
    # def buddy (index)
    #
    # def canDropMimeData (data, action, row, column, parent)
    #
    # def canFetchMore (parent)
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
        
        #return super(BaseTreeModel, self).data(index, role)
        return QVariant()

    # def dropMimeData (data, action, row, column, parent)
    #
    # def fetchMore (parent)
    #
    def flags(self, index):
        defaultFlags = QAbstractItemModel.flags(self, index)
       
        if index.isValid():
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | defaultFlags
        else:
            return Qt.ItemFlag.ItemIsDropEnabled | defaultFlags
    #
    # def hasChildren ([parent=QModelIndex()])
    #
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation==Qt.Orientation.Horizontal and role==Qt.ItemDataRole.DisplayRole:
            return self.columns[section].header
        return super(BaseTreeModel, self).headerData(section, orientation, role)

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
    #
    # def insertRows(self, row, count, parent=QModelIndex()):
    #     if parent.isValid():
    #         parentNode = self.id_to_node[parent.internalId()]
    #     else:
    #         parentNode = self.rootNode
    #
    #     self.beginInsertRows(parent, row, row+count)
    #
    #     node = BaseNode(parentNode)
    #
    #     parentNode.appendChild(BaseNode(None), row)
    #
    #     self.endInsertRows()
    #
    #     return True

    # def itemData (index)
    #
    # def match (start, role, value[, hits=1[, flags=Qt.MatchFlags(Qt.MatchStartsWith|Qt.MatchWrap)]])
    #
    # def mimeData (indexes)
    #
    # def mimeTypes ()
    #
    # def moveColumns (sourceParent, sourceColumn, count, destinationParent, destinationChild)
    #
    # def moveRows (sourceParent, sourceRow, count, destinationParent, destinationChild)
    #
    def parent(self, child):
        if child.isValid()==False:
            return QModelIndex()
        
        if child.internalId() in self.id_to_node:
            node = self.id_to_node[child.internalId()]
            return self.node_to_index(node.parent)
        return QModelIndex()

    # def removeColumns (column, count[, parent=QModelIndex()])
    #
    # def removeRows (row, count[, parent=QModelIndex()])
    #
    # def resetInternalData ()
    #
    # def revert ()
    #
    # def roleNames ()
    #
    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            node = self.id_to_node[parent.internalId()]
            return len(node)
        else:
            return len(self.rootNode)
        
    # def setData (index, value[, role=Qt.EditRole])
    #
    # def setHeaderData (section, orientation, value[, role=Qt.EditRole])
    #
    # def setItemData (index, roles)
    #
    # def sibling (row, column, idx)
    #
    # def sort (column[, order=Qt.AscendingOrder])
    #
    # def span (index)
    #
    # def submit ()
    #
    # def supportedDragActions ()
    #
    # def supportedDropActions ()

    ### Private functions ###
    
    def id_from_node(self, node):
        if node is None:
            return QModelIndex().indernalId()
        else:
            return self.node_to_id[node]
    
    def node_from_id(self, id):
        return self.node_from_id(id)

    def node_to_index(self, node):
        if node is self.rootNode or node is None:
            return QModelIndex()
        row = node.parent.row_from_child(node)
        parent_id = self.id_from_node(node.parent)
        self.createIndex(row, 0, parent_id)
        
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
        if pos is None:
            self.columns.append(column)
        else:
            self.columns.insert(pos, column)
        # self.layoutChanged(parents, hint)
    
    def GetValue(self, node, column):
        return None
    