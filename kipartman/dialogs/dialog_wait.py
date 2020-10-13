# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Sep 24 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogWait
###########################################################################

class DialogWait ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 205,191 ), style = wx.CAPTION|wx.FRAME_TOOL_WINDOW|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.wait_image = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"resources/wait.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.wait_image, 1, wx.ALL|wx.EXPAND, 5 )

		self.button_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.button_cancel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()
		self.timer_wait = wx.Timer()
		self.timer_wait.SetOwner( self, wx.ID_ANY )
		self.timer_wait.Start( 100 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.button_cancel.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.Bind( wx.EVT_TIMER, self.onWaitTimer, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		event.Skip()

	def onWaitTimer( self, event ):
		event.Skip()


