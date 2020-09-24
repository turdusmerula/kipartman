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

		self.toolbar_symbol = wx.ToolBar( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT )
		self.toolbar_symbol.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.toolbar_symbol.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.toggle_symbol_path = self.toolbar_symbol.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_symbol.Realize()

		bSizer10.Add( self.toolbar_symbol, 1, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_symbols = wx.SearchCtrl( self.panel_up, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_symbols.ShowSearchButton( True )
		self.search_symbols.ShowCancelButton( False )
		self.search_symbols.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_symbols, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_symbols = wx.BitmapButton( self.panel_up, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE )

		self.button_refresh_symbols.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_symbols, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( bSizer61, 0, 0, 5 )


		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )


		bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.tree_symbols = wx.dataview.DataViewCtrl( self.panel_up, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer7.Add( self.tree_symbols, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.panel_up.SetSizer( bSizer12 )
		self.panel_up.Layout()
		bSizer12.Fit( self.panel_up )
		self.panel_down = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_horz.SplitHorizontally( self.panel_up, self.panel_down, 449 )
		bSizer1.Add( self.splitter_horz, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_symbol = wx.Menu()
		self.menu_symbol_add = wx.MenuItem( self.menu_symbol, wx.ID_ANY, u"Add symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbol_add.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbol.Append( self.menu_symbol_add )

		self.menu_symbol_duplicate = wx.MenuItem( self.menu_symbol, wx.ID_ANY, u"Duplicate symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbol_duplicate.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbol.Append( self.menu_symbol_duplicate )

		self.menu_symbol_edit = wx.MenuItem( self.menu_symbol, wx.ID_ANY, u"Edit symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbol_edit.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbol.Append( self.menu_symbol_edit )

		self.menu_symbol_remove = wx.MenuItem( self.menu_symbol, wx.ID_ANY, u"Remove symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_symbol_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_symbol.Append( self.menu_symbol_remove )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelSymbolListOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_TOOL, self.onToggleSymbolPathClicked, id = self.toggle_symbol_path.GetId() )
		self.search_symbols.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchSymbolsCancel )
		self.search_symbols.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchSymbolsButton )
		self.search_symbols.Bind( wx.EVT_TEXT_ENTER, self.onSearchSymbolsTextEnter )
		self.button_refresh_symbols.Bind( wx.EVT_BUTTON, self.onButtonRefreshSymbolsClick )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolAdd, id = self.menu_symbol_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolDuplicate, id = self.menu_symbol_duplicate.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolEdit, id = self.menu_symbol_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuSymbolRemove, id = self.menu_symbol_remove.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onToggleSymbolPathClicked( self, event ):
		event.Skip()

	def onSearchSymbolsCancel( self, event ):
		event.Skip()

	def onSearchSymbolsButton( self, event ):
		event.Skip()

	def onSearchSymbolsTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshSymbolsClick( self, event ):
		event.Skip()

	def onMenuSymbolAdd( self, event ):
		event.Skip()

	def onMenuSymbolDuplicate( self, event ):
		event.Skip()

	def onMenuSymbolEdit( self, event ):
		event.Skip()

	def onMenuSymbolRemove( self, event ):
		event.Skip()

	def splitter_horzOnIdle( self, event ):
		self.splitter_horz.SetSashPosition( 449 )
		self.splitter_horz.Unbind( wx.EVT_IDLE )

	def PanelSymbolListOnContextMenu( self, event ):
		self.PopupMenu( self.menu_symbol, event.GetPosition() )


