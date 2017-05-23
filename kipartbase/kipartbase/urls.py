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

#see https://www.machinalis.com/blog/nested-resources-with-django/

#from rest_framework import routers
from rest_framework_nested import routers
from api.views import PartViewSet, PartCategoryViewSet, FootprintViewSet, FootprintCategoryViewSet

router = routers.SimpleRouter()

router.register(r'parts-categories', PartCategoryViewSet, base_name="parts-categories")
router.register(r'parts', PartViewSet, base_name="parts")

router.register(r'footprints-categories', FootprintCategoryViewSet, base_name="footprints-categories")
router.register(r'footprints', FootprintViewSet, base_name="footprints")

print router.urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
