from dialogs.panel_part_attachements import PanelPartAttachements
from frames.edit_attachement_frame import EditAttachementFrame
import helper.tree
import wx
import os
import webbrowser
from configuration import configuration

class PartAttachement(helper.tree.TreeContainerItem):
    def __init__(self, attachement):
        super(PartAttachement, self).__init__()
        self.attachement = attachement

    def GetValue(self, col):
#         url = os.path.join(configuration.kipartbase, 'file', self.attachement.storage_path)
#         url = url.replace('\\','/') #Work around for running on Windows
        if col==0:
            return self.attachement.source_name
        elif col==1:
            return self.attachement.description
        #TODO
#         elif col==2:
#             return url

        return ""

    def IsContainer(self):
        return False

            
class TreeManagerPartAttachement(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartAttachement, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddTextColumn("file name")
        self.AddTextColumn("description")
        self.AddTextColumn("URI")
        
    def Load(self):
        self.SaveState()
        
        if self.part is not None:
            for attachement in self.part.attachements.all():
                attachementobj = self.FindAttachement(attachement)
                if attachementobj is None:
                    attachementobj = PartAttachement(attachement)
                    self.Append(None, attachementobj)
                else:
                    attachementobj.part = self.part
                    attachementobj.part_attachement = attachement
                    self.Update(attachementobj)

#             # add not yet persisted data
#             for attachement in self.part.attachements.pendings():
#                 attachementobj = self.FindAttachement(attachement)
#                 if attachementobj is None:
#                     attachementobj = PartAttachement(attachement.part, attachement)
#                     self.Append(None, attachementobj)
#                 else:
#                     attachementobj.part = self.part
#                     attachementobj.part_attachement = attachement
#                     self.Update(attachementobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindAttachement(self, attachement):
        for data in self.data:
            if isinstance(data, PartAttachement) and data.attachement.id==attachement.id:
                return data
        return None

class PartAttachementsFrame(PanelPartAttachements):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartAttachementsFrame, self).__init__(parent)

        # create octoparts list
        self.tree_attachements_manager = TreeManagerPartAttachement(self.tree_attachements)
        self.tree_attachements_manager.OnItemContextMenu = self.onTreeAttachementsBeforeContextMenu
        
        self.tree_attachements_manager.Clear()
        self.SetPart(None)
                
        self._enable(False)
        
    def SetPart(self, part):
        self.part = part
        self.tree_attachements_manager.SetPart(part)
        self._enable(False)
        
    def EditPart(self, part):
        self.part = part
        self.tree_attachements_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled

    def onTreeAttachementsBeforeContextMenu( self, event ):
        self.menu_attachement_add_attachement.Enable(True)
        self.menu_attachement_edit_attachement.Enable(True)
        self.menu_attachement_remove_attachement.Enable(True)
 
        if len(self.tree_attachements.GetSelections())==0:
            self.menu_attachement_edit_attachement.Enable(False)
            self.menu_attachement_remove_attachement.Enable(False)
        if len(self.tree_attachements.GetSelections())>1:
            self.menu_attachement_edit_attachement.Enable(False)
         
        if self.enabled==False:
            self.menu_attachement_add_attachement.Enable(False)
            self.menu_attachement_edit_attachement.Enable(False)
            self.menu_attachement_remove_attachement.Enable(False)
            
#     def onButtonAddAttachementClick( self, event ):
#         attachement = EditAttachementFrame(self).addAttachement(rest.model.PartAttachement)
#         if attachement:
#             if self.part.attachements is None:
#                 self.part.attachements = []
#             self.part.attachements.append(attachement)
#             self.tree_attachements_manager.AppendItem(None, PartAttachement(attachement))
#              
#     def onButtonEditAttachementClick( self, event ):
#         item = self.tree_attachements.GetSelection()
#         if not item.IsOk():
#             return 
#         attachementobj = self.tree_attachements_manager.ItemToObject(item)
#         EditAttachementFrame(self).editAttachement(attachementobj.attachement)
#         self.tree_attachements_manager.UpdateItem(attachementobj)
#     
#     def onButtonRemoveAttachementClick( self, event ):
#         item = self.tree_attachements.GetSelection()
#         if not item:
#             return
#         attachementobj = self.tree_attachements_manager.ItemToObject(item)
#         self.part.attachements.remove(attachementobj.attachement)
#         self.tree_attachements_manager.DeleteItem(None, attachementobj)
#         
#     def onTreeAttachementsContextMenu( self, event ):
#         self.PopupMenu( self.context_menu, event.GetPosition() )
# 
#     def onContextMenuOpenSelection( self, event ):
#         item = self.tree_attachements.GetSelection()
#         if not item:
#             return
#         attachementobj = self.tree_attachements_manager.ItemToObject(item)
# 
#         url = os.path.join(configuration.kipartbase, 'file', attachementobj.attachement.storage_path)
#         url = url.replace('\\','/')  #Work around for running on Windows
#         webbrowser.open(url)
