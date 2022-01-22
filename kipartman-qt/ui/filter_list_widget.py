from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from helper.dialog import ShowErrorDialog
from ui.button_close_delegate import ButtonCloseDelegate


# from PyQt6.QtWidgets import qApp
class IndentationDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(IndentationDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        if index.column()==0:
            opt.rect.adjust(opt.rect.height(), 0, 0, 0)
        super(IndentationDelegate, self).paint(painter, opt, index)
        
        if index.column()==0:
            branch = QStyleOptionViewItem()
            branch.rect = QRect(0, opt.rect.y(), opt.rect.height(), opt.rect.height())
            branch.state = option.state
            widget = option.widget
            if widget is None:
                style = QApplication.style
            else:
                style = widget.style()
            style.drawPrimitive(QStyle.PrimitiveElement.PE_IndicatorBranch, branch, painter, widget)

class QFilterListWidget(QtWidgets.QWidget):
    selectionChanged = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(QFilterListWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/filter_list_widget.ui', self)

        self.filters = FilterSet()
        self.model = FilterModel(self.filters)
        self.treeView.setModel(self.model)
        self.treeView.setMouseTracking(True)

        self.buttonDelegate = ButtonCloseDelegate(self.model)
        self.indentDelegate = IndentationDelegate(self.model)
        # self.treeView.setItemDelegateForColumn(0, self.indentDelegate) 
        self.treeView.setItemDelegateForColumn(1, self.buttonDelegate) 

        from ui.main_window import app
        app.focusChanged.connect(self.update_menus)
        
        self.filters.filterChanged.connect(self.OnFilterListChanged)
        self.buttonDelegate.buttonCloseClicked.connect(self.OnButtonCloseFilterClicked)
        
        self.update_menus()
        
    def update(self):
        # update treeview
        self.model.Update()
        super(QFilterListWidget, self).update()

    def update_menus(self):
        from ui.main_window import main_window
        if main_window is None:
            return
        
        pass

    def OnFilterListChanged(self):
        # self.model.Clear()
        self.model.Update()

    def OnButtonCloseFilterClicked(self, index):
        node = self.model.node_from_index(index)
        if isinstance(node, GroupNode):
            node.group.Clear()
        elif isinstance(node, FilterNode):
            node.parent.group.Remove(node.filter)

    