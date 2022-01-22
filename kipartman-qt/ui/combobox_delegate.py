from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QStyledItemDelegate, QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from helper.dialog import ShowErrorDialog


# from PyQt6.QtWidgets import qApp
class QComboboxDelegate(QStyledItemDelegate):
    buttonCloseClicked = pyqtSignal(QModelIndex)

    def __init__(self, parent, items):
        super(QComboboxDelegate, self).__init__(parent)
        
        self.widget = None
        self.items = items
        
    def createEditor(self, parent, option, index):
        self.widget = QFrame(parent)
        uic.loadUi('ui/combobox_delegate.ui', self.widget)
        
        self.widget.comboBox.addItems(self.items)
        
        return self.widget

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        index = editor.comboBox.setCurrentIndex(editor.comboBox.findText(value))
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.comboBox.currentText(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        rect = option.rect
        rect.setWidth(self.widget.rect().width())
        rect.setHeight(self.widget.rect().height())
        editor.setGeometry(rect)

