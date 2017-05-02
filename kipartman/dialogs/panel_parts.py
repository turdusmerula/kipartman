# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 29 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class PanelParts
###########################################################################

class PanelParts ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 785,587 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		
		self.m_panel2 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bpButton1 = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.m_bpButton1, 0, wx.ALL, 5 )
		
		self.m_bpButton2 = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.m_bpButton2, 0, wx.ALL, 5 )
		
		self.m_bpButton3 = wx.BitmapButton( self.m_panel2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.m_bpButton3, 0, wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.tree_catergories = wx.TreeCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		bSizer2.Add( self.tree_catergories, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer2 )
		self.m_panel2.Layout()
		bSizer2.Fit( self.m_panel2 )
		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.tree_parts = wx.dataview.DataViewTreeCtrl( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.tree_parts, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer3 )
		self.m_panel3.Layout()
		bSizer3.Fit( self.m_panel3 )
		self.m_splitter2.SplitVertically( self.m_panel2, self.m_panel3, 294 )
		bSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 294 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

