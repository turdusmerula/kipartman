from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QFrame

from api.data.parameter_search import ParameterModel, ParameterNode
from api.event import events
from api.filter import FilterSet, FilterGroup
from database.models import PartCategory
from helper.dialog import ShowErrorDialog
from ui.action_frame import QActionFrame


class QParameterSelectWidget(QActionFrame):

    def __init__(self, *args, **kwargs):
        super(QParameterSelectWidget, self).__init__(*args, **kwargs)
        uic.loadUi('ui/parameter_select_widget.ui', self)

        self.model = ParameterModel()
        self.treeView.setModel(self.model)
        self.treeView.selectionModel().selectionChanged.connect(self.treeViewSelectionChanged)
        self.treeView.doubleClicked.connect(self.treeViewDoubleClicked)

        self.lineEdit.textChanged.connect(self.lineEditTextChanged)
        
    def treeViewSelectionChanged(self, selected, deselected):
        if len(self.treeView.selectionModel().selectedRows())>0:
            node = self.treeView.model().node_from_index(self.treeView.selectionModel().selectedRows()[0])
            self.currentResult.emit(node.parameter)
        else:
            self.currentResult.emit(None)

    def treeViewDoubleClicked(self, event):
        if len(self.treeView.selectionModel().selectedRows())>0:
            node = self.treeView.model().node_from_index(self.treeView.selectionModel().selectedRows()[0])
            self.validated.emit(node.parameter)

    def lineEditTextChanged(self, text):
        self.model.SetFilter(self.lineEdit.text())
        self.model.Update()