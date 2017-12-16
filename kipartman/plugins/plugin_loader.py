#  PLUG in infrastructure 
#  IMPLEMENTED from: # BOMs Away! - BOM/Component manager for KiCad




import pkgutil
import importlib
import inspect

from . import  export_plugins
from . import  import_plugins

def load_export_plugins():
    """ Loads all export plugins stored in kipartman/plugins/export_plugins which
        adhere to the following rules:

        * Must be a base class of KipartmanExporter
        * Must expose an 'export' function
        * Must have class variables: extension, wildcard
    """
    results = []
    for loader, name, is_pkg in pkgutil.walk_packages(export_plugins.__path__):
        # Skip private modules (i.e. base classes)
        if name.startswith('_'):
            continue
        full_name = export_plugins.__name__ + '.' + name
        mod = importlib.import_module(full_name)
        for obj_name in dir(mod):
            obj = getattr(mod, obj_name)
            if not inspect.isclass(obj):
                continue
            baseclass = obj.__bases__[0]

            if not baseclass.__name__ == 'KiPartmanExporter':
                continue

            if not obj().validate():
                continue

            results.append(obj)

    return results

def load_import_plugins():
    """ Loads all import plugins stored in kipartman/plugins/import_plugins which
        adhere to the following rules:

        * Must be a base class of KipartmanImporter
        * Must expose an 'import' function
        * Must have class variables: extension, wildcard
    """
    results = []
    for loader, name, is_pkg in pkgutil.walk_packages(import_plugins.__path__):
        # Skip private modules (i.e. base classes)
        if name.startswith('_'):
            continue
        full_name = import_plugins.__name__ + '.' + name
        mod = importlib.import_module(full_name)
        for obj_name in dir(mod):
            obj = getattr(mod, obj_name)
            if not inspect.isclass(obj):
                continue
            baseclass = obj.__bases__[0]

            if not baseclass.__name__ == 'KiPartmanImporter':
                continue

            if not obj().validate():
                continue

            results.append(obj)

    return results
