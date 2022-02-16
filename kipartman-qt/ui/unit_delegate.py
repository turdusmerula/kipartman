from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex, QPoint
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QStyledItemDelegate, QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate, QMenu

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from api.treeview import ValidationError
from api.unit import ureg, Quantity
from helper.dialog import ShowErrorDialog
from ui.unit_widget import QUnitWidget

class QUnitDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(QUnitDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QUnitWidget(parent)
        return editor

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, Qt.ItemDataRole.EditRole))
        editor.setText(value)
        
    def setModelData(self, editor, model, index):
        try:
            value = Quantity(editor.text())
            model.setData(index, value, Qt.ItemDataRole.EditRole)
        except Exception as e:
            model.dataError.emit(ValidationError(str(e)))

    def updateEditorGeometry(self, editor, option, index):
        rect = option.rect
        if editor is not None:
            rect.setWidth(editor.rect().width())
            editor.setGeometry(rect)
