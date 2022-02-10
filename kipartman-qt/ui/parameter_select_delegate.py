from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QStyledItemDelegate, QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate, QDialog

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from helper.dialog import ShowErrorDialog
from ui.modal_dialog import QModalDialog
from ui.parameter_select_widget import QParameterSelectWidget

# from PyQt6.QtWidgets import qApp
class QParameterSelectDelegate(QStyledItemDelegate):
    buttonCloseClicked = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(QParameterSelectDelegate, self).__init__(parent)
        
        self.widget = None
        self.parameter = None

    def createEditor(self, parent, option, index):
        self.widget = QFrame(parent)
        uic.loadUi('ui/parameter_select_delegate.ui', self.widget)
        
        self.widget.toolButton.clicked.connect(self.toolButtonTriggered)
        return self.widget

    def setEditorData(self, editor, index):
        self.parameter = index.model().data(index, Qt.ItemDataRole.EditRole)
        if self.parameter is None:
            self.widget.label.setText("<None>")
        else:
            self.widget.label.setText(self.parameter.name)
        
    def setModelData(self, editor, model, index):
        model.setData(index, self.parameter, Qt.ItemDataRole.EditRole)

    # def updateEditorGeometry(self, editor, option, index):
    #     rect = option.rect
    #     rect.setWidth(self.widget.rect().width())
    #     rect.setHeight(self.widget.rect().height())
    #     editor.setGeometry(rect)

    def toolButtonTriggered(self, value):
        dialog = QModalDialog(self.widget, title="Select parameter") 
        widget = QParameterSelectWidget(dialog)
        dialog.setWidget(widget)
        dialog.validated.connect(self.dialogValidated)
        dialog.show()
    
    def dialogValidated(self, object):
        self.parameter = object
        self.widget.label.setText(self.parameter.name)
        