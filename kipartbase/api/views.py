# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, routers, exceptions
import models
import serializers


class PartCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.PartCategory.objects.all()
    serializer_class = serializers.PartCategorySerializer

    default_error_messages = {
        'recursive': 'Category cannot be child of itself.',
    }

    def perform_destroy(self, instance):
        # set childrens to parent id
        models.PartCategory.objects.filter(parent=instance.id).update(parent=instance.parent)
        models.Part.objects.filter(category=instance.id).update(category=instance.parent)
        instance.delete()


class PartViewSet(viewsets.ModelViewSet):
    queryset = models.Part.objects.all()
    serializer_class = serializers.PartSerializer


class FootprintCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.FootprintCategory.objects.all()
    serializer_class = serializers.FootprintCategorySerializer
 
    default_error_messages = {
        'constroot': 'Root category element cannot be modified.',
        'recursive': 'Category cannot be child of itself.',
    }
 
    def perform_destroy(self, instance):
        if instance.id==1:
            raise exceptions.PermissionDenied(self.default_error_messages['constroot'])
        # set childrens to parent id
        models.FootprintCategory.objects.filter(parent=instance.id).update(parent=instance.parent)
        models.Footprint.objects.filter(category=instance.id).update(category=instance.parent)
        instance.delete()
 
class FootprintViewSet(viewsets.ModelViewSet):
    queryset = models.Footprint.objects.all()
    serializer_class = serializers.FootprintSerializer

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'parts/categories', PartCategoryViewSet, base_name="parts-categories")
router.register(r'parts', PartViewSet, base_name="parts")
router.register(r'footprints/categories', FootprintCategoryViewSet, base_name="footprints-categories")
router.register(r'footprints', FootprintViewSet, base_name="footprints")
