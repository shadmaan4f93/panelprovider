from rest_framework import serializers
from task.models import Location, TargetGroup,PanelProvider,Country,LocationGroup





class TargetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetGroup
        fields = ['id','name','parent_id','external_id','secret_code','panel_provider_id']

class TargetWithSubtargetSerializer(serializers.ModelSerializer):
    subtargetgroups = TargetGroupSerializer(many=True, read_only=True)
    class Meta:
        model = TargetGroup
        fields = ['id','name','parent_id','external_id','secret_code','panel_provider_id','subtargetgroups']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id','name','secret_code','external_id')


class LocationGroupSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    class Meta:
        model = LocationGroup
        fields = ['id','name','country_id','panel_provider_id','locations']

class CountrySerializer(serializers.ModelSerializer):
    locationgroups = LocationGroupSerializer(many=True, read_only=True)
    class Meta:
        model = Country
        fields = ['id','name','country_code','panel_provider_id','locationgroups']

class PanelProviderSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    class Meta:
        model = PanelProvider
        fields =['id','code','countries']

class CountryTargetGroupSerializer(serializers.ModelSerializer):
    targetgroups = TargetWithSubtargetSerializer(many=True, read_only=True)
    class Meta:
        model = Country
        fields = ['id','name','country_code','panel_provider_id','targetgroups']

