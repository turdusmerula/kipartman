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

class PartParameterSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='part-parameters-detail')
    part = serializers.HyperlinkedRelatedField(
        queryset=models.Part.objects.all(),
        view_name='parts-detail',
        allow_null=True
    )
    unit = serializers.HyperlinkedRelatedField(
        queryset=models.Unit.objects.all(),
        view_name='units-detail',
        allow_null=True
    )
    min_prefix = serializers.HyperlinkedRelatedField(
        queryset=models.UnitPrefix.objects.all(),
        view_name='unitprefixes-detail',
        allow_null=True
    )
    nom_prefix = serializers.HyperlinkedRelatedField(
        queryset=models.UnitPrefix.objects.all(),
        view_name='unitprefixes-detail',
        allow_null=True
    )
    max_prefix = serializers.HyperlinkedRelatedField(
        queryset=models.UnitPrefix.objects.all(),
        view_name='unitprefixes-detail',
        allow_null=True
    )
    class Meta:
        model = models.PartParameter
        fields = ('id', 'path', 'part', 'name', 'description', 'unit', 'numeric', 'text_value', 'min_value', 'min_prefix', 'nom_value', 'nom_prefix', 'max_value', 'max_prefix')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('id', 'name')


class PartManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartManufacturer
        fields = ('id', 'manufacturer', 'part_name')


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distributor
        fields = ('id', 'name')


class PartDistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartDistributor
        fields = ('id', 'distributor', 'packaging_unit', 'item_price', 'currency', 'package_price', 'sku')


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
    parameters = PartParameterSerializer(
        many=True,
        read_only=True
    )
    distributors = PartDistributorSerializer(
        many=True,
        read_only=True
    )
    manufacturers = PartManufacturerSerializer(
        many=True,
        read_only=True
    )

    default_error_messages = {
        'already_in': 'Part already added',
        'recursive': 'Part cannot be child of itself.',
    }

    class Meta:
        model = models.Part
        fields = ('id', 'path', 'category', 'name', 'description', 'footprint', 'comment', 'parts', 'parameters', 'distributors', 'manufacturers')

    def update(self, instance, validated_data):
        # check there is no recursion
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


class UnitSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='units-detail')
    class Meta:
        model = models.Unit
        fields = ('id', 'path', 'name', 'symbol')


class UnitPrefixSerializer(serializers.ModelSerializer):
    path = serializers.HyperlinkedIdentityField(view_name='unitprefixes-detail')
    class Meta:
        model = models.UnitPrefix
        fields = ('id', 'path', 'name', 'symbol', 'power')
