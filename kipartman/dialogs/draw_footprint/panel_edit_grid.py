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
## Class PanelEditGrid
###########################################################################

class PanelEditGrid ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 401,237 ), style = wx.TAB_TRAVERSAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"X count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spin_x_count = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 9999, 10 )
		fgSizer1.Add( self.spin_x_count, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Y count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.spin_y_count = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 9999, 10 )
		fgSizer1.Add( self.spin_y_count, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Spacing X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_spacing_x = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_spacing_x, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Spacing Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_spacing_y = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_spacing_y, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		# Connect Events
		self.spin_x_count.Bind( wx.EVT_SPINCTRL, self.onSpinXCountCtrl )
		self.spin_y_count.Bind( wx.EVT_SPINCTRL, self.onSpinYCountCtrl )
		self.text_spacing_x.Bind( wx.EVT_TEXT, self.onTextSpacingXText )
		self.text_spacing_y.Bind( wx.EVT_TEXT, self.onTextSpacingYText )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onSpinXCountCtrl( self, event ):
		event.Skip()
	
	def onSpinYCountCtrl( self, event ):
		event.Skip()
	
	def onTextSpacingXText( self, event ):
		event.Skip()
	
	def onTextSpacingYText( self, event ):
		event.Skip()
	

