# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov 13 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelPartEcadData
###########################################################################

class PanelPartEcadData ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 759,345 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"SCHEMATIC SYMBOL", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText1.Wrap( -1 )
		bSizer12.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap1.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.m_bitmap1.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer12.Add( self.m_bitmap1, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"PCB FOOTPRINT", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText11.Wrap( -1 )
		bSizer5.Add( self.m_staticText11, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap2.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.m_bitmap2.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer5.Add( self.m_bitmap2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"3D Footprint", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText12.Wrap( -1 )
		bSizer6.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.m_bitmap3 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap3.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.m_bitmap3.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer6.Add( self.m_bitmap3, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
	
	def __del__( self ):
		pass
	

