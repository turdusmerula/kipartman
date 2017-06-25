import wx

class Filter(object):
    def __init__(self, filters_panel, onRemove):
        self.filters = {}
        
#         self.filters_sizer = wx.BoxSizer( wx.HORIZONTAL )
#         filters_panel.SetSizer(self.filters_sizer)
        self.filters_panel = filters_panel
        self.filters_sizer = filters_panel.GetSizer()
        
        self.onRemove = onRemove
        
    def add(self, name, value, value_label=''):
        button_remove_filter = wx.Button( self.filters_panel, wx.ID_ANY, u"x", wx.DefaultPosition, wx.Size( 16,16 ), 0|wx.NO_BORDER, name=name )
        button_remove_filter.SetMaxSize( wx.Size( 16,16 ) )
        button_remove_filter.Bind( wx.EVT_BUTTON, self.onRemove )
        self.filters_sizer.Add( button_remove_filter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        if value_label=="":
            label = name+': '+value
        else:
            label = name+': '+value_label
        label_filter = wx.StaticText( self.filters_panel, wx.ID_ANY, label, wx.DefaultPosition, wx.DefaultSize, 0 )
        label_filter.Wrap( -1 )
        self.filters_sizer.Add( label_filter, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        line_filter = wx.StaticLine( self.filters_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        self.filters_sizer.Add( line_filter, 0, wx.EXPAND|wx.ALL, 5 )
        
        self.filters_panel.SetSizerAndFit(self.filters_sizer)
        self.filters_sizer.RecalcSizes()
        
        f = { 
            'name': name,
            'value': value,
            'value_label': value_label,
            'button_remove_filter': button_remove_filter,
            'label_filter': label_filter,
            'line_filter': line_filter
        }
        
        self.filters[name] = f
        

        return f
    
    def remove(self, name):
        if self.filters.has_key(name)==False:
            return None
        f = self.filters[name]
        f['button_remove_filter'].Destroy()
        f['label_filter'].Destroy()
        f['line_filter'].Destroy()
        self.filters_sizer.RecalcSizes()
        return self.filters.pop(name)

    def query_filter(self):
        qf = {}
        
        for name in self.filters:
            f = self.filters[name]
            qf[f['name']] = f['value']
        
        return qf