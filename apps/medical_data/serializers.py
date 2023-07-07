from rest_framework import serializers
from .models import MedicalTest
from apps.user.models import User
from apps.profile.models import Profile
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
        profile = Profile.objects.get(user=obj.author.pkid)
        
        data = {
            "email": hospital.email,
            "hospitalName": hospital.hospitalName,
            "hospitalLogo": profile.hospitalLogo.url,
        }
        
        return data
   
    def get_appointmentInfo(self, obj):
        appointment = Appointment.objects.get(pkid=obj.appointment.pkid)
        
        data = {
            "donationDate": appointment.donationDate,
            "appointmentID": appointment.appointmentID,
        }
        
        return data


class DonorSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'pkid',
            'fullName',
            'email',
            'avatar',
            'donorID',
            'is_donor',
            'profile',
        ]
        
    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj.pkid)
        
        data = {
            "nationality": profile.nationality,
            "gender": profile.gender,
            "userAvatar": profile.userAvatar.url,
            "religion": profile.religion,
            "address": profile.address,
            "state": profile.state,
            "city_province": profile.city_province,
            "contact_number": profile.contact_number,
        }
        
        return data
    
class DonorRecentAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "pkid",
            "appointmentID",
            "date",
            "donationDate",
        ]