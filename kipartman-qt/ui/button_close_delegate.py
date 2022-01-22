from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate

from api.command import commands
from api.data.filter import FilterModel, GroupNode, FilterNode
from api.event import events
from api.filter import FilterSet, Filter
from helper.dialog import ShowErrorDialog


# from PyQt6.QtWidgets import qApp
class ButtonCloseDelegate(QItemDelegate):
    buttonCloseClicked = pyqtSignal(QModelIndex)

    def __init__(self, parent):
        super(ButtonCloseDelegate, self).__init__(parent)

        self.icon = QIcon()
        self.icon.addFile(u"ui/icons/close-48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        
        self.index = None
        
    def createEditor(self, parent, option, index):
        self.index = index
        
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
        if self.index is None or self.index.isValid()==False:
            return
        self.buttonCloseClicked.emit(self.index)
