from dialogs.panel_footprints import PanelFootprints
import frames
from frames.footprint_libraries_frame import FootprintLibrariesFrame
from frames.footprint_list_frame import FootprintListFrame, FilterLibraryPath
import wx
import helper.filter
from helper.exception import print_stack

class FootprintsFrame(PanelFootprints): 
    def __init__(self, parent):
        super(FootprintsFrame, self).__init__(parent)

        # add libraries panel
        self.panel_libraries = FootprintLibrariesFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_libraries.Bind( frames.footprint_libraries_frame.EVT_SELECT_LIBRARY, self.onFootprintLibrarySelectionChanged )
        self.panel_libraries.Bind( frames.footprint_libraries_frame.EVT_ADD_FOOTPRINT, self.onFootprintLibraryAddFootprint )

        # add footprint list panel
        self.panel_footprint_list = FootprintListFrame(self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_footprint_list.Bind( frames.footprint_list_frame.EVT_ENTER_EDIT_MODE, self.onFootprintEnterEditMode )
        self.panel_footprint_list.Bind( frames.footprint_list_frame.EVT_EXIT_EDIT_MODE, self.onFootprintExitEditMode )
        self.panel_footprint_list.Filters.Bind( helper.filter.EVT_FILTER_CHANGED, self.onFootprintsFilterChanged )

        # organize panels
        self.splitter_vert.Unsplit()
        self.splitter_vert.SplitVertically( self.panel_libraries, self.panel_footprint_list)
        self.panel_left.Hide()
        self.panel_right.Hide()

    def activate(self):
        self.panel_libraries.activate()
        self.panel_footprint_list.activate()

    def GetMenus(self):
        return None
    
    def onFootprintLibrarySelectionChanged( self, event ):
        self.panel_footprint_list.Filters.replace(FilterLibraryPath(event.path), 'path')
        event.Skip()

    def onFootprintsFilterChanged( self, event ):
        if len(self.panel_footprint_list.Filters.get_filters_group('path'))==0:
            self.panel_libraries.UnselectAll()
        event.Skip()

    def onFootprintLibraryAddFootprint( self, event ):
        self.panel_footprint_list.AddFootprint(event.library)
        event.Skip()

    def onFootprintEnterEditMode( self, event ):
        self.panel_libraries.Enabled = False
        event.Skip()

    def onFootprintExitEditMode( self, event ):
        self.panel_libraries.Enabled = True
        event.Skip()
