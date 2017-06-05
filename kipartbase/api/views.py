# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, response, exceptions
from rest_framework.response import Response

from django.shortcuts import get_object_or_404, get_list_or_404
import models
import serializers
from django.db.models import Q

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
        print "update: ", request.data, request.query_params
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
        
        if request.query_params.has_key('search'):
            print "Filter by search pattern"
            # add a category filter
            # extract category
            pattern = request.query_params['search']
            parts = parts.filter(
                Q(name__contains=pattern) |
                Q(description__contains=pattern) |
                Q(comment__contains=pattern)
                )

        queryset = parts.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)

    def perform_destroy(self, instance):
        # remove subitems
        models.PartParameter.objects.filter(part=instance).delete()
        models.PartManufacturer.objects.filter(part=instance).delete()
        models.PartDistributor.objects.filter(part=instance).delete()
        #TODO: files
        
        # delete part
        instance.delete()


class FootprintCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.FootprintCategory.objects.all()
    serializer_class = serializers.FootprintCategorySerializer
    
    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        queryset = models.FootprintCategory.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        print "retrieve: ", request.data, request.query_params

        queryset = models.FootprintCategory.objects.all()
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
            current_child = models.FootprintCategory.objects.get(id = child.id)
            current_child.move_to(parent, 'last-child')
        models.Footprint.objects.filter(category=instance.id).update(category=instance.parent)
        # delete category
        instance.delete()
        # cleanup tree inconsistencies
        models.FootprintCategory._tree_manager.rebuild()


class FootprintViewSet(VerboseModelViewSet):
    queryset = models.Footprint.objects.all()
    serializer_class = serializers.FootprintSerializer

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        footprints = models.Footprint.objects
        
        if request.query_params.has_key('category'):
            print "Filter by category"
            # add a category filter
            # extract category
            categories = models.FootprintCategory.objects.get(pk=int(request.query_params['category'])).get_descendants(include_self=True)
            category_ids = [category.id for category in categories]
            parts = footprints.filter(category__in=category_ids)
        
        if request.query_params.has_key('search'):
            print "Filter by search pattern"
            # add a category filter
            # extract category
            pattern = request.query_params['search']
            footprints = footprints.filter(
                Q(name__contains=pattern) |
                Q(description__contains=pattern) |
                Q(comment__contains=pattern)
                )

        queryset = footprints.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)


class PartParameterViewSet(VerboseModelViewSet):
    queryset = models.PartParameter.objects.all()
    serializer_class = serializers.PartParameterSerializer

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        parameters = models.PartParameter.objects
        
        if request.query_params.has_key('part'):
            print "Filter by part"
            # add a category filter
            # extract category
            parameters = parameters.filter(part=int(request.query_params['part']))

        queryset = parameters.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)


class PartManufacturerViewSet(VerboseModelViewSet):
    queryset = models.PartManufacturer.objects.all()
    serializer_class = serializers.PartManufacturerSerializer


class ManufacturerViewSet(VerboseModelViewSet):
    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer


class UnitViewSet(VerboseModelViewSet):
    queryset = models.Unit.objects.all()
    serializer_class = serializers.UnitSerializer

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        parameters = models.Unit.objects
        
        if request.query_params.has_key('symbol'):
            print "Filter by symbol"
            # add a category filter
            # extract category
            parameters = parameters.filter(symbol=request.query_params['symbol'])

        queryset = parameters.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)


class UnitPrefixViewSet(VerboseModelViewSet):
    queryset = models.UnitPrefix.objects.all()
    serializer_class = serializers.UnitPrefixSerializer

    def list(self, request, *args, **kwargs):
        print "list: ", request.data, request.query_params
        parameters = models.UnitPrefix.objects
        
        if request.query_params.has_key('symbol'):
            print "Filter by symbol"
            # add a category filter
            # extract category
            parameters = parameters.filter(symbol=request.query_params['symbol'])

        queryset = parameters.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return response.Response(serializer.data)
