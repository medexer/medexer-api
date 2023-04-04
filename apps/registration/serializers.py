from rest_framework import serializers
from .models import KnowYourBusiness, KnowYourCustomer


class DonorKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowYourCustomer
        
        fields = [
            'id',
            'pkid',
            'bloodGroup',
            'genotype',
            'haveDonatedBlood',
            'lastBloodDonationTime',
            'hasTattos',
            'identificationType',
            'documentUploadCover',
            'documentUploadRear',
            'donorID',
            'donor',
        ]


class HospitalKYBSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowYourBusiness
        
        fields = [
            'id',
            'pkid',
            'cacRegistrationID',
            'websiteUrl',
            'logo',
            'address',
            'description',
            'identificationType',
            'hospitalID',
            'hospital',
        ]