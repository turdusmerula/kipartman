from dialogs.panel_part_attachements import PanelPartAttachements
from frames.edit_attachement_frame import EditAttachementFrame
import helper.tree
import wx
import os
import rest
import webbrowser
from configuration import Configuration

configuration = Configuration()

class DataModelPartAttachement(helper.tree.TreeContainerItem):
    def __init__(self, attachement):
        super(DataModelPartAttachement, self).__init__()
        self.attachement = attachement

    def GetValue(self, col):
        url = os.path.join(configuration.kipartbase, 'file', self.attachement.storage_path)
        url = url.replace('\\','/') #Work around for running on Windows
        vMap = { 
            0 : self.attachement.source_name,
            1 : self.attachement.description,
            2 : url
        }
        return vMap[col]

    def IsContainer(self):
        return False

            
class PartAttachementsFrame(PanelPartAttachements):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartAttachementsFrame, self).__init__(parent)

        # create octoparts list
        self.tree_attachements_manager = helper.tree.TreeManager(self.tree_attachements)
        self.tree_attachements_manager.AddTextColumn("File name")
        self.tree_attachements_manager.AddTextColumn("Description")
        self.tree_attachements_manager.AddTextColumn("URI")
        self.tree_attachements_manager.OnItemContextMenu = self.onTreeAttachementsContextMenu
        
        self.enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.showAttachements()

    def enable(self, enabled=True):
        self.button_add_attachement.Enabled = enabled
        self.button_edit_attachement.Enabled = enabled
        self.button_remove_attachement.Enabled = enabled

    def showAttachements(self):
        self.tree_attachements_manager.ClearItems()

        if self.part and self.part.attachements:
            for attachement in self.part.attachements:
                self.tree_attachements_manager.AppendItem(None, DataModelPartAttachement(attachement))
            
    def onButtonAddAttachementClick( self, event ):
        attachement = EditAttachementFrame(self).addAttachement(rest.model.PartAttachement)
        if attachement:
            if self.part.attachements is None:
                self.part.attachements = []
            self.part.attachements.append(attachement)
            self.tree_attachements_manager.AppendItem(None, DataModelPartAttachement(attachement))
             
    def onButtonEditAttachementClick( self, event ):
        item = self.tree_attachements.GetSelection()
        if not item.IsOk():
            return 
        attachementobj = self.tree_attachements_manager.ItemToObject(item)
        EditAttachementFrame(self).editAttachement(attachementobj.attachement)
        self.tree_attachements_manager.UpdateItem(attachementobj)
    
    def onButtonRemoveAttachementClick( self, event ):
        item = self.tree_attachements.GetSelection()
        if not item:
            return
        attachementobj = self.tree_attachements_manager.ItemToObject(item)
        self.part.attachements.remove(attachementobj.attachement)
        self.tree_attachements_manager.DeleteItem(None, attachementobj)
        
    def onTreeAttachementsContextMenu( self, event ):
        self.PopupMenu( self.context_menu, event.GetPosition() )

    def onContextMenuOpenSelection( self, event ):
        item = self.tree_attachements.GetSelection()
        if not item:
            return
        attachementobj = self.tree_attachements_manager.ItemToObject(item)

        configuration = Configuration()
        url = os.path.join(configuration.kipartbase, 'file', attachementobj.attachement.storage_path)
        url = url.replace('\\','/')  #Work around for running on Windows
        webbrowser.open(url)
