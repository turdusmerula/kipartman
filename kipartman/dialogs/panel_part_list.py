# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  1 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelPartList
###########################################################################

class PanelPartList ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1467,802 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_horz = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_LIVE_UPDATE )
		self.splitter_horz.Bind( wx.EVT_IDLE, self.splitter_horzOnIdle )
		self.splitter_horz.SetMinimumPaneSize( 100 )

		self.panel_up = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.sizer_part = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		self.sizer_part.Add( self.toolbar_filters, 0, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.toolbar_part = wx.ToolBar( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.toggle_part_path = self.toolbar_part.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_part.Realize()

		bSizer11.Add( self.toolbar_part, 1, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_parts = wx.SearchCtrl( self.panel_up, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_parts.ShowSearchButton( True )
		self.search_parts.ShowCancelButton( False )
		self.search_parts.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_parts, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_parts = wx.BitmapButton( self.panel_up, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_parts.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_parts, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer11.Add( bSizer61, 0, 0, 5 )


		self.sizer_part.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.tree_parts = wx.dataview.DataViewCtrl( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sizer_part.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_up.SetSizer( self.sizer_part )
		self.panel_up.Layout()
		self.sizer_part.Fit( self.panel_up )
		self.panel_down = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_horz.SplitHorizontally( self.panel_up, self.panel_down, 600 )
		bSizer1.Add( self.splitter_horz, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_part = wx.Menu()
		self.menu_part_add_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Add new part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_add_part.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_add_part )

		self.menu_part_duplicate_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Duplicate part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_duplicate_part.SetBitmap( wx.Bitmap( u"resources/duplicate.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_duplicate_part )

		self.menu_part_edit_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Edit part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_edit_part.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_edit_part )

		self.menu_part_remove_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Remove part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_remove_part.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_remove_part )

		self.menu_part.AppendSeparator()

		self.menu_part_append_equivalent = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Append equivalent part", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_part_append_equivalent.SetBitmap( wx.Bitmap( u"resources/duplicate.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_part.Append( self.menu_part_append_equivalent )

		self.menu_part.AppendSeparator()

		self.menu_refresh_octopart_part = wx.MenuItem( self.menu_part, wx.ID_ANY, u"Refresh part from octopart", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_refresh_octopart_part.SetBitmap( wx.NullBitmap )
		self.menu_part.Append( self.menu_refresh_octopart_part )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartListOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_TOOL, self.onToggleCategoryPathClicked, id = self.toggle_part_path.GetId() )
		self.search_parts.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchPartsButton )
		self.search_parts.Bind( wx.EVT_TEXT_ENTER, self.onSearchPartsTextEnter )
		self.button_refresh_parts.Bind( wx.EVT_BUTTON, self.onButtonRefreshPartsClick )
		self.Bind( wx.EVT_MENU, self.onMenuPartAddPart, id = self.menu_part_add_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartDuplicatePart, id = self.menu_part_duplicate_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartEditPart, id = self.menu_part_edit_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartRemovePart, id = self.menu_part_remove_part.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartAppendEquivalentPart, id = self.menu_part_append_equivalent.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuPartRefreshOctopartPart, id = self.menu_refresh_octopart_part.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onToggleCategoryPathClicked( self, event ):
		event.Skip()

	def onSearchPartsButton( self, event ):
		event.Skip()

	def onSearchPartsTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshPartsClick( self, event ):
		event.Skip()

	def onMenuPartAddPart( self, event ):
		event.Skip()

	def onMenuPartDuplicatePart( self, event ):
		event.Skip()

	def onMenuPartEditPart( self, event ):
		event.Skip()

	def onMenuPartRemovePart( self, event ):
		event.Skip()

	def onMenuPartAppendEquivalentPart( self, event ):
		event.Skip()

	def onMenuPartRefreshOctopartPart( self, event ):
		event.Skip()

	def splitter_horzOnIdle( self, event ):
		self.splitter_horz.SetSashPosition( 600 )
		self.splitter_horz.Unbind( wx.EVT_IDLE )

	def PanelPartListOnContextMenu( self, event ):
		self.PopupMenu( self.menu_part, event.GetPosition() )


