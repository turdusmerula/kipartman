from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal, QRect, QModelIndex, QPoint
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QCursor, QPalette
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QWidget, QStyledItemDelegate, QItemDelegate, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame, \
    QStyleOptionViewItem, QApplication, QStyle, QStyledItemDelegate, QMenu,\
    QLineEdit, QToolButton, QLabel


class QMetapartLoadWidget(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent, loaded, count):
        super(QMetapartLoadWidget, self).__init__(parent)
        
        self.setText(f"Load more from Octopart ... ({loaded}/{count})")
        self.setStyleSheet("QLabel { color : blue; }") 

    def mousePressEvent(self, event):
        self.clicked.emit()
