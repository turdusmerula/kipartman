from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect
from PyQt6.QtGui import QStandardItem, QStandardItemModel
# from PyQt6.QtWidgets import qApp

from api.command import commands
from api.event import events
from api.data.filter import FilterModel
from api.filter import FilterSet, Filter
from helper.dialog import ShowErrorDialog

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame,\
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate


class ButtonCloseDelegate(QItemDelegate):
    def __init__(self, parent):
        super(ButtonCloseDelegate, self).__init__(parent)

        self.icon = QIcon()
        self.icon.addFile(u"ui/icons/close-48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        
        # self.index = None
        
    def createEditor(self, parent, option, index):
        # self.index = index
        
        frame = QFrame(parent)
        horizontalLayout = QHBoxLayout(frame)
        horizontalLayout.setSpacing(0)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(horizontalSpacer)

        closeButton = QPushButton(frame)
        closeButton.setMaximumSize(QSize(16, 16))
        closeButton.setIcon(self.icon)
        closeButton.setIconSize(QSize(12, 12))
        closeButton.clicked.connect(self.OnCloseButtonClicked)
        
        horizontalLayout.addWidget(closeButton)

        return frame

    def OnCloseButtonClicked(self):
        pass
        # if self.index is None:
        #     return
        # print("---", self.index.data())

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

        # self.model.AddSection("category", "Category filter")
        # self.model.AddFilter(Filter("test"), "category")
        # self.model.AddFilter(Filter("test2"), "category")
        
        self.filters.filterChanged.connect(self.OnFilterListChanged)
        
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

        