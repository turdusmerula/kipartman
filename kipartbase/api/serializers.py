from rest_framework import serializers, exceptions
import api.models as models

class PartCategorySerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='parts-categories-detail')
    parent = serializers.HyperlinkedRelatedField(
        queryset=models.PartCategory.objects.all(),
        view_name='parts-categories-detail',
        allow_null=True
    )

    default_error_messages = {
        'recursive': 'Category cannot be child of itself.',
    }
    
    class Meta:
        model = models.PartCategory
        fields = ('id', 'path', 'name', 'parent')

    def update(self, instance, validated_data):
        # check that instance will not be child of itself
        parent = validated_data.get('parent', instance.parent)
        while parent is not None:
            if parent.id==instance.id:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
            parent = parent.parent
        return serializers.ModelSerializer.update(self, instance, validated_data)


# class SubPartSerializer(serializers.ModelSerializer, serializers.PrimaryKeyRelatedField):
#     path = serializers.HyperlinkedIdentityField(view_name='parts-detail')
#     category = serializers.HyperlinkedRelatedField(
#         queryset=models.PartCategory.objects.all(),
#         view_name='parts-categories-detail',
#         allow_null=True
#     )
#     footprint = serializers.HyperlinkedRelatedField(
#         queryset=models.Footprint.objects.all(),
#         view_name='footprints-detail',
#         allow_null=True
#     )
#     class Meta:
#         model = models.Part
#         fields = ('id', 'path', 'category', 'name', 'description', 'footprint', 'comment', 'parts')

class PartSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='parts-detail')
    category = serializers.HyperlinkedRelatedField(
        queryset=models.PartCategory.objects.all(),
        view_name='parts-categories-detail',
        allow_null=True
    )
    footprint = serializers.HyperlinkedRelatedField(
        queryset=models.Footprint.objects.all(),
        view_name='footprints-detail',
        allow_null=True
    )
    #parts = SubPartSerializer(many=True, queryset=models.Part.objects.all())

    default_error_messages = {
        'already_in': 'Part already added',
        'recursive': 'Part cannot be child of itself.',
    }

    class Meta:
        model = models.Part
        fields = ('id', 'path', 'category', 'name', 'description', 'footprint', 'comment', 'parts')

    def update(self, instance, validated_data):
        # check there is no recursion
        print "++", instance, "++", validated_data
        subparts = []
        for part in validated_data.get('parts'):
            subparts.append(part)
        while len(subparts)>0:
            subpart = subparts.pop()
            print "--", type(subpart), subpart.pk
            if subpart.pk==instance.pk:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
#            subpart = models.Part.objects.get(pk=subpart_id)
            for part in subpart.parts.all():
                subparts.append(part)
        return super(PartSerializer, self).update(instance, validated_data)


class FootprintCategorySerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='footprints-categories-detail')
    parent = serializers.HyperlinkedRelatedField(
        queryset=models.FootprintCategory.objects.all(),
        view_name='footprints-categories-detail',
        allow_null=True
    )

    default_error_messages = {
        'recursive': 'Category cannot be child of itself.',
    }
    
    class Meta:
        model = models.FootprintCategory
        fields = ('id', 'path', 'name', 'parent')

    def update(self, instance, validated_data):
        # check that instance will not be child of itself
        parent = validated_data.get('parent', instance.parent)
        while parent is not None:
            if parent.id==instance.id:
                raise exceptions.PermissionDenied(self.default_error_messages['recursive'])
            parent = parent.parent
        return serializers.ModelSerializer.update(self, instance, validated_data)


class FootprintSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='footprints-detail')
    category = serializers.HyperlinkedRelatedField(
        queryset=models.FootprintCategory.objects.all(),
        view_name='footprints-categories-detail',
        allow_null=True
    )
    
    class Meta:
        model = models.Footprint
        fields = ('id', 'path', 'category', 'name', 'description', 'comment')
