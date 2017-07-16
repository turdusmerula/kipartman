# cache for kipartman data
import wx.lib.newevent
import rest

PartChangedEvent, EVT_PART_CHANGED_EVENT = wx.lib.newevent.NewEvent()

parts_categories = []
parts = []

def load_parts_categories():
    global parts_categories
    parts_categories = rest.api.find_parts_categories()

def load_parts():
    global parts
    parts = rest.api.find_parts()