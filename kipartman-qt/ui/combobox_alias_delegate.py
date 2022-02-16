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

class QComboboxAliasDelegate(QStyledItemDelegate):
    buttonCloseClicked = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(QComboboxAliasDelegate, self).__init__(parent)
        
        self.widget = None

    def createEditor(self, parent, option, index):
        editor = QFrame(parent)
        uic.loadUi('ui/combobox_alias_delegate.ui', editor)
        editor.comboBox.currentTextChanged.connect(self.comboBoxCurrentTextChanged)
        editor.toolButtonAdd.clicked.connect(self.toolButtonAddTriggered)
        editor.toolButtonRemove.clicked.connect(self.toolButtonRemoveTriggered)

        editor.toolButtonAdd.setEnabled(False)
        editor.toolButtonAdd.setEnabled(False)
        
        self.widget = editor
        
        return editor

    def setEditorData(self, editor, index):
        values = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.comboBox.addItems(values)
        
    def setModelData(self, editor, model, index):
        values = []
        if editor.comboBox.currentIndex()!=-1:
            values.append(editor.comboBox.itemText(editor.comboBox.currentIndex()))
        for i in range(0, editor.comboBox.count()):
            if editor.comboBox.itemText(i) not in values:
                values.append(editor.comboBox.itemText(i))
        
        model.setData(index, values, Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        rect = option.rect
        if editor is not None:
            rect.setWidth(editor.rect().width())
            editor.setGeometry(rect)

    def comboBoxCurrentTextChanged(self):
        self.widget.toolButtonAdd.setEnabled(False)
        self.widget.toolButtonRemove.setEnabled(False)
    
        found = self.widget.comboBox.findText(self.widget.comboBox.currentText(), Qt.MatchFlag.MatchExactly)
        if found==-1 and self.widget.comboBox.currentText()!="":
            self.widget.toolButtonAdd.setEnabled(True)
        if found!=-1:
            self.widget.toolButtonRemove.setEnabled(True)
            
            
    def toolButtonAddTriggered(self):
        self.widget.comboBox.addItem(self.widget.comboBox.currentText())
        self.widget.comboBox.setCurrentIndex(self.widget.comboBox.count()-1)
        
        self.widget.toolButtonAdd.setEnabled(False)
        self.widget.toolButtonRemove.setEnabled(True)
        self.widget.comboBox.setFocus()

    def toolButtonRemoveTriggered(self):
        found = self.widget.comboBox.findText(self.widget.comboBox.currentText(), Qt.MatchFlag.MatchExactly)
        self.widget.comboBox.removeItem(found)
        self.widget.comboBox.setFocus()
        
 