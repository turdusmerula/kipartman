#from __future__ import print_function
from pcbnew import *
import sys
import zipfile
import os

def convert_mod_to_pretty(src_libpath, dst_libpath):

    src_type = IO_MGR.GuessPluginTypeFromLibPath( src_libpath )
    dst_type = IO_MGR.GuessPluginTypeFromLibPath( dst_libpath )
    
    src_plugin = IO_MGR.PluginFind( src_type )
    dst_plugin = IO_MGR.PluginFind( dst_type )
    
    try:
        dst_plugin.FootprintLibDelete( dst_libpath )
    except:
        None    # ignore, new may not exist if first run
    
    dst_plugin.FootprintLibCreate( dst_libpath )
    
    list_of_parts = src_plugin.FootprintEnumerate( src_libpath )
    
    for part_id in list_of_parts:
        module = src_plugin.FootprintLoad( src_libpath, part_id )
        dst_plugin.FootprintSave( dst_libpath, module )
        
    return dst_libpath, list_of_parts

def convert_mod_to_pretty_zip(src_libpath, dst_libpath):

    src_type = IO_MGR.GuessPluginTypeFromLibPath( src_libpath )
    dst_type = IO_MGR.GuessPluginTypeFromLibPath( dst_libpath )
    
    src_plugin = IO_MGR.PluginFind( src_type )
    dst_plugin = IO_MGR.PluginFind( dst_type )
    
    try:
        dst_plugin.FootprintLibDelete( dst_libpath )
    except:
        None    # ignore, new may not exist if first run
    
    dst_plugin.FootprintLibCreate( dst_libpath )
    
    list_of_parts = src_plugin.FootprintEnumerate( src_libpath )
    
    for part_id in list_of_parts:
        module = src_plugin.FootprintLoad( src_libpath, part_id )
        dst_plugin.FootprintSave( dst_libpath, module )
    
    # create zip file with pretty
    zf = zipfile.ZipFile("%s.zip" % (dst_libpath), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(dst_libpath)
    for dirname, subdirs, files in os.walk(dst_libpath):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename), arcname)
            zf.write(absname, arcname)
    zf.close()
    
    return dst_libpath+".zip"
