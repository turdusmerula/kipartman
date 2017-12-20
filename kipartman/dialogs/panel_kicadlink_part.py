# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PanelKicadLinkPart
###########################################################################

class PanelKicadLinkPart ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 1051,863 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel_kicadlink_part_basic = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.panel_kicadlink_part_basic.SetBackgroundColour( wx.Colour( 128, 255, 255 ) )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer5 = wx.FlexGridSizer( 0, 5, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText31 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"KICAD Eeschema Link", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		self.m_staticText31.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		
		fgSizer5.Add( self.m_staticText31, 0, wx.ALL, 5 )
		
		self.m_staticText3121 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3121.Wrap( -1 )
		fgSizer5.Add( self.m_staticText3121, 0, wx.ALL, 5 )
		
		self.m_staticText31211 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31211.Wrap( -1 )
		fgSizer5.Add( self.m_staticText31211, 0, wx.ALL, 5 )
		
		self.m_staticText3123 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3123.Wrap( -1 )
		fgSizer5.Add( self.m_staticText3123, 0, wx.ALL, 5 )
		
		self.m_staticText312 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText312.Wrap( -1 )
		fgSizer5.Add( self.m_staticText312, 0, wx.ALL, 5 )
		
		bSizer1811 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText311 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"AutoSearch", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText311.Wrap( -1 )
		bSizer1811.Add( self.m_staticText311, 0, wx.ALL, 5 )
		
		self.checkBox_search_auto = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_auto.SetValue(True) 
		bSizer1811.Add( self.checkBox_search_auto, 0, wx.ALL, 5 )
		
		
		fgSizer5.Add( bSizer1811, 1, wx.EXPAND, 5 )
		
		self.m_staticText3122 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"--------------", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3122.Wrap( -1 )
		fgSizer5.Add( self.m_staticText3122, 0, wx.ALL, 5 )
		
		self.button_kicad_part_search = wx.Button( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SEARCH", wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT|wx.BU_RIGHT )
		fgSizer5.Add( self.button_kicad_part_search, 0, wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT, 5 )
		
		self.button_partselect = wx.Button( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SelectPart", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.button_partselect, 0, wx.ALL, 5 )
		
		self.button_kicadupdate = wx.Button( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Update KiCAD", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer5.Add( self.button_kicadupdate, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( fgSizer5, 1, wx.EXPAND, 5 )
		
		bSizer181 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer15.Add( bSizer181, 1, wx.EXPAND, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 0, 5, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText32 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"FIELD", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		self.m_staticText32.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, "Arial" ) )
		
		fgSizer1.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		self.m_staticText322 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"EXISTING VALUE", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText322.Wrap( -1 )
		self.m_staticText322.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, "Arial" ) )
		
		fgSizer1.Add( self.m_staticText322, 0, wx.ALL, 5 )
		
		self.m_staticText321 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"NEW VALUE                    ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText321.Wrap( -1 )
		self.m_staticText321.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, "Arial" ) )
		
		fgSizer1.Add( self.m_staticText321, 0, wx.ALL, 5 )
		
		self.m_staticText3221 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SEARCH", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3221.Wrap( -1 )
		self.m_staticText3221.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, "Arial" ) )
		
		fgSizer1.Add( self.m_staticText3221, 0, wx.ALL, 5 )
		
		self.m_staticText3211 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"UPDATE", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3211.Wrap( -1 )
		self.m_staticText3211.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True, "Arial" ) )
		
		fgSizer1.Add( self.m_staticText3211, 0, wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Value", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.kicad_part_value = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_value, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.kicad_part_value_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_value_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_value = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_value.SetValue(True) 
		fgSizer1.Add( self.checkBox_search_value, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_value = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_update_value, 0, wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Reference", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.kicad_part_reference = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_reference, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.kicad_part_reference_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_reference_new.Enable( False )
		self.kicad_part_reference_new.Hide()
		
		fgSizer1.Add( self.kicad_part_reference_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_reference = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_reference.Enable( False )
		self.checkBox_search_reference.Hide()
		
		fgSizer1.Add( self.checkBox_search_reference, 0, wx.ALL, 5 )
		
		self.checkBox_update_reference = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_reference.Enable( False )
		self.checkBox_update_reference.Hide()
		
		fgSizer1.Add( self.checkBox_update_reference, 0, wx.ALL, 5 )
		
		self.m_staticText41 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Component ID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		fgSizer1.Add( self.m_staticText41, 0, wx.ALL, 5 )
		
		self.kicad_part_id = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_id, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_id_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.kicad_part_id_new.Enable( False )
		self.kicad_part_id_new.Hide()
		
		fgSizer1.Add( self.kicad_part_id_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_componentId = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_componentId.Enable( False )
		self.checkBox_search_componentId.Hide()
		
		fgSizer1.Add( self.checkBox_search_componentId, 0, wx.ALL, 5 )
		
		self.checkBox_update_componentid = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_componentid.Enable( False )
		self.checkBox_update_componentid.Hide()
		
		fgSizer1.Add( self.checkBox_update_componentid, 0, wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Footprint", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.kicad_part_footprint = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_footprint, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_footprint_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_footprint_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_footprint = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_footprint, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_footprint = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_update_footprint, 0, wx.ALL, 5 )
		
		self.m_staticText51 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Model", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.kicad_part_model = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_model, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_model_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_model_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_model = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_model.Enable( False )
		self.checkBox_search_model.Hide()
		
		fgSizer1.Add( self.checkBox_search_model, 0, wx.ALL, 5 )
		
		self.checkBox_update_model = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_model.Enable( False )
		self.checkBox_update_model.Hide()
		
		fgSizer1.Add( self.checkBox_update_model, 0, wx.ALL, 5 )
		
		self.m_staticText511 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SKU", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511.Wrap( -1 )
		fgSizer1.Add( self.m_staticText511, 0, wx.ALL, 5 )
		
		self.kicad_part_SKU = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_SKU, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_SKU_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_SKU_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_SKU = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_SKU, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_SKU = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_SKU.SetValue(True) 
		fgSizer1.Add( self.checkBox_update_SKU, 0, wx.ALL, 5 )
		
		self.m_staticText5111 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"MPN", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5111, 0, wx.ALL, 5 )
		
		self.kicad_part_MPN = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_MPN, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_MPN_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_MPN_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_MPN = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_MPN, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_MPN = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_MPN.SetValue(True) 
		fgSizer1.Add( self.checkBox_update_MPN, 0, wx.ALL, 5 )
		
		self.m_staticText51111 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"MFR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51111, 0, wx.ALL, 5 )
		
		self.kicad_part_MFR = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_MFR, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_MFR_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_MFR_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_MFR = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_MFR.Enable( False )
		self.checkBox_search_MFR.Hide()
		
		fgSizer1.Add( self.checkBox_search_MFR, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_MFR = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_MFR.Enable( False )
		self.checkBox_update_MFR.Hide()
		
		fgSizer1.Add( self.checkBox_update_MFR, 0, wx.ALL, 5 )
		
		self.m_staticText51112 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SPN", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51112.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51112, 0, wx.ALL, 5 )
		
		self.kicad_part_SPN = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_SPN, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_SPN_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_SPN_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_SPN = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.checkBox_search_SPN, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_SPN = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_SPN.SetValue(True) 
		fgSizer1.Add( self.checkBox_update_SPN, 0, wx.ALL, 5 )
		
		self.m_staticText511111 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"SPR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText511111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText511111, 0, wx.ALL, 5 )
		
		self.kicad_part_SPR = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.kicad_part_SPR, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.kicad_part_SPR_new = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.kicad_part_SPR_new, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.checkBox_search_SPR = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_search_SPR.Enable( False )
		self.checkBox_search_SPR.Hide()
		
		fgSizer1.Add( self.checkBox_search_SPR, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.checkBox_update_SPR = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.checkBox_update_SPR.Enable( False )
		self.checkBox_update_SPR.Hide()
		
		fgSizer1.Add( self.checkBox_update_SPR, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Comment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.edit_part_comment = wx.TextCtrl( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.edit_part_comment.SetMinSize( wx.Size( -1,120 ) )
		
		fgSizer1.Add( self.edit_part_comment, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText61 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Kicad Eeschema Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		bSizer5.Add( self.m_staticText61, 0, wx.ALL, 5 )
		
		self.m_checkBoxKcEeschemaRunning = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Eeschema Running", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxKcEeschemaRunning.Enable( False )
		
		bSizer5.Add( self.m_checkBoxKcEeschemaRunning, 0, wx.ALL, 5 )
		
		self.m_checkBoxEeschemanAdd = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Component Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxEeschemanAdd.Enable( False )
		
		bSizer5.Add( self.m_checkBoxEeschemanAdd, 0, wx.ALL, 5 )
		
		self.m_checkBoxComponentEdit = wx.CheckBox( self.panel_kicadlink_part_basic, wx.ID_ANY, u"Component Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxComponentEdit.Enable( False )
		
		bSizer5.Add( self.m_checkBoxComponentEdit, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		self.m_staticText13 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer1.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_staticText131 = wx.StaticText( self.panel_kicadlink_part_basic, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )
		fgSizer1.Add( self.m_staticText131, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		
		self.panel_kicadlink_part_basic.SetSizer( bSizer15 )
		self.panel_kicadlink_part_basic.Layout()
		bSizer15.Fit( self.panel_kicadlink_part_basic )
		bSizer1.Add( self.panel_kicadlink_part_basic, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDialog )
		self.button_kicad_part_search.Bind( wx.EVT_BUTTON, self.onButtonKicadLinkComponentSearchClick )
		self.button_partselect.Bind( wx.EVT_BUTTON, self.onButtonKicadLinkPartSelect )
		self.button_kicadupdate.Bind( wx.EVT_BUTTON, self.onButtonKicadLinkFieldsUpdateClick )
		self.kicad_part_value.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_value_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_reference.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_reference_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_id.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_id_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_footprint.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_footprint_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_model.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_model_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SKU.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SKU_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_MPN.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_MPN_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_MFR.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_MFR_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SPN.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SPN_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SPR.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.kicad_part_SPR_new.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
		self.edit_part_comment.Bind( wx.EVT_TEXT, self.onTextEditPartPartText )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDialog( self, event ):
		event.Skip()
	
	def onButtonKicadLinkComponentSearchClick( self, event ):
		event.Skip()
	
	def onButtonKicadLinkPartSelect( self, event ):
		event.Skip()
	
	def onButtonKicadLinkFieldsUpdateClick( self, event ):
		event.Skip()
	
	def onTextEditPartPartText( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

