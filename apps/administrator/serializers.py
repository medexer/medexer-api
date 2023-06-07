from apps.user.models import User
from rest_framework import serializers
from apps.donor.models import Appointment
from apps.registration.models import KnowYourBusiness, KnowYourCustomer
from .models import Integration, Complaint, ComplaintHistory, Notification


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
            'postalCode',
            'registration_info',
        ]
        
    def get_registration_info(self, obj):
        hospital_kyb = KnowYourBusiness.objects.get(hospital=obj.pkid)
        
        data = {
            "cacRegistrationID": hospital_kyb.cacRegistrationID if hospital_kyb.cacRegistrationID else None,
            "websiteUrl": hospital_kyb.websiteUrl if hospital_kyb.websiteUrl else None,
            "logo": hospital_kyb.logo if hospital_kyb.logo else None,
            "address": hospital_kyb.address if hospital_kyb.address else None,
            "description": hospital_kyb.description if hospital_kyb.description else None,
            "identificationType": hospital_kyb.identificationType if hospital_kyb.identificationType else None,
        }
        
        return data


class DonorSerializer(serializers.ModelSerializer):
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
        
