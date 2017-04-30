from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions

import api.models as models


class PartCategorySerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='parts-categories-detail')
    parent = serializers.HyperlinkedRelatedField(
        queryset=models.PartCategory.objects.all(),
        view_name='parts-categories-detail'
    )

    default_error_messages = {
        'constroot': 'Root category element cannot be modified.',
        'recursive': 'Category cannot be child of itself.',
    }
    
    class Meta:
        model = models.PartCategory
        fields = ('id', 'path', 'name', 'parent')

    def update(self, instance, validated_data):
        print "PartCategorySerializer.update"
        if instance.id==1:
            raise exceptions.PermissionDenied(self.default_error_messages['constroot'])
        # check that instance will not be child of itself
        parent = validated_data.get('parent', instance.parent)
        id = parent.id
        print "id: ", id
        while id>1:
            if id==instance.id:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
            id = parent.parent.id
            parent = parent.parent
        return instance


class PartSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='parts-detail')
    category = serializers.HyperlinkedRelatedField(
        queryset=models.PartCategory.objects.all(),
        view_name='parts-categories-detail'
    )
    footprint = serializers.HyperlinkedRelatedField(
        queryset=models.Footprint.objects.all(),
        view_name='footprints-detail',
        allow_null=True
    )

    class Meta:
        model = models.Part
        fields = ('id', 'path', 'category', 'metapart', 'name', 'description', 'footprint')


class FootprintCategorySerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='footprints-categories-detail')
    parent = serializers.HyperlinkedRelatedField(
        queryset=models.FootprintCategory.objects.all(),
        view_name='footprints-categories-detail'
    )

    default_error_messages = {
        'constroot': 'Root category element cannot be modified.',
        'recursive': 'Category cannot be child of itself.',
    }
    
    class Meta:
        model = models.FootprintCategory
        fields = ('id', 'path', 'name', 'parent')

    def update(self, instance, validated_data):
        if instance.id==1:
            raise exceptions.PermissionDenied(self.default_error_messages['constroot'])
        # check that instance will not be child of itself
        parent = validated_data.get('parent', instance.parent)
        id = parent.id
        print "id: ", id
        while id>1:
            if id==instance.id:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
            id = parent.parent.id
            parent = parent.parent
        return instance


class FootprintSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='footprints-detail')
    category = serializers.HyperlinkedRelatedField(
        queryset=models.FootprintCategory.objects.all(),
        view_name='footprints-categories-detail'
    )
    
    class Meta:
        model = models.Footprint
        fields = ('id', 'path', 'category', 'name', 'description')

