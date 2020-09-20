from dialogs.panel_symbols import PanelSymbols
import frames
from frames.symbol_libraries_frame import SymbolLibrariesFrame
from frames.symbol_list_frame import SymbolListFrame, FilterLibraryPath
import wx
import helper.filter
from helper.exception import print_stack
# from frames.edit_symbol_frame import EditSymbolFrame, EVT_EDIT_SYMBOL_APPLY_EVENT, EVT_EDIT_SYMBOL_CANCEL_EVENT
# from kicad.kicad_file_manager import KicadFileManagerLib
# from helper.filter import Filter
# import rest 
# import helper.tree
# import os
# from helper.tree import TreeImageList
# from helper.exception import print_stack
# from configuration import configuration
# import wx
# import re
# import sync
# import json
# from helper.connection import check_backend
# from helper.profiler import Trace

class SymbolsFrame(PanelSymbols): 
    def __init__(self, parent):
        super(SymbolsFrame, self).__init__(parent)

        # add libraries panel
        self.panel_libraries = SymbolLibrariesFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_libraries.Bind( frames.symbol_libraries_frame.EVT_SELECT_LIBRARY, self.onSymbolLibrarySelectionChanged )

        # add symbol list panel
        self.panel_symbol_list = SymbolListFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         self.panel_symbol_list.Bind( frames.part_list_frame.EVT_ENTER_EDIT_MODE, self.onPartsEnterEditMode )
#         self.panel_symbol_list.Bind( frames.part_list_frame.EVT_EXIT_EDIT_MODE, self.onPartsExitEditMode )
#         self.panel_symbol_list.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onPartsFilterChanged )

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
