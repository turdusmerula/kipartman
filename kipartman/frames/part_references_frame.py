from dialogs.panel_part_references import PanelPartReferences
import helper.tree

class PartReference(helper.tree.TreeContainerItem):
    def __init__(self, reference):
        super(PartReference, self).__init__()
        self.reference = reference

    def GetValue(self, col):
        if col==0:
            return self.reference.type
        elif col==1:
            return self.reference.manufacturer
        elif col==2:
            return self.reference.name
        elif col==3:
            return self.reference.description
        elif col==4:
            return self.reference.uid

        return ""

class TreeManagerPartReference(helper.tree.TreeManager):

    def __init__(self, tree_view, *args, **kwargs):
        super(TreeManagerPartReference, self).__init__(tree_view, *args, **kwargs)

        self.part = None
        
        self.AddTextColumn("provider")
        self.AddTextColumn("manufacturer")
        self.AddTextColumn("name")
        self.AddTextColumn("description")
        self.AddTextColumn("UID")
        
    def Load(self):
        
        self.SaveState()
        
        if self.part is not None:
            for reference in self.part.references.all():
                referenceobj = self.FindReference(reference)
                if referenceobj is None:
                    referenceobj = PartReference(reference)
                    self.Append(None, referenceobj)
                else:
                    referenceobj.part_parameter = reference
                    self.Update(referenceobj)
        
        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Load()
        
    def FindReference(self, reference):
        for data in self.data:
            if isinstance(data, PartReference) and data.reference.id==reference:
                return data
        return None

class PartReferencesFrame(PanelPartReferences):
    def __init__(self, parent): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(PartReferencesFrame, self).__init__(parent)

        # create references list
        self.tree_references_manager = TreeManagerPartReference(self.tree_references, context_menu=self.menu_reference)
        self.tree_references_manager.OnItemBeforeContextMenu = self.onTreeReferencesBeforeContextMenu
        
        self.tree_references_manager.Clear()
        self.SetPart(None)
        
        self._enable(False)
            
    def SetPart(self, part):
        self.part = part
        self.tree_references_manager.SetPart(part)
        self._enable(False)
    
    def EditPart(self, part):
        self.part = part
        self.tree_references_manager.SetPart(part)
        self._enable(True)

    def _enable(self, enabled=True):
        self.enabled = enabled
    
    def onTreeReferencesBeforeContextMenu( self, event ):
        self.menu_reference_remove_reference.Enable(True)
        if len(self.tree_references.GetSelections())==0:
            self.menu_reference_remove_reference.Enable(False)
        
        if self.enabled==False:
            self.menu_reference_remove_reference.Enable(False)
            
    def onMenuReferenceRemoveReference( self, event ):
        references = []
        for item in self.tree_references.GetSelections():
            obj = self.tree_references_manager.ItemToObject(item)
            if isinstance(obj, PartReference):
                references.append(obj)
        for referenceobj in references:
            self.part.references.remove(referenceobj.reference)
            self.tree_references_manager.DeleteItem(None, referenceobj)
