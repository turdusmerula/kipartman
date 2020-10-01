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
## Class PanelManufacturers
###########################################################################

class PanelManufacturers ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_vert = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.splitter_vert.Bind( wx.EVT_IDLE, self.splitter_vertOnIdle )
		self.splitter_vert.SetMinimumPaneSize( 300 )

		self.panel_manufacturers = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_manufacturers, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer2.Add( self.toolbar_filters, 0, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_manufacturers = wx.SearchCtrl( self.panel_manufacturers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_manufacturers.ShowSearchButton( True )
		self.search_manufacturers.ShowCancelButton( False )
		self.search_manufacturers.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_manufacturers, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_manufacturers = wx.BitmapButton( self.panel_manufacturers, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_manufacturers.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_manufacturers, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer61, 0, wx.EXPAND, 5 )

		self.tree_manufacturers = wx.dataview.DataViewCtrl( self.panel_manufacturers, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tree_manufacturers, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_manufacturers.SetSizer( bSizer2 )
		self.panel_manufacturers.Layout()
		bSizer2.Fit( self.panel_manufacturers )
		self.panel_right = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_vert.SplitVertically( self.panel_manufacturers, self.panel_right, 540 )
		bSizer1.Add( self.splitter_vert, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_manufacturer = wx.Menu()
		self.menu_manufacturer_add = wx.MenuItem( self.menu_manufacturer, wx.ID_ANY, u"Add manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_add.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturer.Append( self.menu_manufacturer_add )

		self.menu_manufacturer_duplicate = wx.MenuItem( self.menu_manufacturer, wx.ID_ANY, u"Duplicate manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_duplicate.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturer.Append( self.menu_manufacturer_duplicate )

		self.menu_manufacturer_edit = wx.MenuItem( self.menu_manufacturer, wx.ID_ANY, u"Edit manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_edit.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturer.Append( self.menu_manufacturer_edit )

		self.menu_manufacturer_remove = wx.MenuItem( self.menu_manufacturer, wx.ID_ANY, u"Remove manufacturer", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_manufacturer_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_manufacturer.Append( self.menu_manufacturer_remove )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelManufacturersOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.search_manufacturers.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchManufacturersCancel )
		self.search_manufacturers.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchManufacturersButton )
		self.search_manufacturers.Bind( wx.EVT_TEXT_ENTER, self.onSearchManufacturersTextEnter )
		self.button_refresh_manufacturers.Bind( wx.EVT_BUTTON, self.onButtonRefreshManufacturersClick )
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerAdd, id = self.menu_manufacturer_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerDuplicate, id = self.menu_manufacturer_duplicate.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerEdit, id = self.menu_manufacturer_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuManufacturerRemove, id = self.menu_manufacturer_remove.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onSearchManufacturersCancel( self, event ):
		event.Skip()

	def onSearchManufacturersButton( self, event ):
		event.Skip()

	def onSearchManufacturersTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshManufacturersClick( self, event ):
		event.Skip()

	def onMenuManufacturerAdd( self, event ):
		event.Skip()

	def onMenuManufacturerDuplicate( self, event ):
		event.Skip()

	def onMenuManufacturerEdit( self, event ):
		event.Skip()

	def onMenuManufacturerRemove( self, event ):
		event.Skip()

	def splitter_vertOnIdle( self, event ):
		self.splitter_vert.SetSashPosition( 540 )
		self.splitter_vert.Unbind( wx.EVT_IDLE )

	def PanelManufacturersOnContextMenu( self, event ):
		self.PopupMenu( self.menu_manufacturer, event.GetPosition() )


