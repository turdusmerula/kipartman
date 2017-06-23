# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 29 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogEditCategory
###########################################################################

class DialogEditCategory ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 308,130 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		#self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Category:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer1.Add( self.m_staticText1, 0, wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )
		
		self.text_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.text_name, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_validate = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_validate.SetDefault() 
		bSizer2.Add( self.button_validate, 0, wx.ALL, 5 )
		
		self.button_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_cancel, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_validate.Bind( wx.EVT_BUTTON, self.onValidateClick )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.onCancelClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onValidateClick( self, event ):
		event.Skip()
	
	def onCancelClick( self, event ):
		event.Skip()
	

