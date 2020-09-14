# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  2 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelFootprintList
###########################################################################

class PanelFootprintList ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_horz = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_LIVE_UPDATE )
		self.splitter_horz.Bind( wx.EVT_IDLE, self.splitter_horzOnIdle )
		self.splitter_horz.SetMinimumPaneSize( 100 )

		self.panel_up = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.toolbar_filters.SetMinSize( wx.Size( -1,31 ) )

		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer12.Add( self.toolbar_filters, 0, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.toolbar_footprint = wx.ToolBar( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT )
		self.toolbar_footprint.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.toolbar_footprint.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.toggle_footprint_path = self.toolbar_footprint.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_footprint.Realize()

		bSizer10.Add( self.toolbar_footprint, 1, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_footprints = wx.SearchCtrl( self.panel_up, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_footprints.ShowSearchButton( True )
		self.search_footprints.ShowCancelButton( False )
		self.search_footprints.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_footprints, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_footprints = wx.BitmapButton( self.panel_up, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE )

		self.button_refresh_footprints.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_footprints, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( bSizer61, 0, 0, 5 )


		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )


		bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.tree_footprints = wx.dataview.DataViewCtrl( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer7.Add( self.tree_footprints, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.panel_up.SetSizer( bSizer12 )
		self.panel_up.Layout()
		bSizer12.Fit( self.panel_up )
		self.panel_down = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_horz.SplitHorizontally( self.panel_up, self.panel_down, 449 )
		bSizer1.Add( self.splitter_horz, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_footprints = wx.Menu()
		self.menu_footprints_add = wx.MenuItem( self.menu_footprints, wx.ID_ANY, u"Add footprint", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_footprints.Append( self.menu_footprints_add )

		self.menu_footprints_edit = wx.MenuItem( self.menu_footprints, wx.ID_ANY, u"Edit footprint", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_footprints.Append( self.menu_footprints_edit )

		self.menu_footprints_delete = wx.MenuItem( self.menu_footprints, wx.ID_ANY, u"Delete footprint", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_footprints.Append( self.menu_footprints_delete )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelFootprintListOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_TOOL, self.onToggleFootprintPathClicked, id = self.toggle_footprint_path.GetId() )
		self.search_footprints.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchFootprintsButton )
		self.search_footprints.Bind( wx.EVT_TEXT_ENTER, self.onSearchFootprintsTextEnter )
		self.button_refresh_footprints.Bind( wx.EVT_BUTTON, self.onButtonRefreshFootprintsClick )
		self.Bind( wx.EVT_MENU, self.onMenuFootprintsAdd, id = self.menu_footprints_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuFootprintsEdit, id = self.menu_footprints_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuFootprintsDelete, id = self.menu_footprints_delete.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onToggleFootprintPathClicked( self, event ):
		event.Skip()

	def onSearchFootprintsButton( self, event ):
		event.Skip()

	def onSearchFootprintsTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshFootprintsClick( self, event ):
		event.Skip()

	def onMenuFootprintsAdd( self, event ):
		event.Skip()

	def onMenuFootprintsEdit( self, event ):
		event.Skip()

	def onMenuFootprintsDelete( self, event ):
		event.Skip()

	def splitter_horzOnIdle( self, event ):
		self.splitter_horz.SetSashPosition( 449 )
		self.splitter_horz.Unbind( wx.EVT_IDLE )

	def PanelFootprintListOnContextMenu( self, event ):
		self.PopupMenu( self.menu_footprints, event.GetPosition() )


