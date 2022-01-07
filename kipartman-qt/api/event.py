from PyQt6.QtCore import QObject, pyqtSignal

class Events(QObject):
    objectAdded = pyqtSignal(object)
    objectUpdated = pyqtSignal(object)
    objectDeleted = pyqtSignal(object, int)
    object_moved = pyqtSignal(object, object)     # source / destination
    object_inserted = pyqtSignal(object, object)   # object / parent

    focusChanged = pyqtSignal(object)

    def __init__(self):
        super(Events, self).__init__()

events = Events()
