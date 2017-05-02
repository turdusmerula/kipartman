#!/usr/bin/python3

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# configure django to use the model
#from django.core.wsgi import get_wsgi_application
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'kipartbase.settings'
#application = get_wsgi_application()

# configure wxPython
import wx
from frames.main_frame import MainFrame

print "Running kipartman"
app = wx.App()

frame = MainFrame(None)

frame.Show()

app.MainLoop()
