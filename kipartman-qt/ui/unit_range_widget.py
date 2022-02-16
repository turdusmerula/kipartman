from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex, QPoint
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QCursor, QPalette
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QStyledItemDelegate, QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate, QMenu,\
    QLineEdit

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from api.unit import ureg
from helper.dialog import ShowErrorDialog
from ui.unit_menu import QUnitMenu
from ui.unit_prefix_menu import QUnitPrefixMenu

class QUnitRangeLineEdit(QLineEdit):
    focusIn = pyqtSignal(QLineEdit)

    def __init__(self, *args, **kwargs):
        super(QUnitRangeLineEdit, self).__init__(*args, **kwargs)
    
    def focusInEvent(self, event):
        super(QUnitRangeLineEdit, self).focusInEvent(event)
        self.focusIn.emit(self)

class QUnitRangeWidget(QFrame):
    buttonUnitClicked = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(QUnitRangeWidget, self).__init__(parent)
        uic.loadUi('ui/unit_range_widget.ui', self)

        self.menuUnit = QUnitMenu(self)
        self.menuPrefix = QUnitPrefixMenu(self)

        self.lineEditMin.textChanged.connect(self.lineEditMinTextChanged)
        self.lineEditMin.focusIn.connect(self.lineEditFocusChanged)
        
        self.lineEditMax.textChanged.connect(self.lineEditMaxTextChanged)
        self.lineEditMax.focusIn.connect(self.lineEditFocusChanged)
        
        self.toolButtonPrefix.clicked.connect(self.toolButtonPrefixTriggered)
        self.toolButtonUnit.clicked.connect(self.toolButtonUnitTriggered)
        self.menuUnit.unitSelected.connect(self.insertItem)
        self.menuPrefix.prefixSelected.connect(self.insertItem)

        self.defaultPalette = self.lineEditMin.palette()
        self.errorPalette = QPalette()
        self.errorPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.red)

        self.currentEdit = self.lineEditMin
        self.lineEditMin.setFocus()
        
    def minText(self):
        return self.lineEditMin.text()
    
    def setMinText(self, text):
        self.lineEditMin.setText(text)

    def maxText(self):
        return self.lineEditMax.text()
    
    def setMaxText(self, text):
        self.lineEditMax.setText(text)

    def toolButtonPrefixTriggered(self):
        rect = self.toolButtonPrefix.rect()
        self.menuPrefix.popup(self.toolButtonPrefix.mapToGlobal(QPoint(rect.x(), rect.y()+rect.height())))

    def toolButtonUnitTriggered(self):
        rect = self.toolButtonUnit.rect()
        self.menuUnit.popup(self.toolButtonUnit.mapToGlobal(QPoint(rect.x(), rect.y()+rect.height())))


    def lineEditMinTextChanged(self):
        try:
            # check unit consistency
            ureg.parse_expression(self.lineEditMin.text())
            self.lineEditMin.setPalette(self.defaultPalette)
        except Exception as e:
            self.lineEditMin.setPalette(self.errorPalette)

    def lineEditMaxTextChanged(self):
        try:
            # check unit consistency
            ureg.parse_expression(self.lineEditMax.text())
            self.lineEditMax.setPalette(self.defaultPalette)
        except Exception as e:
            self.lineEditMax.setPalette(self.errorPalette)

    def lineEditFocusChanged(self, lineEdit):
        self.currentEdit = lineEdit
            
    def insertItem(self, value):
        self.currentEdit.insert(value)
        self.currentEdit.setFocus()

    def setFocus(self):
        self.currentEdit.setFocus()
