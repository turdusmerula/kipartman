import wx
import wx.lib.newevent

(FilterChangedEvent, EVT_FILTER_CHANGED) = wx.lib.newevent.NewEvent()

class FilterSet(wx.EvtHandler):
    def __init__(self, owner, filter_bar=None):
        super(FilterSet, self).__init__()
        
        self.owner = owner
        
        # list of filters by filter group
        self.filters = {}
        self.check_filter = {}
        
        self.filter_bar = filter_bar

    def replace(self, filter, group=None):
        self.filters[group] = []
        self.filters[group].append(filter)

        self.refresh_filter_panel()
        
        wx.PostEvent(self, FilterChangedEvent())
        
    def append(self, filter, group=None):
        if group not in self.filters:
            self.filters[group] = []
        self.filters[group].append(filter)

        self.refresh_filter_panel()

        wx.PostEvent(self, FilterChangedEvent())

    def refresh_filter_panel(self):
        if self.filter_bar is None:
            return
        
        filters = self.get_filters()
        
        for check_filter in self.check_filter:
            self.filter_bar.RemoveTool(check_filter.GetId())
        self.check_filter = {}
        
        filter_id = 1
        for filter in filters:
#             button_remove_filter = wx.Button( self.filter_bar, wx.ID_ANY, u"x", wx.DefaultPosition, wx.Size( 16,16 ), 0|wx.NO_BORDER, name=f"button_remove_filter_{filter_id}" )
#             button_remove_filter.SetMaxSize( wx.Size( 16,16 ) )
#             button_remove_filter.Bind( wx.EVT_BUTTON, self.onButtonRemoveFilterClick )
#             
#             label_filter = wx.StaticText( self.filter_bar, wx.ID_ANY, str(filter), wx.DefaultPosition, wx.DefaultSize, 0, name=f"label_filter_{filter_id}" )
#             
#             self.filter_bar.AddControl( button_remove_filter )
#             self.filter_bar.AddControl( label_filter )

            check_filter = wx.CheckBox( self.filter_bar, wx.ID_ANY, str(filter), wx.DefaultPosition, wx.DefaultSize, 0 )
            check_filter.SetValue(True)
            check_filter.Bind( wx.EVT_CHECKBOX, self.onCheckFilterClick )

            self.filter_bar.AddControl(check_filter)
            self.check_filter[self.filter_bar.AddSeparator()] = None
            self.filter_bar.Realize()
# 
            self.check_filter[check_filter] = filter
            
            filter_id += 1
    
    def remove(self, filter):
        for name in self.filters:
            filters = self.filters[name]
            if filter in filters:
                filters.remove(filter)
        wx.PostEvent(self, FilterChangedEvent())

    def remove_group(self, name):
        if name in self.filters:
            self.filters.pop(name)
        wx.PostEvent(self, FilterChangedEvent())

    def onCheckFilterClick( self, event ):
        filter = self.check_filter[event.GetEventObject()]
        self.remove(filter)
        self.filter_bar.RemoveTool(event.GetEventObject().GetId())

        wx.PostEvent(self, FilterChangedEvent())
    
    def get_filters(self):
        res = []
        
        for name in self.filters:
            filters = self.filters[name]
            for filter in filters:
                res.append(filter)
        
        return res

    def get_filters_group(self, group):
        if group not in self.filters:
            return []
                
        return self.filters[group]

class Filter(object):
    def __init__(self):
        pass
    
    def apply(self):
        return False

class DataFilter(Filter):
    def __init__(self):
        super(DataFilter, self).__init__()
    
    def apply(self, request):
        return request

# class DataFilter(Filter):
#     def __init__(self):
#         super(DataFilter, self).__init__()
#     
#     def apply(self, request):
#         return request
