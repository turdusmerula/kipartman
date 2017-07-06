from django.conf import settings
import django
import os
# #import v10consolidator.settings

#print "Loading django settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swagger_server.controllers.settings")
django.setup()

