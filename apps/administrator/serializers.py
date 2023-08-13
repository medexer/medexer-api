from apps.user.models import User
from rest_framework import serializers
from apps.donor.models import Appointment
from apps.registration.models import KnowYourBusiness, KnowYourCustomer
from .models import Integration, Complaint, ComplaintHistory, Notification, PaymentHistory
from apps.profile.models import Profile

# GLOBAL
exists = False

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = [
            'id',
            'pkid',
            'organization',
            'email',
            'accessKey',
            'address',
            'state',
            'cac_id',
            'is_approved',
            'created_at',
        ]


class HospitalSerializer(serializers.ModelSerializer):
    profile_info = serializers.SerializerMethodField()
    registration_info = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'pkid',
            'email',
            'hospitalName',
            'hospitalID',
            'address',
            'state',
            'lga',
            'is_approved',
            'is_blocked',
            'postalCode',
            'registration_info',
            'profile_info',
        ]
        
    def get_registration_info(self, obj):
        ids = []
        
        hospital_kybs = KnowYourBusiness.objects.all()
        
        for kyb in hospital_kybs:   
            ids.append(kyb.hospital.pkid)
        
        # print(f'[EXISTS] :: {ids} {type(ids)}')    
        # print(f'[EXISTS] :: {obj.pkid} {type(obj.pkid)}')    
        # print(f'[EXISTS] :: {obj.pkid in ids}')    
        
        if obj.pkid in ids:
            hospital_kyb = KnowYourBusiness.objects.get(hospital=obj.pkid)
            
            data = {
                "cacRegistrationID" : hospital_kyb.cacRegistrationID if hospital_kyb.cacRegistrationID else None,
                "business_type" : hospital_kyb.business_type if hospital_kyb.business_type else None,
                "incorporation_date" : hospital_kyb.incorporation_date if hospital_kyb.incorporation_date else None,
                "address" : hospital_kyb.address if hospital_kyb.address else None,
                "state" : hospital_kyb.state if hospital_kyb.state else None,
                "city" : hospital_kyb.city if hospital_kyb.city else None,
                "description" : hospital_kyb.description if hospital_kyb.description else None,
            }
            
            return data
        return {}
    
    def get_profile_info(self, obj):
        hospital_profile = Profile.objects.get(user=obj.pkid)
    
        data = {
            "address" : hospital_profile.address if hospital_profile.address else None,
            "state" : hospital_profile.state if hospital_profile.state else None,
            "city_province" : hospital_profile.city_province if hospital_profile.city_province else None,
            "hospitalImage" : hospital_profile.hospitalImage.url if hospital_profile.hospitalImage else None,
        }
        
        return data


class DonorSerializer(serializers.ModelSerializer):
    profile_info = serializers.SerializerMethodField()
    registration_info = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'pkid',
            'email',
            'fullName',
            'donorID',
            'address',
            'state',
            'lga',
            "avatar",
            'postalCode',
            'is_blocked',
            'profile_info',
            'registration_info',
        ]
        
    def get_registration_info(self, obj):
        donor_kyc = KnowYourCustomer.objects.get(donor=obj.pkid)
        
        data = {
            "bloodGroup": donor_kyc.bloodGroup if donor_kyc.bloodGroup else None,
            "genotype": donor_kyc.genotype if donor_kyc.genotype else None,
            "haveDonatedBlood": donor_kyc.haveDonatedBlood if donor_kyc.haveDonatedBlood else None,
            "lastBloodDonationTime": donor_kyc.lastBloodDonationTime if donor_kyc.lastBloodDonationTime else None,
            "hasTattos": donor_kyc.hasTattos if donor_kyc.hasTattos else None,
            "identificationType": donor_kyc.identificationType if donor_kyc.identificationType else None,
            "documentUploadCover": donor_kyc.documentUploadCover.url if donor_kyc.documentUploadCover.url else None,
            "documentUploadRear": donor_kyc.documentUploadRear.url if donor_kyc.documentUploadRear.url else None,
        }
        
        return data
    
    def get_profile_info(self, obj):
        profile = Profile.objects.get(user=obj.pkid)
        
        data = {
            "userAvatar": profile.userAvatar.url,
            "nationality": profile.nationality,
            "state": profile.state,
        }
        
        return data
    
class DonationSerializer(serializers.ModelSerializer):
    donorInfo = serializers.SerializerMethodField()
    hospitalInfo = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            "id",
            "pkid",
            "date",
            "donationDate",
            "pints",
            "donor",
            "donorInfo",
            "hospital",
            "hospitalInfo",
            "message",
        ]

    def get_donorInfo(self, obj):
        donor = User.objects.get(pkid=obj.donor.pkid)
        donorKyc = KnowYourCustomer.objects.get(donor=obj.donor.pkid)

        data = {
            "id": donor.id,
            "pkid": donor.pkid,
            "donorID": donor.donorID,
            "fullName": donor.fullName,
            "bloodGroup": donorKyc.bloodGroup,
        }

        return data

    def get_hospitalInfo(self, obj):
        hospital = User.objects.get(pkid=obj.hospital.pkid)

        data = {
            "hospitalID": hospital.hospitalID,
            "hospitalName": hospital.hospitalName,
        }

        return data


class ComplaintSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    hospitalInfo = serializers.SerializerMethodField()
    
    class Meta:
        model = Complaint
        fields = [
            "id",
            "pkid",
            "title",
            "status",
            "complaintID",
            "hospitalID",
            "hospital",
            "hospitalInfo",
            "message",
            "created_at",
        ]
        
    def get_message(self, obj):
        message = ComplaintHistory.objects.filter(complaint=obj.pkid).first()
        
        return message.message
    
    def get_hospitalInfo(self, obj):
        hospital = User.objects.get(pkid=obj.hospital.pkid)

        data = {
            "hospitalID": hospital.hospitalID,
            "hospitalName": hospital.hospitalName,
        }

        return data


class NotificationSerializer(serializers.ModelSerializer):
    # recipientInfo = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'pkid',
            'notificationType',
            'authorType',
            'title',
            'message',
            'author',
            'recipient',
            'recipients',
            # 'recipientInfo',
            'is_read',
            'created_at',
        ]
        
    # def get_recipientInfo(self, obj):
    #     hospital = User.objects.get(pkid=obj.recipient.pkid)

    #     data = {
    #         "hospitalID": hospital.hospitalID,
    #         "hospitalName": hospital.hospitalName,
    #     }

    #     return data


class CustomerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'pkid',
            'fullName',
            'hospitalName',
            'email',
            'is_donor',
            'is_hospital',
            'donorID',
            'hospitalID',
        ]
        
class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = [
            'id',
            'pkid',
            'amount_paid',
            'payment_date',
            'payment_method',
            'payment_reference',
            'currency',
            'hospital',
            'appointment',
        ]
        
