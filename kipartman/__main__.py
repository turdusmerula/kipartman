#!/usr/bin/python3

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('resources'):
    # we are in an installed package, set new path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import multiprocessing
from threading import Thread

# configure django to use the model
#from django.core.wsgi import get_wsgi_application
#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'kipartbase.settings'
#application = get_wsgi_application()

# configure wxPython
import wx
from frames.main_frame import MainFrame
from helper import kicad_gui_monitor
import sys, time

def sleeper(i):
    print "thread %d sleeps for 5 seconds" % i
    time.sleep(5)
    print "thread %d woke up" % i

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
    
    print "Running kipartman"
    app = wx.App()
    
    frame = MainFrame(None)
    
    frame.Show()
    
    app.MainLoop()


if __name__ == "__main__":
    kcW32eventQueue = multiprocessing.Queue()
    kcW32eventProcessingTread = Thread(target=kicad_gui_monitor.EventProcessor, args=(kcW32eventQueue,))
    kcW32eventProcessingTread.start()

    processKcW32Ew = multiprocessing.Process(target=kicad_gui_monitor.EventWatcher, args=(kcW32eventQueue,))
    #FOR DEBUG -- comment out start and uncomment the following line
    processKcW32Ew.start()
    #kicad_gui_monitor.EventWatcher(kcW32eventQueue)
    main()
    #TODO: Terminate Threads and Process properly
    processKcW32Ew.terminate()
    kcW32eventProcessingTread.terminate()

