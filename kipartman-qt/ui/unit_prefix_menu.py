from PyQt6.QtCore import pyqtSignal, QModelIndex
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

prefixes = [
    # decimal prefixes
    ("y", "yocto - 1e-24"),
    ("z", "zepto - 1e-21"),
    ("a", "atto - 1e-18"),
    ("f", "femto - 1e-15"),
    ("p", "pico - 1e-12"),
    ("n", "nano - 1e-9"),
    (["µ", "u"], "micro - 1e-6"),
    ("m", "milli - 1e-3"),
    ("c", "centi - 1e-2"),
    ("d", "deci - 1e-1"),
    ("da", "deca/deka - 1e+1"),
    ("h", "hecto - 1e2"),
    ("k", "kilo - 1e3"),
    ("M", "mega - 1e6"),
    ("G", "giga - 1e9"),
    ("T", "tera - 1e12"),
    ("P", "peta - 1e15"),
    ("E", "exa - 1e18"),
    ("Z", "zetta - 1e21"),
    ("Y", "yotta - 1e24"),
    "",
    # binary_prefixes
    ("Ki", "kibi - 2**10"),
    ("Mi", "mebi - 2**20"),
    ("Gi", "gibi - 2**30"),
    ("Ti", "tebi - 2**40"),
    ("Pi", "pebi - 2**50"),
    ("Ei", "exbi - 2**60"),
    ("Zi", "zebi - 2**70"),
    ("Yi", "yobi - 2**80"),        
]

class QUnitPrefixMenu(QMenu):
    prefixSelected = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs):
        super(QUnitPrefixMenu, self).__init__(*args, **kwargs)
        
        # TODO tweak presentation with QStyleOptionMenuItem
        
        for item in prefixes:
            if item=="":
                self.addSeparator()
            else:
                prefix, description = item
                if isinstance(prefix, list):
                    text = f"{'/'.join(prefix)} - {description}"
                else:
                    text = f"{prefix} - {description}"
                action = QAction(parent=self, text=text)
                action.prefix = item
                action.triggered.connect(self.selectPrefixAction)
                self.addAction(action)
    
    def selectPrefixAction(self):
        item = self.sender().prefix
        if isinstance(item, tuple)==False:
            return
        prefix, description = item
        if isinstance(prefix, list):
            self.prefixSelected.emit(prefix[0])
        else:
            self.prefixSelected.emit(prefix)
