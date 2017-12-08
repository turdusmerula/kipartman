from pywinauto.application import Application
'''http://pywinauto.readthedocs.io/en/latest/code/code.html#main-user-modules'''

'''
TODO:  
    Improve interface setup speed.
        split the application process connect from the find window
    
    monitor for proces terminate
DONE:
    monitor for Component Editor window appearing
        work done, A multiprocess Win32 Event watcher on Kicad
        Repo: BSFE-KiCADddm
        Branch: TEST17W48d5-GUIautomation
        TAG:    INTEGRATE_with_GUIAutomate_and_Kipartman

    Automatically detect Value, Footprint
'''

class KicadEeschemaComponentProperties:
    """
    Manage a component's properties through the Kicad Eeschema Dialog 'Component Properties'
    """

    def __init__( self  ):
        self._app = Application(backend="uia")
        self.hWnd = 0
    def connect(self):

#        self._app = self._app.connect(path='Kicad')
        self._app = self._app.connect(path='kicad.exe')
        #TODO: check connection was made
        self._thewinTop = self._app.top_window()
        
    def windowComponentProperties(self):

        self._dlgCompProp = self._thewinTop.window(best_match=u'Component Properties')
        if self._dlgCompProp.exists():
                #self.refresh()
                return True

        else:
             print("Window Does not exist")
             return False
        pass

    def refresh(self):
        # Retrieve the Dict of fields on the Component
        self._cListBox = self._dlgCompProp.ListBox.wrapper_object()
        self._cFields = {t[0]:{'Index': i,'Value':t[1:]} for i,t in enumerate(self._cListBox.texts())}
        

    def update_field(self,field_name='', value =u''):
        self._cListBox.items()[self._cFields[field_name]['Index']].select()
        d1=self._dlgCompProp.child_window(title="Field Name:",  control_type="Edit").wrapper_object()
        assert field_name == d1.legacy_properties()['Value']

        d2=self._dlgCompProp.child_window(title="Field Value:",  control_type="Edit").wrapper_object()
        d2.set_text(value)
        self._cListBox.items()[self._cFields['Reference']['Index']].select()
        self.refresh()

    def get_field(self,field_name=''):
        #TODO: check if there is a better way to refresh maybe not on every get
        #self.refresh()
        return self._cFields[field_name]['Value'][0]


    def test(self):
        self.update_field('SPR', 'TEST')
        self.update_field('MFR', 'Multicomp')
        self.update_field('MPN', 'MCSR06X1002FTL')
        self.update_field('SPURL', 'http:')
    def reset(self):
        self.update_field('SPR', '-')
        self.update_field('MFR', '-')
        self.update_field('SPURL', '-')
