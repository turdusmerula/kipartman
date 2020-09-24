from dialogs.panel_symbols import PanelSymbols
import frames
from frames.symbol_libraries_frame import SymbolLibrariesFrame
from frames.symbol_list_frame import SymbolListFrame, FilterLibraryPath
import wx
import helper.filter
from helper.exception import print_stack

class SymbolsFrame(PanelSymbols): 
    def __init__(self, parent):
        super(SymbolsFrame, self).__init__(parent)

        # add libraries panel
        self.panel_libraries = SymbolLibrariesFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_libraries.Bind( frames.symbol_libraries_frame.EVT_SELECT_LIBRARY, self.onSymbolLibrarySelectionChanged )
        self.panel_libraries.Bind( frames.symbol_libraries_frame.EVT_ADD_SYMBOL, self.onSymbolLibraryAddSymbol )

        # add symbol list panel
        self.panel_symbol_list = SymbolListFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_symbol_list.Bind( frames.symbol_list_frame.EVT_ENTER_EDIT_MODE, self.onSymbolEnterEditMode )
        self.panel_symbol_list.Bind( frames.symbol_list_frame.EVT_EXIT_EDIT_MODE, self.onSymbolExitEditMode )
        self.panel_symbol_list.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onSymbolsFilterChanged )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_libraries, self.panel_symbol_list)
        self.panel_left.Hide()
        self.panel_right.Hide()

    def activate(self):
        self.panel_libraries.activate()
        self.panel_symbol_list.activate()

    def GetMenus(self):
        return None
    
    def onSymbolLibrarySelectionChanged( self, event ):
        self.panel_symbol_list.Filters.replace(FilterLibraryPath(event.path), 'path')
        event.Skip()

    def onSymbolsFilterChanged( self, event ):
        if len(self.panel_symbol_list.Filters.get_filters_group('path'))==0:
            self.panel_libraries.UnselectAll()
        event.Skip()

    def onSymbolLibraryAddSymbol( self, event ):
        self.panel_symbol_list.AddSymbol(event.library)
        event.Skip()

    def onSymbolEnterEditMode( self, event ):
        self.panel_libraries.Enabled = False
        event.Skip()

    def onSymbolExitEditMode( self, event ):
        self.panel_libraries.Enabled = True
        event.Skip()
