from .models import *
from apps.user.models import User
from rest_framework import serializers


class DonorAppointmentSerializer(serializers.ModelSerializer):
    hospitalInfo = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = [
            "pkid",
            "id",
            "date",
            "donor",
            "message",
            "hospital",
            "isDonated",
            "hospitalInfo",
            "created_at",
        ]
        
    def get_hospitalInfo(self, obj):
        hospital = User.objects.get(pkid=obj.hospital.pkid)
        
        data = {
            "pkid": hospital.pkid,
            "hospitalName": hospital.hospitalName,
            "email": hospital.email,
        }
        
        return data


class DonationCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "pkid",
            "hospitalName",
            "email",
            "hospitalID",
            "location",
            "is_active",
        ]
