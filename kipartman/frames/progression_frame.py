from dialogs.dialog_progression import DialogProgression
import wx

class ProgressionFrame(DialogProgression):
    def __init__(self, parent, title): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(ProgressionFrame, self).__init__(parent)
        
        self.SetTitle(title) ;
        
        # set result functions
        self.canceled = False
        self.result = None

    def SetProgression(self, caption, current_item, max_item):
        self.static_progression.Label = "%s (%d / %d)"%(caption, current_item, max_item)
        
        self.gauge_progression.SetRange(max_item)
        self.gauge_progression.SetValue(current_item)
    
    def Canceled(self):
        return self.canceled 
    
    def onCancelButtonClick( self, event ):
        self.canceled = True
