from dialogs.panel_part_references import PanelPartReferences
import helper.tree

class PartReference(helper.tree.TreeContainerItem):
    def __init__(self, part_reference):
        super(PartReference, self).__init__()
        self.part_reference = part_reference

    def GetValue(self, col):
        if col==0:
            return self.part_reference.type
        elif col==1:
            return self.part_reference.manufacturer
        elif col==2:
            return self.part_reference.name
        elif col==3:
            return self.part_reference.description
        elif col==4:
            return self.part_reference.uid

        return ""

    def GetAttr(self, col, attr):
        res = False
        if self.part_reference.id is None:
            attr.SetColour(helper.colors.GREEN_NEW_ITEM)
            res = True
        if self.part_reference.removed_pending():
            attr.SetStrikethrough(True)
            res = True
        return res


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
            for part_reference in self.part.references.all():
                part_referenceobj = self.FindReference(part_reference)
                if part_referenceobj is None:
                    part_referenceobj = PartReference(part_reference)
                    self.Append(None, part_referenceobj)
                else:
                    # all() extracts from database, fields are not updated to avoid discarding changes
                    self.Update(part_referenceobj)
        
            # add not yet persisted data
            for part_reference in self.part.references.pendings():
                part_referenceobj = self.FindReference(part_reference)
                if part_referenceobj is None:
                    part_referenceobj = PartReference(part_reference)
                    self.Append(None, part_referenceobj)
                else:
                    self.Update(part_referenceobj)

        self.PurgeState()
    
    def SetPart(self, part):
        self.part = part
        self.Clear()
        self.Load()
        
    def FindReference(self, part_reference):
        for data in self.data:
            if isinstance(data, PartReference) and data.part_reference.id==part_reference.id:
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
            self.part.references.remove_pending(referenceobj.part_reference)
        self.tree_references_manager.Load()
