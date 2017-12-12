# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui

###########################################################################
## Class PanelKicadLinkPart
###########################################################################

class PanelKicadLinkPart ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1089,1034 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		
		self.panel_kicadlink_part_basic = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer181 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.button_kicad_part_search = wx.Button( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SEARCH", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT )
		bSizer181.Add( self.button_kicad_part_search, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer15.Add( bSizer181, 1, wx.EXPAND, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText3 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Value", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.kicad_part_value = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_value.Enable( False )
		
		fgSizer1.Add( self.kicad_part_value, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.checkBox_search_value = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_value, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText4 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Reference", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.kicad_part_reference = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_reference.Enable( False )
		
		fgSizer1.Add( self.kicad_part_reference, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.checkBox_search_reference = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_reference.Enable( False )
		self.checkBox_search_reference.Hide()
		
		fgSizer1.Add( self.checkBox_search_reference, 0, wx.ALL, 5 )
		
		self.m_staticText41 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Component ID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		fgSizer1.Add( self.m_staticText41, 0, wx.ALL, 5 )
		
		self.kicad_part_id = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_id.Enable( False )
		
		fgSizer1.Add( self.kicad_part_id, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_componentId = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_componentId.Enable( False )
		self.checkBox_search_componentId.Hide()
		
		fgSizer1.Add( self.checkBox_search_componentId, 0, wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Footprint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.kicad_part_footprint = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_footprint.Enable( False )
		
		fgSizer1.Add( self.kicad_part_footprint, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_footprint = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_footprint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText51 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.kicad_part_model = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_model.Enable( False )
		
		fgSizer1.Add( self.kicad_part_model, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_model = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_model.Enable( False )
		self.checkBox_search_model.Hide()
		
		fgSizer1.Add( self.checkBox_search_model, 0, wx.ALL, 5 )
		
		self.m_staticText511 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SKU", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )
		fgSizer1.Add( self.m_staticText511, 0, wx.ALL, 5 )
		
		self.kicad_part_SKU = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_SKU.Enable( False )
		
		fgSizer1.Add( self.kicad_part_SKU, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_SKU = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_SKU, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText5111 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"MPN", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5111, 0, wx.ALL, 5 )
		
		self.kicad_part_MPN = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_MPN.Enable( False )
		
		fgSizer1.Add( self.kicad_part_MPN, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_MPN = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_MPN, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText51111 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"MFR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51111, 0, wx.ALL, 5 )
		
		self.kicad_part_MFR = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_MFR.Enable( False )
		
		fgSizer1.Add( self.kicad_part_MFR, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_MFR = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_MFR.Enable( False )
		self.checkBox_search_MFR.Hide()
		
		fgSizer1.Add( self.checkBox_search_MFR, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText51112 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SPN", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51112.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51112, 0, wx.ALL, 5 )
		
		self.kicad_part_SPN = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_SPN.Enable( False )
		
		fgSizer1.Add( self.kicad_part_SPN, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_SPN = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_SPN, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText511111 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SPR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText511111, 0, wx.ALL, 5 )
		
		self.kicad_part_SPR = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_SPR.Enable( False )
		
		fgSizer1.Add( self.kicad_part_SPR, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_SPR = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_SPR.Enable( False )
		self.checkBox_search_SPR.Hide()
		
		fgSizer1.Add( self.checkBox_search_SPR, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticText6 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_comment = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_part_comment.SetMinSize( wx.Size( -1,120 ) )
		
		fgSizer1.Add( self.edit_part_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer1.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_staticText61 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Kicad Eeschema Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		fgSizer1.Add( self.m_staticText61, 0, wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBoxKcEeschemaRunning = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Eeschema Running", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxKcEeschemaRunning.Enable( False )
		
		bSizer5.Add( self.m_checkBoxKcEeschemaRunning, 0, wx.ALL, 5 )
		
		self.m_checkBoxEeschemanAdd = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Component Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxEeschemanAdd.Enable( False )
		
		bSizer5.Add( self.m_checkBoxEeschemanAdd, 0, wx.ALL, 5 )
		
		self.m_checkBoxComponentEdit = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Component Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxComponentEdit.Enable( False )
		
		bSizer5.Add( self.m_checkBoxComponentEdit, 0, wx.ALL, 5 )
		
		self.button_kicadupdate = wx.Button( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.button_kicadupdate, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		button_part_edit = wx.StdDialogButtonSizer()
		self.button_part_editApply = wx.Button( self.panel_kicadlink_part_basic, wx.ID_APPLY )
		button_part_edit.AddButton( self.button_part_editApply )
		self.button_part_editCancel = wx.Button( self.panel_kicadlink_part_basic, wx.ID_CANCEL )
		button_part_edit.AddButton( self.button_part_editCancel )
		button_part_edit.Realize();
		
		bSizer15.Add( button_part_edit, 0, wx.EXPAND, 5 )
		
		
		self.panel_kicadlink_part_basic.SetSizer( bSizer15 )
		self.panel_kicadlink_part_basic.Layout()
		bSizer15.Fit( self.panel_kicadlink_part_basic )
		self.panel_kicadlink_part_extended = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.notebook_part = wx.aui.AuiNotebook( self.panel_kicadlink_part_extended, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer17.Add( self.notebook_part, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.panel_kicadlink_part_extended.SetSizer( bSizer17 )
		self.panel_kicadlink_part_extended.Layout()
		bSizer17.Fit( self.panel_kicadlink_part_extended )
		self.m_splitter3.SplitVertically( self.panel_kicadlink_part_basic, self.panel_kicadlink_part_extended, 0 )
		bSizer1.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_kicad_part_search.Bind( wx.EVT_BUTTON, self.onButtonPartFootprintClick )
		self.kicad_part_value.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_reference.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_id.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_footprint.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_model.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SKU.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_MPN.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_MFR.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SPN.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SPR.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.edit_part_comment.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.button_kicadupdate.Bind( wx.EVT_BUTTON, self.onButtonOctopartClick )
		self.button_part_editApply.Bind( wx.EVT_BUTTON, self.onButtonPartEditApply )
		self.button_part_editCancel.Bind( wx.EVT_BUTTON, self.onButtonPartEditCancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonPartFootprintClick( self, event ):
		event.Skip()
	
	def onTextEditPartPartText( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	def onButtonOctopartClick( self, event ):
		event.Skip()
	
	def onButtonPartEditApply( self, event ):
		event.Skip()
	
	def onButtonPartEditCancel( self, event ):
		event.Skip()
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	

