# https://coderedirect.com/questions/391562/how-to-insert-and-remove-row-from-model-linked-to-qtableview

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Model(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.items = ['Item_A000','Item_B001','Item_A002','Item_B003','Item_B004']
        self.numbers=[20,10,30,50,40]
        self.added=0
    def rowCount(self, parent=QModelIndex()):
        return len(self.items)      
    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role):
        if not index.isValid(): return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        row=index.row()
        column=index.column()

        if column==0:
            if row<len(self.items):
                return QVariant(self.items[row])
        elif column==1:
            if row<len(self.numbers):
                return QVariant( self.numbers[row] )
        else:
            return QVariant()

    def removeRows(self, position, rows=1, index=QModelIndex()):
        print "ntt ...removeRows() Starting position: '%s'"%position, 'with the total rows to be deleted: ', rows
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)       
        self.items = self.items[:position] + self.items[position + rows:]
        self.endRemoveRows()

        return True

    def insertRows(self, position, rows=1, index=QModelIndex()):
        print "ntt ...insertRows() Starting position: '%s'"%position, 'with the total rows to be inserted: ', rows
        indexSelected=self.index(position, 0)
        itemSelected=indexSelected.data().toPyObject()

        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.items.insert(position + row,  "%s_%s"% (itemSelected, self.added))
            self.added+=1
        self.endInsertRows()
        return True

class Proxy(QSortFilterProxyModel):
    def __init__(self):
        super(Proxy, self).__init__()

    def filterAcceptsRow(self, rowProc, parentProc):  
        modelIndex=self.sourceModel().index(rowProc, 0, parentProc)
        item=self.sourceModel().data(modelIndex, Qt.DisplayRole).toPyObject()

        if item and 'B' in item:
            return True
        else: return False


class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        vLayout=QVBoxLayout(self)
        self.setLayout(vLayout)

        hLayout=QHBoxLayout()
        vLayout.insertLayout(0, hLayout)

        tableModel=Model(self)               

        proxyB=Proxy()
        proxyB.setSourceModel(tableModel)

        self.ViewA=QTableView(self)
        self.ViewA.setModel(tableModel)
        self.ViewA.clicked.connect(self.viewClicked)

        self.ViewB=QTableView(self) 
        self.ViewB.setModel(proxyB)
        self.ViewB.clicked.connect(self.viewClicked)
        self.ViewB.setSortingEnabled(True)
        self.ViewB.sortByColumn(0, Qt.AscendingOrder)
        self.ViewB.setSelectionBehavior(QTableView.SelectRows)

        hLayout.addWidget(self.ViewA)
        hLayout.addWidget(self.ViewB)

        insertButton=QPushButton('Insert Row Above Selection')
        insertButton.setObjectName('insertButton')
        insertButton.clicked.connect(self.buttonClicked)
        removeButton=QPushButton('Remove Selected Item')
        removeButton.setObjectName('removeButton')
        removeButton.clicked.connect(self.buttonClicked)

        vLayout.addWidget(insertButton)
        vLayout.addWidget(removeButton)

    def getZeroColumnSelectedIndexes(self, tableView=None):
        if not tableView: return
        selectedIndexes=tableView.selectedIndexes()
        if not selectedIndexes: return
        return [index for index in selectedIndexes if not index.column()]

    def viewClicked(self, indexClicked):
        print 'indexClicked() row: %s  column: %s'%(indexClicked.row(), indexClicked.column() )
        proxy=indexClicked.model()

    def buttonClicked(self):
        button=self.sender()
        if not button: return

        tableView=None
        if self.ViewA.hasFocus(): tableView=self.ViewA
        elif self.ViewB.hasFocus(): tableView=self.ViewB
        if not tableView: print 'buttonClicked(): not tableView'; return

        zeroColumnSelectedIndexes=self.getZeroColumnSelectedIndexes(tableView)
        if not zeroColumnSelectedIndexes: print 'not zeroColumnSelectedIndexes'; return

        firstZeroColumnSelectedIndex=zeroColumnSelectedIndexes[0]
        if not firstZeroColumnSelectedIndex or not firstZeroColumnSelectedIndex.isValid():
            print 'buttonClicked(): not firstZeroColumnSelectedIndex.isValid()'; return            

        startingRow=firstZeroColumnSelectedIndex.row()
        print 'n buttonClicked() startingRow =', startingRow

        if button.objectName()=='removeButton':            
            tableView.model().removeRows(startingRow, len(zeroColumnSelectedIndexes), QModelIndex())

        elif button.objectName()=='insertButton':
            tableView.model().insertRows(startingRow, len(zeroColumnSelectedIndexes), QModelIndex())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
    