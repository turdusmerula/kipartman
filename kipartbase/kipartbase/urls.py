# -*- coding: utf-8 -*-

"""kipartbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from rest_framework import routers

#see https://www.machinalis.com/blog/nested-resources-with-django/

#from rest_framework import routers
from api.views import PartViewSet, PartCategoryViewSet, PartParameterViewSet, PartManufacturerViewSet, PartDistributorViewSet
from api.views import FootprintViewSet, FootprintCategoryViewSet
from api.views import UnitViewSet, UnitPrefixViewSet
from api.views import ManufacturerViewSet
from api.views import DistributorViewSet

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]


# router = routers.DefaultRouter()
# 
# router.register(r'parts-categories', PartCategoryViewSet, base_name="parts-categories")
# router.register(r'parts', PartViewSet, base_name="parts")
# router.register(r'part-parameters', PartParameterViewSet, base_name="part-parameters")
# router.register(r'part-distributors', PartDistributorViewSet, base_name="part-distributors")
# router.register(r'part-manufacturers', PartManufacturerViewSet, base_name="part-manufacturers")
# 
# router.register(r'footprints-categories', FootprintCategoryViewSet, base_name="footprints-categories")
# router.register(r'footprints', FootprintViewSet, base_name="footprints")
# 
# router.register(r'units', UnitViewSet, base_name="units")
# router.register(r'unitprefixes', UnitPrefixViewSet, base_name="unitprefixes")
# 
# router.register(r'distributors', DistributorViewSet, base_name="distributors")
# router.register(r'manufacturers', ManufacturerViewSet, base_name="manufacturers")
# 
# print router.urls
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^api/footprints/files/(?P<path>.*)$', serve, {
#         'document_root': settings.MEDIA_ROOT,
#     }),
#     url(r'^api/', include(router.urls)),
# ]
