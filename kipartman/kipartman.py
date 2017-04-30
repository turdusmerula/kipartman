#!/usr/bin/python3

# simple.py

import wx

from frames.main_frame import MainFrame


app = wx.App()

frame = MainFrame(None)

frame.Show()

app.MainLoop()
