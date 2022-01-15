from PyQt6 import Qt6, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit, QMainWindow

from ui.parts_window import PartsWindow
from ui.symbols_widget import SymbolsWidget

from api.command import commands
from api.event import events

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)

        self.actionDatabaseSave.triggered.connect(self.OnActionDatabaseSaveTriggered)
        self.actionEditUndo.triggered.connect(self.OnActionEditUndoTriggered)
        self.actionEditRedo.triggered.connect(self.OnActionEditRedoTriggered)
        self.actionViewParts.triggered.connect(self.OnActionViewPartsTriggered)
        self.actionViewSymbols.triggered.connect(self.OnActionViewSymbolsTriggered)

        self.activeWindow = None 
        self.mdiArea.subWindowActivated.connect(self.OnMdiAreaSubWindowActivated)
        
        commands.done.connect(self.update_menus)
        commands.undone.connect(self.update_menus)
        commands.redone.connect(self.update_menus)
        commands.flushed.connect(self.update_menus)

        # TODO geometry
        # QSettings settings("MyCompany", "MyApp");
        # restoreGeometry(settings.value("myWidget/geometry").toByteArray()); restoreState(settings.value("myWidget/windowState").toByteArray());

        self.update_menus()
        self.update_dock_widgets()

        self.defaultDockPartCategoryWidget = self.dockPartCategoryWidget.widget()
        self.defaultDockFilterWidget = self.dockFilterWidget.widget()
        
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

        self.actionPartAddPart.setEnabled(False)
        self.actionPartAddMetapart.setEnabled(False)
        self.actionPartImportOctopart.setEnabled(False)
        self.actionPartRemovePart.setEnabled(False)
        
        self.actionCategoryAdd.setEnabled(False)
        self.actionCategoryDelete.setEnabled(False)

        self.actionSelectNone.setEnabled(False)
        self.actionSelectAll.setEnabled(False)
        self.actionSelectChildMode.setEnabled(False)

        self.actionParameterAdd.setEnabled(False)
        self.actionMetaParameterAdd.setEnabled(False)
        self.actionParameterDelete.setEnabled(False)

    def update_dock_widgets(self):
        self.dockPartCategoryWidget.setVisible(False)
        self.dockPartParameterWidget.setVisible(False)

    def update(self):
        for child in self.mdiArea.subWindowList():
            print(child)
            child.widget().update()
        super(MainWindow, self).update()
            
    def AddWindow(self, widget_class, title):
        window = widget_class(self.mdiArea)
        window.setWindowTitle(title)
        window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # window = QMdiSubWindow(self.mdiArea)
        # window.setWidget(widget_class(self.mdiArea))
        # window.setWindowTitle(title)

        self.mdiArea.addSubWindow(window)
        window.show()
        return window


    def OnActionDatabaseSaveTriggered(self):
        commands.Flush()


    def OnActionEditUndoTriggered(self):
        commands.Undo()
        self.update()
        
    def OnActionEditRedoTriggered(self):
        commands.Redo()
        self.update()


    def OnActionViewPartsTriggered(self, value):
        self.AddWindow(PartsWindow, "parts")

    def OnActionViewSymbolsTriggered(self, value):
        self.AddWindow(SymbolsWidget, "symbols")


    def OnMdiAreaSubWindowActivated(self, window):
        self.update_menus()
        if self.activeWindow is not None:
            self.activeWindow.widget().deactivated()
        if window is not None:
            window.widget().activated()
        self.activeWindow = window


    def ChangeDockPartCategoryWidget(self, widget=None):
        if widget is None:
            self.dockPartCategoryWidget.setWidget(self.defaultDockPartCategoryWidget)
            self.dockPartCategoryWidget.setVisible(False)
        else:
            self.dockPartCategoryWidget.setWidget(widget)
            self.dockPartCategoryWidget.setVisible(True)

    def ChangeDockFilterWidget(self, widget=None):
        if widget is None:
            self.dockFilterWidget.setWidget(self.defaultDockFilterWidget)
            self.dockFilterWidget.setVisible(False)
        else:
            self.dockFilterWidget.setWidget(widget)
            self.dockFilterWidget.setVisible(True)

main_window = None
app = None