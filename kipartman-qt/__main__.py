#!/usr/bin/python3

# activate whole application profiling
# see https://toucantoco.com/en/tech-blog/tech/python-performance-optimization
# see https://github.com/what-studio/profiling

import os, sys
# os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

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

def migrate():
    print(sys.path)
    os.environ['DJANGO_SETTINGS_MODULE'] = "database.config.settings"

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(["manage.py", "migrate"])
#    execute_from_command_line(["manage.py", "migrate"])

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

    # set django configuration
    migrate()

    from PyQt6.QtWidgets import QApplication
    from ui.main_window import MainWindow
    
    app = QApplication([])
    # TODO https://github.com/CabbageDevelopment/qasync
    # TODO https://gist.github.com/danieljfarrell/6e94aa6f8c3c437d901fd15b7b931afb
    
    # # register providers
    # import providers.mouser.provider
    # providers.mouser.provider.MouserProvider.register()
    # import providers.octopart.provider_scrap
    # providers.octopart.provider_scrap.OctopartProvider.register()
    # import providers.octopart.provider_api
    # providers.octopart.provider_api.OctopartProvider.register()
    
    global dialog_main
    dialog_main = MainWindow()    
    dialog_main.show()

    app.exec() 

if __name__ == "__main__":

    main()

