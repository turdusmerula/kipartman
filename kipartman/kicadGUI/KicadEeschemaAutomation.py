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
        self.componentID=''

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
        #TODO: Retrieve 'Component ID:' /
        #https://onedrive.live.com/edit.aspx/Personal%20^5Web^6?cid=cc518521c9785e69&id=documents&wd=target%28BSFE%20Electronic%20Engineering%2FKICAD%20notes.one%7C51EBB93C-A386-41F3-A731-AE7350ADC068%2F17W48%20Kipartman%20Kicad%20Interface%7CB4FF5EE3-FF6B-43C8-8083-6866445524F6%2F%29
        #onenote:https://d.docs.live.net/cc518521c9785e69/Personal%20(Web)/BSFE%20Electronic%20Engineering/KICAD%20notes.one#17W48%20Kipartman%20Kicad%20Interface&section-id={51EBB93C-A386-41F3-A731-AE7350ADC068}&page-id={B4FF5EE3-FF6B-43C8-8083-6866445524F6}&object-id={35BAD83A-5084-4002-885B-34598FF497A8}&E
        #
        #TODO: IMPROVE the pywinauto interface remove wrapper_object. /
        #http://pywinauto.readthedocs.io/en/latest/getting_started.html?highlight=wrapper_object
        #Python can hide this wrapper_object() call so that you have more compact code in production. The following statements do absolutely the same:
        # Alter child_window
        # Remove wrapper_object
        # does not seem possible but the line below using iface_value seems the better way ??
        #self.componentID = self._dlgCompProp.child_window(title="Component ID:",  control_type="Edit").wrapper_object().legacy_properties()['Value']
        #self.componentID = self._dlgCompProp.child_window(title="Component ID:", control_type="Edit").wrapper_object().iface_value.CurrentValue
        self.componentID = self._dlgCompProp.componentidEdit.wrapper_object().iface_value.CurrentValue
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
