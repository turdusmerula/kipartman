#!/usr/bin/python3

import os
import platform
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('resources'):
    # we are in an installed package, set new path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import multiprocessing


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
    
    frame = MainFrame(None)    
    frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    # kicad GUI link to Kipartman :SETUP
    # 2017-12 presently only Windows support
    # TODO: Change to the configuration variable configuration.kicad_eeschema_link
    # TODO: Move Subprocess and Thread startup and teardown to where first configuration is accessed
    if platform.system() == 'Windows':
        from helper import kicad_gui_monitor

        kcW32eventQueue = multiprocessing.Queue()
        kcW32eventProcessingThread = kicad_gui_monitor.KicadGUIEventProcessor(target=kicad_gui_monitor.KicadGUIEventProcessor.EventProcessor,
                                                                              args=(kicad_gui_monitor.KicadGUIEventProcessor, kcW32eventQueue,))
        kcW32eventProcessingThread.start()

        processKcW32Ew = multiprocessing.Process(target=kicad_gui_monitor.EventWatcher, args=(kcW32eventQueue,))
        #FOR DEBUG -- comment out start and uncomment the following line
        processKcW32Ew.start()
        #kicad_gui_monitor.EventWatcher(kcW32eventQueue)
    else:
        pass  # TODO: Linux/Mac support for KICAD GUI to Kipartman : SETUP
    
    main()

    #kicad GUI link to Kipartman : TEARDOWN
    # 2017-12 presently only Windows
    if platform.system() == 'Windows':
        kcW32eventProcessingThread.terminate()
        kcW32eventProcessingThread.join()
        kcW32eventProcessingThread = None
        processKcW32Ew.terminate()
    else:
        pass  # TODO: Linux/Mac support for KICAD GUI to Kipartman : TEARDOWN

    #import cProfile
    #cProfile.run("main()")
