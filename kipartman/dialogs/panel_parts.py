# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep  2 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelParts
###########################################################################

class PanelParts ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 848,489 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_vert = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_LIVE_UPDATE )
		self.splitter_vert.Bind( wx.EVT_IDLE, self.splitter_vertOnIdle )
		self.splitter_vert.SetMinimumPaneSize( 100 )

		self.panel_left = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel_right = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_vert.SplitVertically( self.panel_left, self.panel_right, 449 )
		bSizer1.Add( self.splitter_vert, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.menu_parts = wx.Menu()
		self.menu_parts_refresh_octopart = wx.MenuItem( self.menu_parts, wx.ID_ANY, u"Refresh octopart parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parts.Append( self.menu_parts_refresh_octopart )

		self.menu_parts.AppendSeparator()

		self.menu_parts_import_parts = wx.MenuItem( self.menu_parts, wx.ID_ANY, u"Import parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parts.Append( self.menu_parts_import_parts )

		self.menu_parts_export_parts = wx.MenuItem( self.menu_parts, wx.ID_ANY, u"Export parts", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu_parts.Append( self.menu_parts_export_parts )

		self.Bind( wx.EVT_RIGHT_DOWN, self.PanelPartsOnContextMenu )


		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.Bind( wx.EVT_MENU, self.onMenuItemPartsRefreshOctopart, id = self.menu_parts_refresh_octopart.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPartsImportParts, id = self.menu_parts_import_parts.GetId() )
		self.Bind( wx.EVT_MENU, self.onMenuItemPartsExportParts, id = self.menu_parts_export_parts.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def onMenuItemPartsRefreshOctopart( self, event ):
		event.Skip()

	def onMenuItemPartsImportParts( self, event ):
		event.Skip()

	def onMenuItemPartsExportParts( self, event ):
		event.Skip()

	def splitter_vertOnIdle( self, event ):
		self.splitter_vert.SetSashPosition( 449 )
		self.splitter_vert.Unbind( wx.EVT_IDLE )

	def PanelPartsOnContextMenu( self, event ):
		self.PopupMenu( self.menu_parts, event.GetPosition() )


