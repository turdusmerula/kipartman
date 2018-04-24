# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelSymbols
###########################################################################

class PanelSymbols ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 300 )
		
		self.panel_path = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_refresh_categories = wx.BitmapButton( self.panel_path, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.button_refresh_categories, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )
		
		self.tree_libraries = wx.dataview.DataViewCtrl( self.panel_path, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_libraries, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_path.SetSizer( bSizer2 )
		self.panel_path.Layout()
		bSizer2.Fit( self.panel_path )
		self.menu_libraries = wx.Menu()
		self.menu_libraries_add_folder = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Add folder", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries.Append( self.menu_libraries_add_folder )
		
		self.menu_libraries_add_library = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Add library", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries.Append( self.menu_libraries_add_library )
		
		self.menu_libraries_rename = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Rename", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries.Append( self.menu_libraries_rename )
		
		self.menu_libraries_remove = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Remove", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries.Append( self.menu_libraries_remove )
		
		self.menu_libraries.AppendSeparator()
		
		self.menu_libraries_add_symbol = wx.MenuItem( self.menu_libraries, wx.ID_ANY, u"Add symbol", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_libraries.Append( self.menu_libraries_add_symbol )
		
		self.panel_path.Bind( wx.EVT_RIGHT_DOWN, self.panel_pathOnContextMenu ) 
		
		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.symbol_splitter = wx.SplitterWindow( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.symbol_splitter.Bind( wx.EVT_IDLE, self.symbol_splitterOnIdle )
		
		self.panel_symbols = wx.Panel( self.symbol_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.filters_panel = wx.Panel( self.panel_symbols, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer161 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self.filters_panel, wx.ID_ANY, u"Filters: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		bSizer161.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		
		self.filters_panel.SetSizer( bSizer161 )
		self.filters_panel.Layout()
		bSizer161.Fit( self.filters_panel )
		bSizer12.Add( self.filters_panel, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.toolbar_symbol = wx.ToolBar( self.panel_symbols, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT ) 
		self.toolbar_symbol.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.toolbar_symbol.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		self.toggle_symbol_path = self.toolbar_symbol.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar_symbol.AddSeparator()
		
		self.toggle_show_both_changes = self.toolbar_symbol.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_both.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_conflict_changes = self.toolbar_symbol.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_conf.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_incoming_changes = self.toolbar_symbol.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_in.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toggle_show_outgoing_changes = self.toolbar_symbol.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/show_out.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None ) 
		
		self.toolbar_symbol.Realize() 
		
		bSizer10.Add( self.toolbar_symbol, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.search_symbols = wx.SearchCtrl( self.panel_symbols, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_symbols.ShowSearchButton( True )
		self.search_symbols.ShowCancelButton( False )
		self.search_symbols.SetMinSize( wx.Size( 200,-1 ) )
		
		bSizer61.Add( self.search_symbols, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.button_refresh_symbols = wx.BitmapButton( self.panel_symbols, wx.ID_ANY, wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer61.Add( self.button_refresh_symbols, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer61, 0, 0, 5 )
		
		
		bSizer11.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.tree_symbols = wx.dataview.DataViewCtrl( self.panel_symbols, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer7.Add( self.tree_symbols, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer12.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.panel_symbols.SetSizer( bSizer12 )
		self.panel_symbols.Layout()
		bSizer12.Fit( self.panel_symbols )
		self.symbol_splitter.Initialize( self.panel_symbols )
		bSizer3.Add( self.symbol_splitter, 1, wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer3 )
		self.m_panel3.Layout()
		bSizer3.Fit( self.m_panel3 )
		self.m_splitter2.SplitVertically( self.panel_path, self.m_panel3, 294 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
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
		
		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelSymbolsOnContextMenu ) 
		
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_refresh_categories.Bind( wx.EVT_BUTTON, self.onButtonRefreshCategoriesClick )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesAddFolder, id = self.menu_libraries_add_folder.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesAddLibrary, id = self.menu_libraries_add_library.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesRename, id = self.menu_libraries_rename.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesRemove, id = self.menu_libraries_remove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuLibrariesAddSymbol, id = self.menu_libraries_add_symbol.GetId() )
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
	
	def onButtonRefreshCategoriesClick( self, event ):
		event.Skip()
	
	def onMenuLibrariesAddFolder( self, event ):
		event.Skip()
	
	def onMenuLibrariesAddLibrary( self, event ):
		event.Skip()
	
	def onMenuLibrariesRename( self, event ):
		event.Skip()
	
	def onMenuLibrariesRemove( self, event ):
		event.Skip()
	
	def onMenuLibrariesAddSymbol( self, event ):
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
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	
	def panel_pathOnContextMenu( self, event ):
		self.panel_path.PopupMenu( self.menu_libraries, event.GetPosition() )
		
	def symbol_splitterOnIdle( self, event ):
		self.symbol_splitter.SetSashPosition( 455 )
		self.symbol_splitter.Unbind( wx.EVT_IDLE )
	
	def PanelSymbolsOnContextMenu( self, event ):
		self.PopupMenu( self.menu_symbols, event.GetPosition() )
		

