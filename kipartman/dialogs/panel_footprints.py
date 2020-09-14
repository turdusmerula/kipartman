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
## Class PanelFootprints
###########################################################################

class PanelFootprints ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1086,756 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.splitter_vert = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.splitter_vert.Bind( wx.EVT_IDLE, self.splitter_vertOnIdle )
		self.splitter_vert.SetMinimumPaneSize( 300 )

		self.panel_left = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel_right = wx.Panel( self.splitter_vert, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.splitter_vert.SplitVertically( self.panel_left, self.panel_right, 294 )
		bSizer1.Add( self.splitter_vert, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()

	def splitter_vertOnIdle( self, event ):
		self.splitter_vert.SetSashPosition( 294 )
		self.splitter_vert.Unbind( wx.EVT_IDLE )


