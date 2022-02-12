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
from api.unit import ureg, UnitValue
from helper.dialog import ShowErrorDialog
from ui.unit_range_widget import QUnitRangeWidget

class QUnitRangeDelegate(QStyledItemDelegate):
    buttonUnitClicked = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(QUnitRangeDelegate, self).__init__(parent)
        
        self.widget = None

    def createEditor(self, parent, option, index):
        self.widget = QUnitRangeWidget(parent)
        return self.widget

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, Qt.ItemDataRole.EditRole))
        editor.setText(value)
        
    def setModelData(self, editor, model, index):
        value = UnitValue()
        value.from_str(editor.text())
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    # def updateEditorGeometry(self, editor, option, index):
    #     rect = option.rect
    #     rect.setWidth(self.widget.rect().width())
    #     rect.setHeight(self.widget.rect().height())
    #     editor.setGeometry(rect)
