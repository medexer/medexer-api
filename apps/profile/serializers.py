from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'pkid',
            'latitude',
            'longitude',
            'address',
            'state',
            'about_hospital',
            'city_province',
            'contact_number',
            'occupation',
            'marital_status',
            'userAvatar',
            'hospitalImage',
            'hospitalLogo',
            'user',
        ]


class DonorProfileLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'pkid',
            'latitude',
            'longitude',
        ]