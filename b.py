# http://rowinggolfer.blogspot.com/2010/05/qtreeview-and-qabractitemmodel-example.html

import sys
from functools import partial
from PyQt4 import QtGui, QtCore

HORIZONTAL_HEADERS = ("Asset Name", "Date Added")


class AssetClass(object):
    '''
    a trivial custom data object
    '''

    def __init__(self, **kwargs):
        if not kwargs.get('name') or not kwargs.get('type'):
            return
        self.name = kwargs.get('name')
        self.date_added = kwargs.get('date_added')
        self.type = kwargs.get('type')

    def __repr__(self):
        return "%s - %s %s" % (self.type, self.name, self.date_added)


class TreeItem(object):
    '''
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    '''

    def __init__(self, asset, header, parent_item):
        self.asset = asset
        self.parent_item = parent_item
        self.header = header
        self.child_items = []

    def appendChild(self, item):
        self.child_items.append(item)

    def removeChild(self, item):
        self.child_items.remove(item)

    def child(self, row):
        return self.child_items[row]

    def childCount(self):
        return len(self.child_items)

    def columnCount(self):
        return 2

    def data(self, column):
        if self.asset == None:
            if column == 0:
                return QtCore.QVariant(self.header)
            if column == 1:
                return QtCore.QVariant("")
        else:
            if column == 0:
                return QtCore.QVariant(self.asset.name)
            if column == 1:
                return QtCore.QVariant(self.asset.date_added)
        return QtCore.QVariant()

    def parent(self):
        return self.parent_item

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0


class TreeModel(QtCore.QAbstractItemModel):
    '''
    a model to display a few names, ordered by sex
    '''

    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)
        self.assets = []
        model_data = (("VEHICLE", "Truck", 'May 27th, 2020'),
                      ("VEHICLE", "Car", 'May 25th, 2020'),
                      ("CHARACTER", "Peter", 'May 27th, 2020'),
                      ("CHARACTER", "Rachel", 'May 29th, 2020'),
                      ("PROP", "Chair", 'May 27th, 2020'),
                      ("PROP", "Axe", 'May 17th, 2020'))
        for asset_type, name, date in model_data:
            asset = AssetClass(type=asset_type, name=name, date_added=date)
            self.assets.append(asset)

        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.setupModelData()

    def columnCount(self, parent=None):
        if parent and parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return len(HORIZONTAL_HEADERS)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())
        if role == QtCore.Qt.UserRole:
            if item:
                return item.asset

        return QtCore.QVariant()

    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and
                role == QtCore.Qt.DisplayRole):
            try:
                return QtCore.QVariant(HORIZONTAL_HEADERS[column])
            except IndexError:
                pass

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        childItem = parent_item.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QtCore.QModelIndex()

        parent_item = childItem.parent()

        if parent_item == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_Item = self.rootItem
        else:
            p_Item = parent.internalPointer()
        return p_Item.childCount()

    def setupModelData(self):
        for asset in self.assets:
            asset_type = asset.type

            if not self.parents.has_key(asset_type):
                new_parent = TreeItem(None, asset_type, self.rootItem)
                self.rootItem.appendChild(new_parent)

                self.parents[asset_type] = new_parent

            parent_item = self.parents[asset_type]
            new_item = TreeItem(asset, "", parent_item)
            parent_item.appendChild(new_item)

    def addSubRow(self, new_asset):
        asset_type, name, date = new_asset
        asset = AssetClass(type=asset_type, name=name, date_added=date)
        parent_item = self.parents[asset_type]
        already_exists = False
        for child in parent_item.child_items:
            if child.asset.name == name and child.asset.type == asset_type:
                already_exists = True
        if already_exists:
            print 'this asset already exists'
            return
        new_item = TreeItem(asset, "", parent_item)
        parent_item.appendChild(new_item)

    def customRemoveRow(self, rowIndex):
        child_tree_item = rowIndex.internalPointer()
        asset_type = rowIndex.parent().data().toString()
        parent_item = self.parents[str(asset_type)]
        self.beginRemoveRows(rowIndex.parent(), rowIndex.row(), rowIndex.row() + 1)
        parent_item.removeChild(child_tree_item)
        self.endRemoveRows()

    def searchModel(self, asset):
        '''
        get the modelIndex for a given appointment
        '''

        def searchNode(node):
            '''
            a function called recursively, looking at all nodes beneath node
            '''
            for child in node.child_items:
                print child.childCount()
                if asset == child.asset:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    result = searchNode(child)
                    if result:
                        return result

        retarg = searchNode(self.parents[0])
        print retarg
        return retarg

    def findAssetName(self, name):
        app = None
        for asset in self.assets:
            if asset.name == name:
                app = asset
                break
        if app != None:
            index = self.searchModel(app)
            return (True, index)
        return (False, None)


