#!/usr/bin/python3

# activate whole application profiling
# see https://toucantoco.com/en/tech-blog/tech/python-performance-optimization
# see https://github.com/what-studio/profiling

import os
import platform
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('resources'):
    # we are in an installed package, set new path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# configure wxPython
import sys
import argparse
from configuration import configuration
import sys, time

dialog_main = None

def configure(value):
    pass

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

    parser = argparse.ArgumentParser(description='Kipartman, the kicad part manager')
    parser.add_argument('-c', '--config', help='configuration file to use (default: %s)'%configuration.filename)
    
    args = parser.parse_args()
    
    if args.config:
        configuration.filename = args.config
        if not configuration.Load():
            return 
    
    print("Running kipartman")

    import wx
    from frames.main_frame import MainFrame
    app = wx.App()
    
    global dialog_main
    dialog_main = MainFrame(None)    
    dialog_main.Show()

    app.MainLoop() 

if __name__ == "__main__":

    main()

