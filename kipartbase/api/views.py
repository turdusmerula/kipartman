# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, routers, exceptions, response
from django.shortcuts import get_object_or_404, get_list_or_404
import models
import serializers
import filters
import mptt.models

class VerboseModelViewSet(viewsets.ModelViewSet):
    def get(self, request, *args, **kwargs):
        print "get: ", request.data, request.query_params
        return super(VerboseModelViewSet, self).get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        return super(VerboseModelViewSet, self).list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        print "retrieve: ", request.data, args, kwargs
        return super(VerboseModelViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print "create: ", request.data, args, kwargs
        return super(VerboseModelViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print "get: ", request.data, request.query_params
        return super(VerboseModelViewSet, self).update(request, *args, **kwargs)

class PartCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.PartCategory.objects.all()
    serializer_class = serializers.PartCategorySerializer
#     filter_backends = (filters.CategoryFilterBackend,)
#     filter_fields = ['recursive']
    
    def list(self, request, *args, **kwargs):
        print "list"
        queryset = models.PartCategory.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        print "retrieve", request.query_params

        queryset = models.PartCategory.objects.all()
        if request.query_params.has_key('recursive'):
            category = get_object_or_404(queryset, pk=pk).get_descendants(include_self=True)
            serializer = self.serializer_class(category, many=True, context={'request': request})
        else:
            category = get_object_or_404(queryset, pk=pk)
            serializer = self.serializer_class(category, context={'request': request})
        return response.Response(serializer.data)
    
    def perform_destroy(self, instance):
        # set childrens to parent id
        for child in instance.get_children():
            if instance.is_child_node():
                parent = instance.get_ancestors(ascending=True)[0]
            else:
                parent = None
            current_child = models.PartCategory.objects.get(id = child.id)
            current_child.move_to(parent, 'last-child')
        models.Part.objects.filter(category=instance.id).update(category=instance.parent)
        # delete category
        instance.delete()
        # cleanup tree inconsistencies
        models.PartCategory._tree_manager.rebuild()


class PartViewSet(VerboseModelViewSet):
    queryset = models.Part.objects.all()
    serializer_class = serializers.PartSerializer


class FootprintCategoryViewSet(VerboseModelViewSet):
    queryset = models.FootprintCategory.objects.all()
    serializer_class = serializers.FootprintCategorySerializer
 
    def perform_destroy(self, instance):
        # set childrens to parent id
        models.FootprintCategory.objects.filter(parent=instance.id).update(parent=instance.parent)
        models.Footprint.objects.filter(category=instance.id).update(category=instance.parent)
        instance.delete()
 
class FootprintViewSet(VerboseModelViewSet):
    queryset = models.Footprint.objects.all()
    serializer_class = serializers.FootprintSerializer

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'parts/categories', PartCategoryViewSet, base_name="parts-categories")
router.register(r'parts', PartViewSet, base_name="parts")
router.register(r'footprints/categories', FootprintCategoryViewSet, base_name="footprints-categories")
router.register(r'footprints', FootprintViewSet, base_name="footprints")
