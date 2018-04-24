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
## Class PanelPartPreviewData
###########################################################################

class PanelPartPreviewData ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 759,345 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Symbol", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText1.Wrap( -1 )
		bSizer12.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.panel_image_symbol = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )
		
		self.image_symbol = wx.StaticBitmap( self.panel_image_symbol, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.image_symbol.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.image_symbol.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer51.Add( self.image_symbol, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_image_symbol.SetSizer( bSizer51 )
		self.panel_image_symbol.Layout()
		bSizer51.Fit( self.panel_image_symbol )
		bSizer12.Add( self.panel_image_symbol, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Footprint", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText11.Wrap( -1 )
		bSizer5.Add( self.m_staticText11, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.panel_image_footprint = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		self.image_footprint = wx.StaticBitmap( self.panel_image_footprint, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.image_footprint.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.image_footprint.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer61.Add( self.image_footprint, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_image_footprint.SetSizer( bSizer61 )
		self.panel_image_footprint.Layout()
		bSizer61.Fit( self.panel_image_footprint )
		bSizer5.Add( self.panel_image_footprint, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"3D Model", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText12.Wrap( -1 )
		bSizer6.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.panel_image_3d_model = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.image_3d_model = wx.StaticBitmap( self.panel_image_3d_model, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.image_3d_model.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.image_3d_model.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer7.Add( self.image_3d_model, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_image_3d_model.SetSizer( bSizer7 )
		self.panel_image_3d_model.Layout()
		bSizer7.Fit( self.panel_image_3d_model )
		bSizer6.Add( self.panel_image_3d_model, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
	
	def __del__( self ):
		pass
	

