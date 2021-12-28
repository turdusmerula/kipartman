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

        commands.on_do.connect(self.update_menus)
        commands.on_undo.connect(self.update_menus)
        commands.on_redo.connect(self.update_menus)
        commands.on_flush.connect(self.update_menus)
        
        self.update_menus()

    def update_menus(self):
        self.actionSchematicOpen.setEnabled(False)
        self.actionSchematicSave.setEnabled(False)
        
        self.actionDatabaseSave.setEnabled(commands.HasUndo)
        
        if commands.HasUndo:
            self.actionEditUndo.setEnabled(True)
            self.actionEditUndo.setText(f"Undo {commands.LastUndo.description}")
        else:
            self.actionEditUndo.setEnabled(False)
            self.actionEditUndo.setText(f"Undo")
            
        if commands.HasRedo:
            self.actionEditRedo.setEnabled(True)
            self.actionEditRedo.setText(f"Redo {commands.LastRedo.description}")
        else:
            self.actionEditRedo.setEnabled(False)
            self.actionEditRedo.setText(f"Redo")

    def refresh_childs(self):
        for child in self.mdiArea.subWindowList():
            print(child)
            child.widget().update()
            
    def AddWindow(self, widget_class, title):
        window = QMdiSubWindow(self.mdiArea)
        window.setWidget(widget_class(self.mdiArea))
        window.setWindowTitle(title)
        # subWindow1.setAttribute(Qt6.WA_DeleteOnClose)
        self.mdiArea.addSubWindow(window)
        window.show()
        return window


    def OnActionDatabaseSaveTriggered(self):
        commands.Flush()


    def OnActionEditUndoTriggered(self):
        commands.Undo()
        self.refresh_childs()
        
    def OnActionEditRedoTriggered(self):
        commands.Redo()
        self.refresh_childs()


    def OnActionViewPartsTriggered(self, value):
        self.AddWindow(PartsWidget, "parts")
