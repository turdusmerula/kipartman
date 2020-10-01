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
## Class PanelPartAttachements
###########################################################################

class PanelPartAttachements ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 496,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer12.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.tree_attachements = wx.dataview.DataViewCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.tree_attachements, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.context_menu = wx.Menu()
		self.context_menu_open = wx.MenuItem( self.context_menu, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.context_menu.Append( self.context_menu_open )



		# Connect Events
		self.Bind( wx.EVT_MENU, self.onContextMenuOpenSelection, id = self.context_menu_open.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onContextMenuOpenSelection( self, event ):
		event.Skip()


