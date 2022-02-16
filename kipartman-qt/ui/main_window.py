from PyQt6 import Qt6, QtWidgets, uic
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QMdiSubWindow, QTextEdit, QMainWindow

from api.command import commands
from api.event import events
from ui.parts_window import PartsWindow
from ui.symbols_widget import SymbolsWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)


        self.actionDatabaseSave.triggered.connect(self.actionDatabaseSaveTriggered)
        self.actionEditUndo.triggered.connect(self.actionEditUndoTriggered)
        self.actionEditRedo.triggered.connect(self.actionEditRedoTriggered)
        self.actionViewParts.triggered.connect(self.actionViewPartsTriggered)
        self.actionViewSymbols.triggered.connect(self.actionViewSymbolsTriggered)
        self.actionConfiguration.triggered.connect(self.actionConfigurationTriggered)

        self.activeWindow = None 
        self.mdiArea.subWindowActivated.connect(self.mdiAreaSubWindowActivated)
        
        commands.done.connect(self.update_menus)
        commands.undone.connect(self.update_menus)
        commands.redone.connect(self.update_menus)
        commands.flushed.connect(self.update_menus)

        app.focusChanged.connect(self.globalFocusChanged)

        # restoreGeometry(settings.value("myWidget/geometry").toByteArray()); restoreState(settings.value("myWidget/windowState").toByteArray());

        self.update_menus()
        self.update_dock_widgets()

        self.defaultDockPartCategoryWidget = self.dockPartCategoryWidget.widget()
        self.defaultDockFilterWidget = self.dockFilterWidget.widget()
        self.defaultDockPartParameterWidget = self.dockPartParameterWidget.widget()

        self.actionPartAddPart.setEnabled(False)
        self.actionPartAddMetapart.setEnabled(False)
        self.actionPartImportOctopart.setEnabled(False)
        self.actionPartDelete.setEnabled(False)

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
        self.dockParameterWidget.setVisible(False)
        self.dockPartParameterWidget.setVisible(False)
        self.dockStorageWidget.setVisible(False)
        self.dockPartStorageWidget.setVisible(False)
        self.dockFilterWidget.setVisible(False)
        
    def update(self):
        for child in self.mdiArea.subWindowList():
            child.widget().update()
        super(MainWindow, self).update()

    def globalFocusChanged(self):
        self.update_menus()
        events.focusChanged.emit(None)

    def saveWindowSettings(self, name):
        settings = QSettings("Kipartman", name)
        settings.setValue("geometry", self.saveGeometry()) 
        settings.setValue("windowState", self.saveState())
        print(settings.fileName())
    
    def loadWindowSettings(self, name):
        settings = QSettings("Kipartman", name)
        # if settings.value("geometry") is not None:
        #     saved_geometry = settings.value("geometry")
        #     self.restoreGeometry(saved_geometry)
        if settings.value("windowState") is not None:
            saved_state = settings.value("windowState")
            self.restoreState(saved_state)
    

    def AddWindow(self, widget_class, title):
        window = widget_class(self.mdiArea)
        window.setWindowTitle(title)
        window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        window.setWindowState(Qt.WindowState.WindowMaximized);

        # window = QMdiSubWindow(self.mdiArea)
        # window.setWidget(widget_class(self.mdiArea))
        # window.setWindowTitle(title)

        self.mdiArea.addSubWindow(window)
        window.show()
        return window


    def actionDatabaseSaveTriggered(self):
        commands.Flush()


    def actionEditUndoTriggered(self):
        commands.Undo()
        self.update()
        
    def actionEditRedoTriggered(self):
        commands.Redo()
        self.update()


    def actionViewPartsTriggered(self, value):
        self.AddWindow(PartsWindow, "parts")

    def actionViewSymbolsTriggered(self, value):
        self.AddWindow(SymbolsWidget, "symbols")


    def actionConfigurationTriggered(self, value):
        # from api.octopart.queries import OctopartPartQuery
        # query = OctopartPartQuery()
        # query.search("ATSAMD21G18A-MU")
        from api.unit import ureg, Quantity
        a = ureg.Quantity("2")
        b = ureg.Quantity("2 mF")
        c = ureg.Quantity("2 mF", "F")
        pass

    def mdiAreaSubWindowActivated(self, window):
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

    def ChangeDockPartParameterWidget(self, widget=None):
        if widget is None:
            self.dockPartParameterWidget.setWidget(self.defaultDockPartParameterWidget)
            self.dockPartParameterWidget.setVisible(False)
        else:
            self.dockPartParameterWidget.setWidget(widget)
            self.dockPartParameterWidget.setVisible(True)

main_window = None
app = None