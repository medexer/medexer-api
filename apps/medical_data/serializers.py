from rest_framework import serializers
from .models import MedicalTest
from apps.user.models import User
from apps.donor.models import Appointment


class DonorMedicalHistorySerializer(serializers.ModelSerializer):
    hospitalProfile = serializers.SerializerMethodField()
    appointmentInfo = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicalTest
        fields = [
            "id",
            "pkid",
            "hiv",
            "hepatitisB",
            "hepatitisC",
            "vdrl",
            "bloodPressure",
            "bodyTemperature",
            "bloodGroup",
            "genotype",
            "pcv",
            "weight",
            "height",
            "donor",
            "hospitalProfile",
            "appointment",
            "appointmentInfo",
            "author",
            "created_at",
        ]
        
    def get_hospitalProfile(self, obj):
        hospital = User.objects.get(pkid=obj.author.pkid)
        
        data = {
            "email": hospital.email,
            "hospitalName": hospital.hospitalName,
        }
        
        return data
   
    def get_appointmentInfo(self, obj):
        appointment = Appointment.objects.get(pkid=obj.appointment.pkid)
        
        data = {
            "donationDate": appointment.donationDate,
            "appointmentID": appointment.appointmentID,
        }
        
        return data

