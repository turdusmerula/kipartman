from PyQt6 import Qt6, QtWidgets, uic
from PyQt6.QtGui import QWindowStateChangeEvent
from PyQt6.QtCore import pyqtSignal, QEvent
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit


class QChildWindow(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(QChildWindow, self).__init__(parent)
        
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        # names = {}
        # for value in QEvent.Type:
        #     names[value.value] = value.name
        # if event.type() not in names:
        #     names[event.type()] = "## UNKNOWN ##"
        #
        # print(object, names[event.type()])
        #
        # if event.type()==QEvent.Type.WindowActivate:
        #     print("activate")
        return super(QChildWindow, self).eventFilter(object, event)
    
    def update_menus(self):
        pass

    def activated(self):
        pass
    
    def deactivated(self):
        pass
    