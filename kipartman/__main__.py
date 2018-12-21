#!/usr/bin/python3

import os
import platform
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('resources'):
    # we are in an installed package, set new path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# configure django to use the model
#from django.core.wsgi import get_wsgi_application
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'kipartbase.settings'
#application = get_wsgi_application()

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
    
#     from kicad.kicad_schematic_file import KicadSchematicFile
#     sch = KicadSchematicFile()
#     sch.LoadFile('/home/seb/git/mcu_atsamd21g/MCU_ATSAMD21G/MCU_ATSAMD21G.sch')
#     
#     for comp in sch.Components():
#         comp.kicad_part = 'aaa'
#         print "**", comp.symbol, comp.reference, comp.value, comp.footprint
#     sch.Save()
#     #sch.DebugWrite(sch.parent)
#     exit(1)

#     import cProfile
#     cProfile.run("main()")
    main()

