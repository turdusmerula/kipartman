# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jul 12 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogEditAttachement
###########################################################################

class DialogEditAttachement ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 427,187 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer2.Add( self.m_staticText1, 1, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_open_file = wx.Button( self, wx.ID_ANY, u"<None>", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT|wx.NO_BORDER )
		bSizer17.Add( self.button_open_file, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.button_add_file = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap( u"resources/browse-16x16.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer17.Add( self.button_add_file, 0, wx.ALL, 5 )
		
		
		fgSizer2.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_description = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.text_description, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_validate = wx.Button( self, wx.ID_OK, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_validate.SetDefault() 
		bSizer2.Add( self.button_validate, 0, wx.ALL, 5 )
		
		self.button_cancel = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_cancel, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer4.Add( bSizer1, 0, wx.EXPAND|wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.button_open_file.Bind( wx.EVT_BUTTON, self.onButtonOpenFileClick )
		self.button_add_file.Bind( wx.EVT_BUTTON, self.onButtonAddFileClick )
		self.button_validate.Bind( wx.EVT_BUTTON, self.onValidateClick )
		self.button_cancel.Bind( wx.EVT_BUTTON, self.onCancelClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onButtonOpenFileClick( self, event ):
		event.Skip()
	
	def onButtonAddFileClick( self, event ):
		event.Skip()
	
	def onValidateClick( self, event ):
		event.Skip()
	
	def onCancelClick( self, event ):
		event.Skip()
	

