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
## Class PanelParameters
###########################################################################

class PanelParameters ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1616,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_vert = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.splitter_vert.Bind( wx.EVT_IDLE, self.splitter_vertOnIdle )
		self.splitter_vert.SetMinimumPaneSize( 300 )

		self.panel_parameter_list = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.toolbar_filters = wx.ToolBar( self.panel_parameter_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
		self.filters_label = wx.StaticText( self.toolbar_filters, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filters_label.Wrap( -1 )

		self.toolbar_filters.AddControl( self.filters_label )
		self.toolbar_filters.Realize()

		bSizer2.Add( self.toolbar_filters, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.search_parameters = wx.SearchCtrl( self.panel_parameter_list, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.search_parameters.ShowSearchButton( True )
		self.search_parameters.ShowCancelButton( True )
		self.search_parameters.SetMinSize( wx.Size( 200,-1 ) )

		bSizer61.Add( self.search_parameters, 0, wx.ALL|wx.EXPAND, 5 )

		self.button_refresh_parameters = wx.BitmapButton( self.panel_parameter_list, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0|wx.BORDER_NONE )

		self.button_refresh_parameters.SetBitmap( wx.Bitmap( u"resources/refresh.png", wx.BITMAP_TYPE_ANY ) )
		bSizer61.Add( self.button_refresh_parameters, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer61, 0, wx.ALIGN_RIGHT, 5 )

		self.tree_parameters = wx.dataview.DataViewCtrl( self.panel_parameter_list, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_MULTIPLE )
		bSizer2.Add( self.tree_parameters, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		self.panel_parameter_list.SetSizer( bSizer2 )
		self.panel_parameter_list.Layout()
		bSizer2.Fit( self.panel_parameter_list )
		self.menu_parameter = wx.Menu()
		self.menu_parameter_add = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Add parameter", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_add.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_add )

		self.menu_parameter_duplicate = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Duplicate parameter", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_duplicate.SetBitmap( wx.Bitmap( u"resources/add.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_duplicate )

		self.menu_parameter_edit = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Edit parameter", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_edit.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_edit )

		self.menu_parameter_remove = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Remove parameter(s)", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_remove.SetBitmap( wx.Bitmap( u"resources/remove.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_remove )

		self.menu_parameter_merge = wx.MenuItem( self.menu_parameter, wx.ID_ANY, u"Merge parameters", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parameter_merge.SetBitmap( wx.Bitmap( u"resources/edit.png", wx.BITMAP_TYPE_ANY ) )
		self.menu_parameter.Append( self.menu_parameter_merge )

		self.panel_parameter_list.Bind( wx.EVT_RIGHT_DOWN, self.panel_parameter_listOnContextMenu )

		self.panel_right = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_vert.SplitVertically( self.panel_parameter_list, self.panel_right, 1149 )
		bSizer1.Add( self.splitter_vert, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.search_parameters.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchParametersCancel )
		self.search_parameters.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearchParametersButton )
		self.search_parameters.Bind( wx.EVT_TEXT_ENTER, self.onSearchParametersTextEnter )
		self.button_refresh_parameters.Bind( wx.EVT_BUTTON, self.onButtonRefreshParametersClick )
		self.Bind( wx.EVT_MENU, self.onMenuParameterAdd, id = self.menu_parameter_add.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParameterDuplicate, id = self.menu_parameter_duplicate.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParameterEdit, id = self.menu_parameter_edit.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParameterRemove, id = self.menu_parameter_remove.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuParameterMerge, id = self.menu_parameter_merge.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onSearchParametersCancel( self, event ):
		event.Skip()

	def onSearchParametersButton( self, event ):
		event.Skip()

	def onSearchParametersTextEnter( self, event ):
		event.Skip()

	def onButtonRefreshParametersClick( self, event ):
		event.Skip()

	def onMenuParameterAdd( self, event ):
		event.Skip()

	def onMenuParameterDuplicate( self, event ):
		event.Skip()

	def onMenuParameterEdit( self, event ):
		event.Skip()

	def onMenuParameterRemove( self, event ):
		event.Skip()

	def onMenuParameterMerge( self, event ):
		event.Skip()

	def splitter_vertOnIdle( self, event ):
		self.splitter_vert.SetSashPosition( 1149 )
		self.splitter_vert.Unbind( wx.EVT_IDLE )

	def panel_parameter_listOnContextMenu( self, event ):
		self.panel_parameter_list.PopupMenu( self.menu_parameter, event.GetPosition() )


