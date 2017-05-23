# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, response
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404
import models
import serializers


class VerboseModelViewSet(viewsets.ModelViewSet):
    def get(self, request, *args, **kwargs):
        print "get: ", request.data, request.query_params
        return super(VerboseModelViewSet, self).get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        return super(VerboseModelViewSet, self).list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        print "retrieve: ", request.data, request.query_params
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
    
    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        queryset = models.PartCategory.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        print "retrieve: ", request.data, request.query_params

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

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        parts = models.Part.objects
        if request.query_params.has_key('category'):
            print "Filter by category"
            # add a category filter
            # extract category
            categories = models.PartCategory.objects.get(pk=int(request.query_params['category'])).get_descendants(include_self=True)
            category_ids = [category.id for category in categories]
            parts = parts.filter(category__in=category_ids)
        queryset = parts.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)


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
