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
from api.unit import ureg, Quantity, QuantityRange
from helper.dialog import ShowErrorDialog
from ui.unit_range_widget import QUnitRangeWidget

class QUnitRangeDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(QUnitRangeDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QUnitRangeWidget(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setMinText('')
        editor.setMaxText('')
        if value.min is not None:
            editor.setMinText(str(value.min))
        if value.max is not None:
            editor.setMaxText(str(value.max))
        
    def setModelData(self, editor, model, index):
        value = QuantityRange()

        try:
            if editor.minText()!="":
                value.min = Quantity(editor.minText())
            if editor.maxText()!="":
                value.max = Quantity(editor.maxText())
        except Exception as e:
            model.dataError.emit(ValidationError(str(e)))
            return 
        
        if value.min is not None and value.max is not None and value.min.value>value.max.value:
            model.dataError.emit(ValidationError("Invalid range, maximum is greater than min"))
            
        model.setData(index, value, Qt.ItemDataRole.EditRole)
        
    def updateEditorGeometry(self, editor, option, index):
        rect = option.rect
        if editor is not None:
            rect.setWidth(editor.rect().width())
            editor.setGeometry(rect)
