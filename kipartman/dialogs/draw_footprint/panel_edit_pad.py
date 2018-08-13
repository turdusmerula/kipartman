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
## Class PanelEditPad
###########################################################################

class PanelEditPad ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 401,360 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		radio_shapeChoices = [ u"Rectangle", u"Oval" ]
		self.radio_shape = wx.RadioBox( self, wx.ID_ANY, u"Shape", wx.DefaultPosition, wx.DefaultSize, radio_shapeChoices, 1, 0 )
		self.radio_shape.SetSelection( 0 )
		bSizer7.Add( self.radio_shape, 0, wx.ALL|wx.EXPAND, 5 )
		
		radio_typeChoices = [ u"SMD", u"Thru hole" ]
		self.radio_type = wx.RadioBox( self, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, radio_typeChoices, 1, 0 )
		self.radio_type.SetSelection( 0 )
		bSizer7.Add( self.radio_type, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Pad", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_name = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_name, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Position X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_position_x = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_position_x, 0, wx.ALL, 5 )
		
		self.m_staticText63 = wx.StaticText( self, wx.ID_ANY, u"Position Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )
		fgSizer1.Add( self.m_staticText63, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_size_x11 = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_size_x11, 0, wx.ALL, 5 )
		
		self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"Size X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		fgSizer1.Add( self.m_staticText62, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_size_x = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_size_x, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"Size Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		fgSizer1.Add( self.m_staticText61, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_size_y = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.text_size_y, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.radio_shape.Bind( wx.EVT_RADIOBOX, self.onRadioShapeRadioBox )
		self.radio_type.Bind( wx.EVT_RADIOBOX, self.onRadioTypeRadioBox )
		self.text_name.Bind( wx.EVT_TEXT, self.onPadText )
		self.text_position_x.Bind( wx.EVT_TEXT, self.onPositionXText )
		self.text_size_x11.Bind( wx.EVT_TEXT, self.onPositionYText )
		self.text_size_x.Bind( wx.EVT_TEXT, self.onSizeXText )
		self.text_size_y.Bind( wx.EVT_TEXT, self.onSizeYText )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onRadioShapeRadioBox( self, event ):
		event.Skip()
	
	def onRadioTypeRadioBox( self, event ):
		event.Skip()
	
	def onPadText( self, event ):
		event.Skip()
	
	def onPositionXText( self, event ):
		event.Skip()
	
	def onPositionYText( self, event ):
		event.Skip()
	
	def onSizeXText( self, event ):
		event.Skip()
	
	def onSizeYText( self, event ):
		event.Skip()
	

