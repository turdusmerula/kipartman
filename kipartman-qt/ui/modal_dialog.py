from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QEvent, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QFrame, QDialog, QDialogButtonBox


class QModalDialog(QDialog):
    validated = pyqtSignal(object)
    cancelled = pyqtSignal()

    def __init__(self, *args, title="Kipartman", **kwargs):
        super(QModalDialog, self).__init__(*args, **kwargs)
        uic.loadUi('ui/modal_dialog.ui', self)
        
        self.setWindowTitle(title)
        self.setModal(True)
        
        self.result = None

        self.buttonBox.clicked.connect(self.buttonBoxClicked)
        
    def setWidget(self, widget):
        self.layout().replaceWidget(self.widget, widget)
        widget.currentResult.connect(self.widgetCurrentResult)
        widget.validated.connect(self.widgetValidated)
        # self.widget = widget

    def buttonBoxClicked(self, button):
        if button==self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel):
            self.cancelled.emit()
            self.close()
        elif button==self.buttonBox.button(QDialogButtonBox.StandardButton.Ok):
            self.validated.emit(self.result)
            self.close()
    
    def widgetCurrentResult(self, object):
        if object is None:
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        else:
            self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
        self.result = object
    
    def widgetValidated(self, object):
        self.validated.emit(self.result)
        self.close()
        
     