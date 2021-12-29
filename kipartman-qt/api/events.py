from PyQt6.QtCore import QObject, pyqtSignal

class Events(QObject):
    on_object_update = pyqtSignal(object)
    on_object_delete = pyqtSignal(object)
    on_object_move = pyqtSignal(object, object)     # source destination
    on_object_insert = pyqtSignal(object, object)   # object parent
    
    def __init__(self):
        super(Events, self).__init__()

events = Events()
