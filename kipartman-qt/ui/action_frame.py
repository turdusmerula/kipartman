from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QFrame

class QActionFrame(QFrame):
    currentResult = pyqtSignal(object)
    validated = pyqtSignal(object)
    
    def __init__(self, *args, **kwargs):
        super(QActionFrame, self).__init__(*args, **kwargs)
    
