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
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 404,611 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		radio_shapeChoices = [ u"Rectangular", u"Trapezoidal", u"Oval", u"Circular" ]
		self.radio_shape = wx.RadioBox( self, wx.ID_ANY, u"Shape", wx.DefaultPosition, wx.DefaultSize, radio_shapeChoices, 1, 0 )
		self.radio_shape.SetSelection( 0 )
		bSizer7.Add( self.radio_shape, 0, wx.ALL|wx.EXPAND, 5 )
		
		radio_typeChoices = [ u"SMD", u"Thru hole", u"Connector", u"Mechanical" ]
		self.radio_type = wx.RadioBox( self, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, radio_typeChoices, 1, 0 )
		self.radio_type.SetSelection( 0 )
		bSizer7.Add( self.radio_type, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.panel_pad = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Pad", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		fgSizer1.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_name = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_name, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText51 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Angle (degree)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		fgSizer1.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_angle = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_angle, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Position X (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_position_x = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_position_x, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText63 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Position Y (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )
		fgSizer1.Add( self.m_staticText63, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_position_y = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_position_y, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText62 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Size X (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		fgSizer1.Add( self.m_staticText62, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_size_x = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_size_x, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText61 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Size Y (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		fgSizer1.Add( self.m_staticText61, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_size_y = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_size_y, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText611 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Shape Offset X (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )
		fgSizer1.Add( self.m_staticText611, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_offset_x = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_offset_x, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText6111 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Shape Offset Y (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText6111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_offset_y = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_offset_y, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText61111 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Pad to die length (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61111.Wrap( -1 )
		fgSizer1.Add( self.m_staticText61111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_pad_to_die = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_pad_to_die, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText621 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Trapezoidal delta (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText621.Wrap( -1 )
		fgSizer1.Add( self.m_staticText621, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_pad_trapezoidal_delta = wx.TextCtrl( self.panel_pad, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer1.Add( self.text_pad_trapezoidal_delta, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText622 = wx.StaticText( self.panel_pad, wx.ID_ANY, u"Trapezoidal direction", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText622.Wrap( -1 )
		fgSizer1.Add( self.m_staticText622, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		choice_trapezoidal_directionChoices = [ u"Vert", u"Horz" ]
		self.choice_trapezoidal_direction = wx.Choice( self.panel_pad, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_trapezoidal_directionChoices, 0 )
		self.choice_trapezoidal_direction.SetSelection( 0 )
		fgSizer1.Add( self.choice_trapezoidal_direction, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.panel_pad.SetSizer( fgSizer1 )
		self.panel_pad.Layout()
		fgSizer1.Fit( self.panel_pad )
		self.m_notebook1.AddPage( self.panel_pad, u"Pad", True )
		self.panel_drill = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer11 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer11.AddGrowableCol( 1 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText52 = wx.StaticText( self.panel_drill, wx.ID_ANY, u"Shape", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )
		fgSizer11.Add( self.m_staticText52, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		choice_drill_shapeChoices = [ u"Circular hole", u"Oval hole" ]
		self.choice_drill_shape = wx.Choice( self.panel_drill, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_drill_shapeChoices, 0 )
		self.choice_drill_shape.SetSelection( 0 )
		fgSizer11.Add( self.choice_drill_shape, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText34 = wx.StaticText( self.panel_drill, wx.ID_ANY, u"Size X (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		fgSizer11.Add( self.m_staticText34, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_drill_size_x = wx.TextCtrl( self.panel_drill, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer11.Add( self.text_drill_size_x, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText341 = wx.StaticText( self.panel_drill, wx.ID_ANY, u"Size Y (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText341.Wrap( -1 )
		fgSizer11.Add( self.m_staticText341, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_drill_size_y = wx.TextCtrl( self.panel_drill, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer11.Add( self.text_drill_size_y, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		self.panel_drill.SetSizer( fgSizer11 )
		self.panel_drill.Layout()
		fgSizer11.Fit( self.panel_drill )
		self.m_notebook1.AddPage( self.panel_drill, u"Drill", False )
		self.panel_clearance = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer111 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer111.AddGrowableCol( 1 )
		fgSizer111.SetFlexibleDirection( wx.BOTH )
		fgSizer111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText342 = wx.StaticText( self.panel_clearance, wx.ID_ANY, u"Net pad clearance (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText342.Wrap( -1 )
		fgSizer111.Add( self.m_staticText342, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_pad_clearance = wx.TextCtrl( self.panel_clearance, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer111.Add( self.text_pad_clearance, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3411 = wx.StaticText( self.panel_clearance, wx.ID_ANY, u"Solder mask clearance (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3411.Wrap( -1 )
		fgSizer111.Add( self.m_staticText3411, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_solder_mask_clearance = wx.TextCtrl( self.panel_clearance, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer111.Add( self.text_solder_mask_clearance, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_staticText44 = wx.StaticText( self.panel_clearance, wx.ID_ANY, u"Solder paste clearance (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )
		fgSizer111.Add( self.m_staticText44, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_solder_paste_clearance = wx.TextCtrl( self.panel_clearance, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer111.Add( self.text_solder_paste_clearance, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText45 = wx.StaticText( self.panel_clearance, wx.ID_ANY, u"Solder paste ratio clearance (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		fgSizer111.Add( self.m_staticText45, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_solder_paste_ratio_clearance = wx.TextCtrl( self.panel_clearance, wx.ID_ANY, u"0.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer111.Add( self.text_solder_paste_ratio_clearance, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panel_clearance.SetSizer( fgSizer111 )
		self.panel_clearance.Layout()
		fgSizer111.Fit( self.panel_clearance )
		self.m_notebook1.AddPage( self.panel_clearance, u"Clearance", False )
		self.panel_copper = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer112 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer112.AddGrowableCol( 1 )
		fgSizer112.SetFlexibleDirection( wx.BOTH )
		fgSizer112.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText521 = wx.StaticText( self.panel_copper, wx.ID_ANY, u"Pad connection", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText521.Wrap( -1 )
		fgSizer112.Add( self.m_staticText521, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		choice_pad_connectionChoices = [ u"None", u"From parent footprint", u"Solid", u"Thermal relief" ]
		self.choice_pad_connection = wx.Choice( self.panel_copper, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_pad_connectionChoices, 0 )
		self.choice_pad_connection.SetSelection( 0 )
		fgSizer112.Add( self.choice_pad_connection, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText343 = wx.StaticText( self.panel_copper, wx.ID_ANY, u"Thermal relief width (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText343.Wrap( -1 )
		fgSizer112.Add( self.m_staticText343, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_thermal_relief_width = wx.TextCtrl( self.panel_copper, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer112.Add( self.text_thermal_relief_width, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText3412 = wx.StaticText( self.panel_copper, wx.ID_ANY, u"Thermal relief gap (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3412.Wrap( -1 )
		fgSizer112.Add( self.m_staticText3412, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.text_thermal_relief_gap = wx.TextCtrl( self.panel_copper, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		fgSizer112.Add( self.text_thermal_relief_gap, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		self.panel_copper.SetSizer( fgSizer112 )
		self.panel_copper.Layout()
		fgSizer112.Fit( self.panel_copper )
		self.m_notebook1.AddPage( self.panel_copper, u"Copper zone", False )
		self.panel_layers = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1121 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1121.AddGrowableCol( 1 )
		fgSizer1121.SetFlexibleDirection( wx.BOTH )
		fgSizer1121.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText5211 = wx.StaticText( self.panel_layers, wx.ID_ANY, u"Copper", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5211.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText5211, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		choice_copper_layerChoices = [ u"All copper layers", u"F.Cu", u"B.Cu", u"None" ]
		self.choice_copper_layer = wx.Choice( self.panel_layers, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_copper_layerChoices, 0 )
		self.choice_copper_layer.SetSelection( 0 )
		fgSizer1121.Add( self.choice_copper_layer, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText58 = wx.StaticText( self.panel_layers, wx.ID_ANY, u"Technical Layers", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText58.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText58, 0, wx.ALL, 5 )
		
		self.m_staticText59 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText59.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText59, 0, wx.ALL, 5 )
		
		self.m_staticText591 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText591.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText591, 0, wx.ALL, 5 )
		
		self.check_f_adhes = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"F.Adhes", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_f_adhes, 0, wx.ALL, 5 )
		
		self.m_staticText592 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText592.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText592, 0, wx.ALL, 5 )
		
		self.check_b_adhes = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"B.Adhes", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_b_adhes, 0, wx.ALL, 5 )
		
		self.m_staticText593 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText593.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText593, 0, wx.ALL, 5 )
		
		self.check_f_paste = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"F.Paste", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_f_paste, 0, wx.ALL, 5 )
		
		self.m_staticText594 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText594.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText594, 0, wx.ALL, 5 )
		
		self.check_b_paste = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"B.Paste", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_b_paste, 0, wx.ALL, 5 )
		
		self.m_staticText595 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText595.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText595, 0, wx.ALL, 5 )
		
		self.check_f_silk = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"F.Silk", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_f_silk, 0, wx.ALL, 5 )
		
		self.m_staticText596 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText596.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText596, 0, wx.ALL, 5 )
		
		self.check_b_silk = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"B.Silk", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_b_silk, 0, wx.ALL, 5 )
		
		self.m_staticText597 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText597.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText597, 0, wx.ALL, 5 )
		
		self.check_f_mask = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"F.Mask", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_f_mask, 0, wx.ALL, 5 )
		
		self.m_staticText598 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText598.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText598, 0, wx.ALL, 5 )
		
		self.check_b_mask = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"B.Mask", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_b_mask, 0, wx.ALL, 5 )
		
		self.m_staticText599 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText599.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText599, 0, wx.ALL, 5 )
		
		self.check_dwgs_user = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"Dwgs.User", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_dwgs_user, 0, wx.ALL, 5 )
		
		self.m_staticText5910 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5910.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText5910, 0, wx.ALL, 5 )
		
		self.check_eco1_u = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"Eco1.U", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_eco1_u, 0, wx.ALL, 5 )
		
		self.m_staticText5911 = wx.StaticText( self.panel_layers, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5911.Wrap( -1 )
		fgSizer1121.Add( self.m_staticText5911, 0, wx.ALL, 5 )
		
		self.check_eco2_u = wx.CheckBox( self.panel_layers, wx.ID_ANY, u"Eco2.U", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1121.Add( self.check_eco2_u, 0, wx.ALL, 5 )
		
		
		self.panel_layers.SetSizer( fgSizer1121 )
		self.panel_layers.Layout()
		fgSizer1121.Fit( self.panel_layers )
		self.m_notebook1.AddPage( self.panel_layers, u"Layers", False )
		
		bSizer7.Add( self.m_notebook1, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.radio_shape.Bind( wx.EVT_RADIOBOX, self.onShapeRadioBox )
		self.radio_type.Bind( wx.EVT_RADIOBOX, self.onTypeRadioBox )
		self.text_name.Bind( wx.EVT_TEXT_ENTER, self.onPadTextEnter )
		self.text_angle.Bind( wx.EVT_TEXT_ENTER, self.onAngleTextEnter )
		self.text_position_x.Bind( wx.EVT_TEXT_ENTER, self.onPositionXTextEnter )
		self.text_position_y.Bind( wx.EVT_TEXT_ENTER, self.onPositionYTextEnter )
		self.text_size_x.Bind( wx.EVT_TEXT_ENTER, self.onSizeXTextEnter )
		self.text_size_y.Bind( wx.EVT_TEXT_ENTER, self.onSizeYTextEnter )
		self.text_offset_x.Bind( wx.EVT_TEXT_ENTER, self.onOffsetXTextEnter )
		self.text_offset_y.Bind( wx.EVT_TEXT_ENTER, self.onOffsetYTextEnter )
		self.text_pad_to_die.Bind( wx.EVT_TEXT_ENTER, self.onPadToDieTextEnter )
		self.text_pad_trapezoidal_delta.Bind( wx.EVT_TEXT_ENTER, self.onTrapezoidalDeltaTextEnter )
		self.choice_trapezoidal_direction.Bind( wx.EVT_CHOICE, self.onTrapezoidalDirectionChoice )
		self.choice_drill_shape.Bind( wx.EVT_CHOICE, self.onDrillShapeChoice )
		self.text_drill_size_x.Bind( wx.EVT_TEXT_ENTER, self.onDrillSizeXTextEnter )
		self.text_drill_size_y.Bind( wx.EVT_TEXT_ENTER, self.onDrillSizeYTextEnter )
		self.text_pad_clearance.Bind( wx.EVT_TEXT_ENTER, self.onPadClearanceTextEnter )
		self.text_solder_mask_clearance.Bind( wx.EVT_TEXT_ENTER, self.onSolderMaskClearanceTextEnter )
		self.text_solder_paste_clearance.Bind( wx.EVT_TEXT_ENTER, self.onTextSolderPasteClearanceTextEnter )
		self.text_solder_paste_ratio_clearance.Bind( wx.EVT_TEXT_ENTER, self.onSolderPasteRatioClearanceTextEnter )
		self.choice_pad_connection.Bind( wx.EVT_CHOICE, self.onPadConnectionChoice )
		self.text_thermal_relief_width.Bind( wx.EVT_TEXT_ENTER, self.onThermalReliefWidthTextEnter )
		self.text_thermal_relief_gap.Bind( wx.EVT_TEXT_ENTER, self.onTextThermalReliefGapTextEnter )
		self.choice_copper_layer.Bind( wx.EVT_CHOICE, self.onCopperLayerChoice )
		self.check_f_adhes.Bind( wx.EVT_CHECKBOX, self.onFAdhesCheckBox )
		self.check_b_adhes.Bind( wx.EVT_CHECKBOX, self.onBAdhesCheckBox )
		self.check_f_paste.Bind( wx.EVT_CHECKBOX, self.onFPasteCheckBox )
		self.check_b_paste.Bind( wx.EVT_CHECKBOX, self.onBPasteCheckBox )
		self.check_f_silk.Bind( wx.EVT_CHECKBOX, self.onFSilkCheckBox )
		self.check_b_silk.Bind( wx.EVT_CHECKBOX, self.onBSilkCheckBox )
		self.check_f_mask.Bind( wx.EVT_CHECKBOX, self.onFMaskCheckBox )
		self.check_b_mask.Bind( wx.EVT_CHECKBOX, self.onBMaskCheckBox )
		self.check_dwgs_user.Bind( wx.EVT_CHECKBOX, self.onDwgsUserCheckBox )
		self.check_eco1_u.Bind( wx.EVT_CHECKBOX, self.onEco1UCheckBox )
		self.check_eco2_u.Bind( wx.EVT_CHECKBOX, self.onEco2UCheckBox )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onShapeRadioBox( self, event ):
		event.Skip()
	
	def onTypeRadioBox( self, event ):
		event.Skip()
	
	def onPadTextEnter( self, event ):
		event.Skip()
	
	def onAngleTextEnter( self, event ):
		event.Skip()
	
	def onPositionXTextEnter( self, event ):
		event.Skip()
	
	def onPositionYTextEnter( self, event ):
		event.Skip()
	
	def onSizeXTextEnter( self, event ):
		event.Skip()
	
	def onSizeYTextEnter( self, event ):
		event.Skip()
	
	def onOffsetXTextEnter( self, event ):
		event.Skip()
	
	def onOffsetYTextEnter( self, event ):
		event.Skip()
	
	def onPadToDieTextEnter( self, event ):
		event.Skip()
	
	def onTrapezoidalDeltaTextEnter( self, event ):
		event.Skip()
	
	def onTrapezoidalDirectionChoice( self, event ):
		event.Skip()
	
	def onDrillShapeChoice( self, event ):
		event.Skip()
	
	def onDrillSizeXTextEnter( self, event ):
		event.Skip()
	
	def onDrillSizeYTextEnter( self, event ):
		event.Skip()
	
	def onPadClearanceTextEnter( self, event ):
		event.Skip()
	
	def onSolderMaskClearanceTextEnter( self, event ):
		event.Skip()
	
	def onTextSolderPasteClearanceTextEnter( self, event ):
		event.Skip()
	
	def onSolderPasteRatioClearanceTextEnter( self, event ):
		event.Skip()
	
	def onPadConnectionChoice( self, event ):
		event.Skip()
	
	def onThermalReliefWidthTextEnter( self, event ):
		event.Skip()
	
	def onTextThermalReliefGapTextEnter( self, event ):
		event.Skip()
	
	def onCopperLayerChoice( self, event ):
		event.Skip()
	
	def onFAdhesCheckBox( self, event ):
		event.Skip()
	
	def onBAdhesCheckBox( self, event ):
		event.Skip()
	
	def onFPasteCheckBox( self, event ):
		event.Skip()
	
	def onBPasteCheckBox( self, event ):
		event.Skip()
	
	def onFSilkCheckBox( self, event ):
		event.Skip()
	
	def onBSilkCheckBox( self, event ):
		event.Skip()
	
	def onFMaskCheckBox( self, event ):
		event.Skip()
	
	def onBMaskCheckBox( self, event ):
		event.Skip()
	
	def onDwgsUserCheckBox( self, event ):
		event.Skip()
	
	def onEco1UCheckBox( self, event ):
		event.Skip()
	
	def onEco2UCheckBox( self, event ):
		event.Skip()
	

