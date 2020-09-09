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
## Class PanelSymbolList
###########################################################################

class PanelSymbolList ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.toolbar_filters.SetMinSize( wx.Size( -1,31 ) )

		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer12.Add( self.toolbar_filters, 0, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.toolbar_symbol = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT )
		self.toolbar_symbol.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.toolbar_symbol.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.toggle_symbol_path = self.toolbar_symbol.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_symbol.AddSeparator()

		self.toggle_show_both_changes = self.toolbar_symbol.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_both.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toggle_show_conflict_changes = self.toolbar_symbol.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_conf.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toggle_show_incoming_changes = self.toolbar_symbol.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_in.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toggle_show_outgoing_changes = self.toolbar_symbol.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_out.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_symbol.Realize()

		bSizer10.Add( self.toolbar_symbol, 1, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_symbols = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_symbols.ShowSearchButton( True )
		self.search_symbols.ShowCancelButton( False )
		self.search_symbols.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_symbols, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_symbols = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE )

		self.button_refresh_symbols.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_symbols, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( bSizer61, 0, 0, 5 )


		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )


		bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.tree_symbols = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer7.Add( self.tree_symbols, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_symbols = wx.Menu()
		self.menu_symbols_update = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Update", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols_update.SetBitmap( wx.Bitmap( u"resources/update.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbols.Append( self.menu_symbols_update )

		self.menu_symbols_force_update = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Force update", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols_force_update.SetBitmap( wx.Bitmap( u"resources/update.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbols.Append( self.menu_symbols_force_update )

		self.menu_symbols.AppendSeparator()

		self.menu_symbols_commit = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Commit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols_commit.SetBitmap( wx.Bitmap( u"resources/commit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbols.Append( self.menu_symbols_commit )

		self.menu_symbols_force_commit = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Force commit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols_force_commit.SetBitmap( wx.Bitmap( u"resources/commit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbols.Append( self.menu_symbols_force_commit )

		self.menu_symbols.AppendSeparator()

		self.menu_symbols_add = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Add symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols.Append( self.menu_symbols_add )

		self.menu_symbols_edit = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Edit symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols.Append( self.menu_symbols_edit )

		self.menu_symbols_delete = wx.MenuItem( self.menu_symbols, wx.ID_ANY, u"Delete symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbols.Append( self.menu_symbols_delete )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelSymbolListOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_TOOL, self.onToggleSymbolPathClicked, id = self.toggle_symbol_path.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToggleShowBothChangesClicked, id = self.toggle_show_both_changes.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToggleShowConflictChangesClicked, id = self.toggle_show_conflict_changes.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToggleShowIncomingChangesClicked, id = self.toggle_show_incoming_changes.GetId() )
		self.Bind( wx.EVT_TOOL, self.onToggleShowOutgoingChangesClicked, id = self.toggle_show_outgoing_changes.GetId() )
		self.search_symbols.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchSymbolsButton )
		self.search_symbols.Bind( wx.EVT_TEXT_ENTER, self.onSearchSymbolsTextEnter )
		self.button_refresh_symbols.Bind( wx.EVT_BUTTON, self.onButtonRefreshSymbolsClick )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsUpdate, id = self.menu_symbols_update.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsForceUpdate, id = self.menu_symbols_force_update.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsCommit, id = self.menu_symbols_commit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsForceCommit, id = self.menu_symbols_force_commit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsAdd, id = self.menu_symbols_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsEdit, id = self.menu_symbols_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolsDelete, id = self.menu_symbols_delete.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onToggleSymbolPathClicked( self, event ):
		event.Skip()

	def onToggleShowBothChangesClicked( self, event ):
		event.Skip()

	def onToggleShowConflictChangesClicked( self, event ):
		event.Skip()

	def onToggleShowIncomingChangesClicked( self, event ):
		event.Skip()

	def onToggleShowOutgoingChangesClicked( self, event ):
		event.Skip()

	def onSearchSymbolsButton( self, event ):
		event.Skip()

	def onSearchSymbolsTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshSymbolsClick( self, event ):
		event.Skip()

	def onMenuSymbolsUpdate( self, event ):
		event.Skip()

	def onMenuSymbolsForceUpdate( self, event ):
		event.Skip()

	def onMenuSymbolsCommit( self, event ):
		event.Skip()

	def onMenuSymbolsForceCommit( self, event ):
		event.Skip()

	def onMenuSymbolsAdd( self, event ):
		event.Skip()

	def onMenuSymbolsEdit( self, event ):
		event.Skip()

	def onMenuSymbolsDelete( self, event ):
		event.Skip()

	def PanelSymbolListOnContextMenu( self, event ):
		self.PopupMenu( self.menu_symbols, event.GetPosition() )


