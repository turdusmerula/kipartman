from dialogs.dialog_project import DialogProject
from frames.buy_frame import BuyFrame
from frames.bom_frame import BomFrame
from frames.schematic_frame import SchematicFrame
from frames.configuration_frame import ConfigurationFrame
from helper.exception import print_stack
import helper.tree
import os
import wx
from kicad.kicad_project import KicadProject

class DataModelFilePath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(DataModelFilePath, self).__init__()
        self.path = path
        
    def GetValue(self, col):
        vMap = { 
            0 : os.path.basename(self.path),
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

class DataModelFile(helper.tree.TreeContainerItem):
    def __init__(self, path, name):
        super(DataModelFile, self).__init__()
        self.path = os.path.join(path, name)
        self.name = name
        
    def GetValue(self, col):
        vMap = { 
            0 : self.name,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = False
        return True

class TreeManagerFiles(helper.tree.TreeManager):
    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerFiles, self).__init__(tree_view, *args, **kwargs)

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelFilePath) and data.path==os.path.normpath(path):
                return data
        return None

    def FindFile(self, path, name):
        pathobj = self.FindPath(path)
        for data in self.data:
            if isinstance(data, DataModelFile) and data.name==name and data.parent==pathobj:
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelFilePath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def AppendFile(self, path, name):
        fileobj = self.FindFile(path, name)
        if fileobj:
            return fileobj
        pathobj = self.FindPath(path)
        fileobj = DataModelFile(path, name)
        self.AppendItem(pathobj, fileobj)


class ProjectFrame(DialogProject): 
    def __init__(self, parent, project_path): 
        DialogProject.__init__(self, parent)
        
        self.project_path = project_path
        
        self.menus = self.menu_bar.GetMenus()

        self.kicad_project = KicadProject(self.project_path)
        self.kicad_project.on_change_hook = self.onProjectFileChanged

        # create libraries data
        self.tree_project_manager = TreeManagerFiles(self.tree_project, context_menu=self.menu_project)
        self.tree_project_manager.AddTextColumn("name")
        self.tree_project_manager.OnSelectionChanged = self.onTreeProjectSelChanged
        self.tree_project_manager.OnItemBeforeContextMenu = self.onTreeProjectBeforeContextMenu
        self.load()

        self.pages = []
        
    def onMenuViewConfigurationSelection( self, event ):
        ConfigurationFrame(self).ShowModal()
    
    def OnMenuItem( self, event ):
        self.pages[self.notebook.GetSelection()].OnMenuItem(event)

    def onProjectFileChanged(self, path):
        self.kicad_project.Enabled(False)
        
        # do a synchronize when a file change on disk
        self.load()

        # reload pages
        for page in self.pages:
            if path.endswith(".bom") and isinstance(page, BomFrame):
                page.reload()
            elif path.endswith(".sch") and isinstance(page, SchematicFrame):
                page.reload()
        
        self.kicad_project.Enabled(True)
        
    def load(self):
        try:
            self.loadFiles()
        except Exception as e:
            print_stack()
            wx.MessageBox(format(e), 'Project load failed', wx.OK | wx.ICON_ERROR)                                    
                    
    def loadFiles(self):
        self.kicad_project.Load()
        
        self.tree_project_manager.SaveState()
        
        # load libraries tree
        for file_path in self.kicad_project.files:
            # decompose path
            folders = []
            file_name = os.path.basename(file_path)
            path = os.path.dirname(file_path)
            while path!='' and path!='/':
                folders.insert(0, path)
                path = os.path.dirname(path)
            
            file_path = self.kicad_project.root_path
            for folder in folders:
                file_path = os.path.join(self.kicad_project.root_path, folder)
                pathobj = self.tree_project_manager.FindPath(folder)
                if self.tree_project_manager.DropStateObject(pathobj)==False:
                    self.tree_project_manager.AppendPath(folder)
                     
            fileobj = self.tree_project_manager.FindFile(file_path, file_name)
            if self.tree_project_manager.DropStateObject(fileobj)==False:
                self.tree_project_manager.AppendFile(file_path, file_name)
                            
        self.tree_project_manager.PurgeState()

    def onTreeProjectSelChanged( self, event ):
        item = self.tree_project.GetSelection()
        if item.IsOk()==False:
            return    
        pathobj = self.tree_project_manager.ItemToObject(item)

    def onTreeProjectBeforeContextMenu( self, event ):
        item = self.tree_project.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_project_manager.ItemToObject(item)

    def onButtonRefreshProjectClick( self, event ):
        self.load()

    def onMenuProjectOpenSelection( self, event ):
        item = self.tree_project.GetSelection()
        if item.IsOk()==False:
            return    
        obj = self.tree_project_manager.ItemToObject(item)

        if isinstance(obj, DataModelFile):
#             if obj.name.endswith(".bom"):
#                 bom = BomFrame(self.notebook)
#                 self.pages.append(bom)
#                 self.notebook.AddPage(bom, obj.path, False)
            if obj.name.endswith(".sch"):
                sch = SchematicFrame(self.notebook, obj.path)
                self.pages.append(sch)
                self.notebook.AddPage(sch, obj.name, False)
                
    def onMenuProjectNewBomSelection( self, event ):
        pass
