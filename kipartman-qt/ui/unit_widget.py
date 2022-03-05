from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex, QPoint
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QCursor, QPalette
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QStyledItemDelegate, QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate, QMenu

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from api.unit import ureg
from helper.dialog import ShowErrorDialog
from ui.unit_menu import QUnitMenu
from ui.unit_prefix_menu import QUnitPrefixMenu

class QUnitWidget(QFrame):
    def __init__(self, parent):
        super(QUnitWidget, self).__init__(parent)
        uic.loadUi('ui/unit_widget.ui', self)

        self.menuUnit = QUnitMenu(self)
        self.menuPrefix = QUnitPrefixMenu(self)
        
        self.lineEdit.textChanged.connect(self.lineEditTextChanged)
        self.toolButtonPrefix.clicked.connect(self.toolButtonPrefixTriggered)
        self.toolButtonUnit.clicked.connect(self.toolButtonUnitTriggered)
        self.menuUnit.unitSelected.connect(self.insertItem)
        self.menuPrefix.prefixSelected.connect(self.insertItem)

        self.defaultPalette = self.lineEdit.palette()
        self.errorPalette = QPalette()
        self.errorPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.red)
        
    def text(self):
        return self.lineEdit.text()
    
    def setText(self, text):
        self.lineEdit.setText(text)


    def toolButtonPrefixTriggered(self):
        rect = self.toolButtonPrefix.rect()
        self.menuPrefix.popup(self.toolButtonPrefix.mapToGlobal(QPoint(rect.x(), rect.y()+rect.height())))

    def toolButtonUnitTriggered(self):
        rect = self.toolButtonUnit.rect()
        self.menuUnit.popup(self.toolButtonUnit.mapToGlobal(QPoint(rect.x(), rect.y()+rect.height())))

    def lineEditTextChanged(self):
        try:
            # check unit consistency
            ureg.parse_expression(self.lineEdit.text())
            self.lineEdit.setPalette(self.defaultPalette)
        except Exception as e:
            self.lineEdit.setPalette(self.errorPalette)
            
    def insertItem(self, value):
        self.lineEdit.insert(value)
        self.lineEdit.setFocus()

    def setFocus(self):
        self.lineEdit.setFocus()
