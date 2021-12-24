from PyQt6 import Qt6
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit

from ui.parts_widget import PartsWidget

from api.command import commands

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)

        self.actionDatabaseSave.triggered.connect(self.OnActionDatabaseSaveTriggered)

        self.actionEditUndo.triggered.connect(self.OnActionEditUndoTriggered)
        self.actionEditRedo.triggered.connect(self.OnActionEditRedoTriggered)

        self.actionViewParts.triggered.connect(self.OnActionViewPartsTriggered)

        commands.on_undo.connect(self.OnCommandUndoTriggered)
        commands.on_redo.connect(self.OnCommandRedoTriggered)
        
        self.update_menus()

    def update_menus(self):
        self.actionSchematicOpen.setEnabled(False)
        self.actionSchematicSave.setEnabled(False)
        
        self.actionDatabaseSave.setEnabled(commands.HasUndo())
        
        self.actionEditUndo.setEnabled(commands.HasUndo())
        self.actionEditRedo.setEnabled(commands.HasRedo())

    def AddWindow(self, widget_class, title):
        window = QMdiSubWindow(self.mdiArea)
        window.setWidget(widget_class(self.mdiArea))
        window.setWindowTitle(title)
        # subWindow1.setAttribute(Qt6.WA_DeleteOnClose)
        self.mdiArea.addSubWindow(window)
        window.show()
        return window


    def OnActionDatabaseSaveTriggered(self):
        # TODO commit transaction
        commands.Flush()


    def OnActionEditUndoTriggered(self):
        commands.Undo()

    def OnActionEditRedoTriggered(self):
        commands.Redo()


    def OnActionViewPartsTriggered(self, value):
        self.AddWindow(PartsWidget, "parts")


    def OnCommandUndoTriggered(self):
        self.update_menus()

    def OnCommandRedoTriggered(self):
        self.update_menus()
