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
## Class PanelUnits
###########################################################################

class PanelUnits ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1616,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_vert = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.splitter_vert.Bind( wx.EVT_IDLE, self.splitter_vertOnIdle )
		self.splitter_vert.SetMinimumPaneSize( 300 )

		self.panel_unit_list = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_unit_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer2.Add( self.toolbar_filters, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_units = wx.SearchCtrl( self.panel_unit_list, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_units.ShowSearchButton( True )
		self.search_units.ShowCancelButton( True )
		self.search_units.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_units, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_units = wx.BitmapButton( self.panel_unit_list, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_units.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_units, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer61, 0, wx.ALIGN_RIGHT, 5 )

		self.tree_units = wx.dataview.DataViewCtrl( self.panel_unit_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_SINGLE )
		bSizer2.Add( self.tree_units, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		self.panel_unit_list.SetSizer( bSizer2 )
		self.panel_unit_list.Layout()
		bSizer2.Fit( self.panel_unit_list )
		self.menu_unit = wx.Menu()
		self.menu_unit_add = wx.MenuItem( self.menu_unit, wx.ID_ANY, u"Add unit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_unit_add.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_unit.Append( self.menu_unit_add )

		self.menu_unit_duplicate = wx.MenuItem( self.menu_unit, wx.ID_ANY, u"Duplicate unit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_unit_duplicate.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_unit.Append( self.menu_unit_duplicate )

		self.menu_unit_edit = wx.MenuItem( self.menu_unit, wx.ID_ANY, u"Edit unit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_unit_edit.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_unit.Append( self.menu_unit_edit )

		self.menu_unit_remove = wx.MenuItem( self.menu_unit, wx.ID_ANY, u"Remove unit", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_unit_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_unit.Append( self.menu_unit_remove )

		self.panel_unit_list.Bind( wx.EVT_RIGHT_DOWN, self.panel_unit_listOnContextMenu )

		self.panel_right = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_vert.SplitVertically( self.panel_unit_list, self.panel_right, 1149 )
		bSizer1.Add( self.splitter_vert, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.search_units.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchUnitsCancel )
		self.search_units.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchUnitsEnter )
		self.search_units.Bind( wx.EVT_TEXT_ENTER, self.onSearchUnitsEnter )
		self.button_refresh_units.Bind( wx.EVT_BUTTON, self.onButtonRefreshParametersClick )
		self.Bind( wx.EVT_MENU, self.onMenuUnitAdd, id = self.menu_unit_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuUnitDuplicate, id = self.menu_unit_duplicate.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuUnitEdit, id = self.menu_unit_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuUnitRemove, id = self.menu_unit_remove.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onSearchUnitsCancel( self, event ):
		event.Skip()

	def onSearchUnitsEnter( self, event ):
		event.Skip()


	def onButtonRefreshParametersClick( self, event ):
		event.Skip()

	def onMenuUnitAdd( self, event ):
		event.Skip()

	def onMenuUnitDuplicate( self, event ):
		event.Skip()

	def onMenuUnitEdit( self, event ):
		event.Skip()

	def onMenuUnitRemove( self, event ):
		event.Skip()

	def splitter_vertOnIdle( self, event ):
		self.splitter_vert.SetSashPosition( 1149 )
		self.splitter_vert.Unbind( wx.EVT_IDLE )

	def panel_unit_listOnContextMenu( self, event ):
		self.panel_unit_list.PopupMenu( self.menu_unit, event.GetPosition() )


