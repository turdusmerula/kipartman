# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr 29 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui

###########################################################################
## Class PanelEditPart
###########################################################################

class PanelEditPart ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1080,325 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.panel_edit_part_basic = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.panel_edit_part_basic, wx.ID_ANY, u"Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.edit_part_name = wx.TextCtrl( self.panel_edit_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.edit_part_name, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.button_octopart = wx.Button( self.panel_edit_part_basic, wx.ID_ANY, u"Octopart", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.button_octopart, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self.panel_edit_part_basic, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_description = wx.TextCtrl( self.panel_edit_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.edit_part_description, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.panel_edit_part_basic, wx.ID_ANY, u"Footprint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_part_footprint = wx.Button( self.panel_edit_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		fgSizer1.Add( self.button_part_footprint, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText51 = wx.StaticText( self.panel_edit_part_basic, wx.ID_ANY, u"Symbol", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.button_part_symbol = wx.Button( self.panel_edit_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		fgSizer1.Add( self.button_part_symbol, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self.panel_edit_part_basic, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_comment = wx.TextCtrl( self.panel_edit_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_part_comment.SetMinSize( wx.Size( -1,120 ) )
		
		fgSizer1.Add( self.edit_part_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_part_edit = wx.StdDialogButtonSizer()
		self.button_part_editApply = wx.Button( self.panel_edit_part_basic, wx.ID_APPLY )
		button_part_edit.AddButton( self.button_part_editApply )
		self.button_part_editCancel = wx.Button( self.panel_edit_part_basic, wx.ID_CANCEL )
		button_part_edit.AddButton( self.button_part_editCancel )
		button_part_edit.Realize();
		
		bSizer15.Add( button_part_edit, 0, wx.EXPAND, 5 )
		
		
		self.panel_edit_part_basic.SetSizer( bSizer15 )
		self.panel_edit_part_basic.Layout()
		bSizer15.Fit( self.panel_edit_part_basic )
		self.panel_edit_part_extended = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.notebook_part = wx.aui.AuiNotebook( self.panel_edit_part_extended, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer17.Add( self.notebook_part, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panel_edit_part_extended.SetSizer( bSizer17 )
		self.panel_edit_part_extended.Layout()
		bSizer17.Fit( self.panel_edit_part_extended )
		self.m_splitter3.SplitVertically( self.panel_edit_part_basic, self.panel_edit_part_extended, 0 )
		bSizer1.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.edit_part_name.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.button_octopart.Bind( wx.EVT_BUTTON, self.onButtonOctopartClick )
		self.edit_part_description.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.button_part_footprint.Bind( wx.EVT_BUTTON, self.onButtonPartFootprintClick )
		self.button_part_symbol.Bind( wx.EVT_BUTTON, self.onButtonPartSymbolClick )
		self.edit_part_comment.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.button_part_editApply.Bind( wx.EVT_BUTTON, self.onButtonPartEditApply )
		self.button_part_editCancel.Bind( wx.EVT_BUTTON, self.onButtonPartEditCancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onTextEditPartPartText( self, event ):
		event.Skip()
	
	def onButtonOctopartClick( self, event ):
		event.Skip()
	
	
	def onButtonPartFootprintClick( self, event ):
		event.Skip()
	
	def onButtonPartSymbolClick( self, event ):
		event.Skip()
	
	
	def onButtonPartEditApply( self, event ):
		event.Skip()
	
	def onButtonPartEditCancel( self, event ):
		event.Skip()
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	

