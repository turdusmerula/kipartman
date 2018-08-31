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
## Class PanelEditText
###########################################################################

class PanelEditText ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 427,442 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		radio_styleChoices = [ u"Normal", u"Italic" ]
		self.radio_style = wx.RadioBox( self, wx.ID_ANY, u"Style", wx.DefaultPosition, wx.DefaultSize, radio_styleChoices, 1, 0 )
		self.radio_style.SetSelection( 0 )
		bSizer1.Add( self.radio_style, 0, wx.ALL, 5 )
		
		radio_orientationChoices = [ u"Horizontal", u"Vertical" ]
		self.radio_orientation = wx.RadioBox( self, wx.ID_ANY, u"Orientation", wx.DefaultPosition, wx.DefaultSize, radio_orientationChoices, 1, 0 )
		self.radio_orientation.SetSelection( 0 )
		bSizer1.Add( self.radio_orientation, 0, wx.ALL, 5 )
		
		radio_displayChoices = [ u"Visible", u"Invisible" ]
		self.radio_display = wx.RadioBox( self, wx.ID_ANY, u"Display", wx.DefaultPosition, wx.DefaultSize, radio_displayChoices, 1, 0 )
		self.radio_display.SetSelection( 0 )
		bSizer1.Add( self.radio_display, 0, wx.ALL, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Text", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_text, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Pos X (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_pos_x = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_pos_x, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Pos Y (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_pos_y = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_pos_y, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Width (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_width = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_width, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Height (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_height = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_height, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		fgSizer1.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_thickness = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_thickness, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.radio_style.Bind( wx.EVT_RADIOBOX, self.onStyleRadioBox )
		self.radio_orientation.Bind( wx.EVT_RADIOBOX, self.onOrientationRadioBox )
		self.radio_display.Bind( wx.EVT_RADIOBOX, self.onDisplayRadioBox )
		self.text_text.Bind( wx.EVT_TEXT_ENTER, self.onTextTextEnter )
		self.text_pos_x.Bind( wx.EVT_TEXT_ENTER, self.onPosXTextEnter )
		self.text_pos_y.Bind( wx.EVT_TEXT_ENTER, self.onPosYTextEnter )
		self.text_width.Bind( wx.EVT_TEXT_ENTER, self.onWidthTextEnter )
		self.text_height.Bind( wx.EVT_TEXT_ENTER, self.onHeightTextEnter )
		self.text_thickness.Bind( wx.EVT_TEXT_ENTER, self.onThicknessTextEnter )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onStyleRadioBox( self, event ):
		event.Skip()
	
	def onOrientationRadioBox( self, event ):
		event.Skip()
	
	def onDisplayRadioBox( self, event ):
		event.Skip()
	
	def onTextTextEnter( self, event ):
		event.Skip()
	
	def onPosXTextEnter( self, event ):
		event.Skip()
	
	def onPosYTextEnter( self, event ):
		event.Skip()
	
	def onWidthTextEnter( self, event ):
		event.Skip()
	
	def onHeightTextEnter( self, event ):
		event.Skip()
	
	def onThicknessTextEnter( self, event ):
		event.Skip()
	

