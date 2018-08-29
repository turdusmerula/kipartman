# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 22 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelEditFootprint
###########################################################################

class PanelEditFootprint ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 401,237 ), style = wx.TAB_TRAVERSAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_name, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Timestamp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_timestamp = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_timestamp, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText511 = wx.StaticText( self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )
		fgSizer1.Add( self.m_staticText511, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_descr = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_descr, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText5111 = wx.StaticText( self, wx.ID_ANY, u"Tags", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_tags = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_tags, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		# Connect Events
		self.text_name.Bind( wx.EVT_TEXT_ENTER, self.onNameTextEnter )
		self.text_timestamp.Bind( wx.EVT_TEXT_ENTER, self.onTimestampTextEnter )
		self.text_descr.Bind( wx.EVT_TEXT_ENTER, self.onDescrTextEnter )
		self.text_tags.Bind( wx.EVT_TEXT_ENTER, self.onTagsTextEnter )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onNameTextEnter( self, event ):
		event.Skip()
	
	def onTimestampTextEnter( self, event ):
		event.Skip()
	
	def onDescrTextEnter( self, event ):
		event.Skip()
	
	def onTagsTextEnter( self, event ):
		event.Skip()
	

