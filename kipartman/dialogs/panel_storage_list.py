# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelStorageList
###########################################################################

class PanelStorageList ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_horz = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.splitter_horz.Bind( wx.EVT_IDLE, self.splitter_horzOnIdle )

		self.panel_storage_locations = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer25 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer25.Add( self.toolbar_filters, 0, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer112 = wx.BoxSizer( wx.HORIZONTAL )

		self.toolbar_storage = wx.ToolBar( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.toggle_storage_path = self.toolbar_storage.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/tree_mode.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, wx.EmptyString, wx.EmptyString, None )

		self.toolbar_storage.Realize()

		bSizer112.Add( self.toolbar_storage, 1, wx.EXPAND, 5 )

		bSizer611 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_storages = wx.SearchCtrl( self.panel_storage_locations, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_storages.ShowSearchButton( True )
		self.search_storages.ShowCancelButton( False )
		self.search_storages.SetMinSize( wx.Size( 200,-1 ) )

		bSizer611.Add( self.search_storages, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_storages = wx.BitmapButton( self.panel_storage_locations, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_storages.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer611.Add( self.button_refresh_storages, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer112.Add( bSizer611, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer7.Add( bSizer112, 0, wx.EXPAND, 5 )

		self.tree_storages = wx.dataview.DataViewCtrl( self.panel_storage_locations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer7.Add( self.tree_storages, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer25.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.panel_storage_locations.SetSizer( bSizer25 )
		self.panel_storage_locations.Layout()
		bSizer25.Fit( self.panel_storage_locations )
		self.menu_storage = wx.Menu()
		self.menu_storage_add_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Add new storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_add_storage.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_add_storage )

		self.menu_storage_edit_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Edit storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_edit_storage.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_edit_storage )

		self.menu_storage_remove_storage = wx.MenuItem( self.menu_storage, wx.ID_ANY, u"Remove storage", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_storage_remove_storage.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_storage.Append( self.menu_storage_remove_storage )

		self.panel_storage_locations.Bind( wx.EVT_RIGHT_DOWN, self.panel_storage_locationsOnContextMenu )

		self.panel_down = wx.Panel( self.splitter_horz, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_horz.SplitHorizontally( self.panel_storage_locations, self.panel_down, 455 )
		bSizer1.Add( self.splitter_horz, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_TOOL, self.onToggleStoragePathClicked, id = self.toggle_storage_path.GetId() )
		self.search_storages.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchStoragesCancel )
		self.search_storages.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchStoragesChanged )
		self.search_storages.Bind( wx.EVT_TEXT_ENTER, self.onSearchStoragesChanged )
		self.button_refresh_storages.Bind( wx.EVT_BUTTON, self.onButtonRefreshStoragesClick )
		self.Bind( wx.EVT_MENU, self.onMenuStorageAddStorage, id = self.menu_storage_add_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageEditStorage, id = self.menu_storage_edit_storage.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuStorageRemoveStorage, id = self.menu_storage_remove_storage.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onToggleStoragePathClicked( self, event ):
		event.Skip()

	def onSearchStoragesCancel( self, event ):
		event.Skip()

	def onSearchStoragesChanged( self, event ):
		event.Skip()


	def onButtonRefreshStoragesClick( self, event ):
		event.Skip()

	def onMenuStorageAddStorage( self, event ):
		event.Skip()

	def onMenuStorageEditStorage( self, event ):
		event.Skip()

	def onMenuStorageRemoveStorage( self, event ):
		event.Skip()

	def splitter_horzOnIdle( self, event ):
		self.splitter_horz.SetSashPosition( 455 )
		self.splitter_horz.Unbind( wx.EVT_IDLE )

	def panel_storage_locationsOnContextMenu( self, event ):
		self.panel_storage_locations.PopupMenu( self.menu_storage, event.GetPosition() )


