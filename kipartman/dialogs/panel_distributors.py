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
## Class PanelDistributors
###########################################################################

class PanelDistributors ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_vert = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.splitter_vert.Bind( wx.EVT_IDLE, self.splitter_vertOnIdle )
		self.splitter_vert.SetMinimumPaneSize( 300 )

		self.panel_distributor_list = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_distributor_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer2.Add( self.toolbar_filters, 0, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_distributors = wx.SearchCtrl( self.panel_distributor_list, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_distributors.ShowSearchButton( True )
		self.search_distributors.ShowCancelButton( False )
		self.search_distributors.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_distributors, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_distributors = wx.BitmapButton( self.panel_distributor_list, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_distributors.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_distributors, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer61, 0, wx.EXPAND, 5 )

		self.tree_distributors = wx.dataview.DataViewCtrl( self.panel_distributor_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.tree_distributors, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_distributor_list.SetSizer( bSizer2 )
		self.panel_distributor_list.Layout()
		bSizer2.Fit( self.panel_distributor_list )
		self.panel_right = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_vert.SplitVertically( self.panel_distributor_list, self.panel_right, 500 )
		bSizer1.Add( self.splitter_vert, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_distributor = wx.Menu()
		self.menu_distributor_add = wx.MenuItem( self.menu_distributor, wx.ID_ANY, u"Add distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_add.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributor.Append( self.menu_distributor_add )

		self.menu_distributor_duplicate = wx.MenuItem( self.menu_distributor, wx.ID_ANY, u"Duplicate distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_duplicate.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributor.Append( self.menu_distributor_duplicate )

		self.menu_distributor_edit = wx.MenuItem( self.menu_distributor, wx.ID_ANY, u"Edit distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_edit.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributor.Append( self.menu_distributor_edit )

		self.menu_distributor_remove = wx.MenuItem( self.menu_distributor, wx.ID_ANY, u"Remove distributor", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_distributor_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_distributor.Append( self.menu_distributor_remove )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelDistributorsOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.search_distributors.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchDistributorsCancel )
		self.search_distributors.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchDistributorsButton )
		self.search_distributors.Bind( wx.EVT_TEXT_ENTER, self.onSearchDistributorsTextEnter )
		self.button_refresh_distributors.Bind( wx.EVT_BUTTON, self.onButtonRefreshDistributorsClick )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorAdd, id = self.menu_distributor_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorDuplicate, id = self.menu_distributor_duplicate.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorEdit, id = self.menu_distributor_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuDistributorRemove, id = self.menu_distributor_remove.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onSearchDistributorsCancel( self, event ):
		event.Skip()

	def onSearchDistributorsButton( self, event ):
		event.Skip()

	def onSearchDistributorsTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshDistributorsClick( self, event ):
		event.Skip()

	def onMenuDistributorAdd( self, event ):
		event.Skip()

	def onMenuDistributorDuplicate( self, event ):
		event.Skip()

	def onMenuDistributorEdit( self, event ):
		event.Skip()

	def onMenuDistributorRemove( self, event ):
		event.Skip()

	def splitter_vertOnIdle( self, event ):
		self.splitter_vert.SetSashPosition( 500 )
		self.splitter_vert.Unbind( wx.EVT_IDLE )

	def PanelDistributorsOnContextMenu( self, event ):
		self.PopupMenu( self.menu_distributor, event.GetPosition() )


