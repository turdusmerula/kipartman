from PyQt6.QtCore import QObject, pyqtSignal

class Events(QObject):
    object_added = pyqtSignal(object)
    object_updated = pyqtSignal(object)
    object_deleted = pyqtSignal(object)
    object_moved = pyqtSignal(object, object)     # source destination
    object_inserted = pyqtSignal(object, object)   # object parent
    
    def __init__(self):
        super(Events, self).__init__()

events = Events()