class TreeView(QtGui.QTreeView):
    right_button_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def selectedRows(self):
        rows = []
        for index in self.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        print type(rows)
        return rows

    def openMenu(self, position):
        indexes = self.selectedIndexes()
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QtGui.QMenu()
        editMenu = None
        if level == 0:
            editMenu = QtGui.QAction("Edit person", self)
            menu.addAction(editMenu)
        elif level == 1:
            editMenu = QtGui.QAction("Delete", self)
            menu.addAction(editMenu)
        elif level == 2:
            editMenu = QtGui.QAction("Edit object", self)
            menu.addAction(editMenu)

        if editMenu:
            editMenu.triggered.connect(self._on_right_click)

        menu.exec_(self.viewport().mapToGlobal(position))

    def _on_right_click(self):
        self.right_button_clicked.emit()

class Proxy01(QtGui.QSortFilterProxyModel):
    def __init__(self):
        super(Proxy01, self).__init__()
        self.keyword = None
        self.searched_parents = None

    def setFilterRegExp(self, pattern):
        if isinstance(pattern, str):
            pattern = QtCore.QRegExp(pattern, QtCore.Qt.CaseInsensitive,
                                        QtCore.QRegExp.FixedString)
        super(Proxy01, self).setFilterRegExp(pattern)

    def _accept_index(self, idx):
        if idx.isValid():
            text = idx.data(QtCore.Qt.DisplayRole).toString()
            if self.filterRegExp().indexIn(text) >= 0:
                return True
            for row in range(idx.model().rowCount(idx)):
                if self._accept_index(idx.model().index(row, 0, idx)):
                    return True
        return False

    def filterAcceptsRow(self, source_row, source_parent):
        idx = self.sourceModel().index(source_row, 0, source_parent)
        return self._accept_index(idx)


class Dialog(QtGui.QDialog):
    add_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setMinimumSize(300, 150)

        self.model = TreeModel()
        self.proxy1 = Proxy01()
        self.proxy1.setSourceModel(self.model)
        self.proxy1.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        layout = QtGui.QVBoxLayout(self)

        self.tree_view = TreeView(self)
        self.tree_view.setModel(self.proxy1)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.right_button_clicked.connect(self.deleteMenuButtonClicked)
        layout.addWidget(self.tree_view)

        label = QtGui.QLabel("Search for the following person")
        layout.addWidget(label)

        search_layout = QtGui.QHBoxLayout(self)

        self.search_line_edit = QtGui.QLineEdit()
        self.search_line_edit.textChanged.connect(self.updateFilter)
        search_layout.addWidget(self.search_line_edit)

        search_line_button = QtGui.QPushButton('Search')
        search_line_button.setMaximumWidth(75)
        search_layout.addWidget(search_line_button)

        layout.addLayout(search_layout)

        self.add_button = QtGui.QPushButton("Add \"Character - Smith\"")
        layout.addWidget(self.add_button)
        QtCore.QObject.connect(self.add_button, QtCore.SIGNAL("clicked()"), self.addButtonClicked)

        self.delete_button = QtGui.QPushButton("Delete Selected")
        layout.addWidget(self.delete_button)
        QtCore.QObject.connect(self.delete_button, QtCore.SIGNAL("clicked()"), self.deleteButtonClicked)

        self.but = QtGui.QPushButton("Clear Selection")
        layout.addWidget(self.but)
        QtCore.QObject.connect(self.but, QtCore.SIGNAL("clicked()"), self.tree_view.clearSelection)

        QtCore.QObject.connect(self.tree_view, QtCore.SIGNAL("clicked(QModelIndex)"), self.row_clicked)

    def row_clicked(self, index):
        '''
        when a row is clicked... show the name
        '''
        real_index = self.tree_view.model().mapToSource(index)
        print self.tree_view.model().sourceModel().data(real_index, QtCore.Qt.UserRole)

    def but_clicked(self):
        '''
        when a name button is clicked, I iterate over the model,
        find the person with this name, and set the treeviews current item
        '''
        name = self.sender().text()
        print "BUTTON CLICKED:", name
        result, index = self.model.findAssetName(name)
        if result:
            if index:
                self.tree_view.setCurrentIndex(index)
                return
        self.tree_view.clearSelection()

    def addButtonClicked(self):
        new_asset = ("CHARACTER", "Smith", 'May 28th, 2020')
        self.model.addSubRow(new_asset)
        self.proxy1.invalidate()

    @QtCore.pyqtSlot()
    def deleteMenuButtonClicked(self):
        self.deleteButtonClicked()

    def deleteButtonClicked(self):
        current = self.tree_view.currentIndex()
        source_index = self.proxy1.mapToSource(current)
        self.model.customRemoveRow(source_index)
        self.proxy1.invalidate()

    def customFilter(self):
        self.proxy1.setKeyword(self.search_line_edit.text())

    def updateFilter(self, text):
        self.proxy1.setFilterRegExp(text)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_()