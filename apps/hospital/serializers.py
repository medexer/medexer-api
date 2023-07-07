from .models import *
from django.db.models import Q
from apps.user.models import User
from rest_framework import serializers
from apps.administrator.models import *
from apps.profile.models import Profile
from apps.registration.models import KnowYourCustomer
from apps.donor.models import Appointment, DonationHistory


class DonorSearchSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'pkid',
            'fullName',
            'email',
            'avatar',
            'profile'
        ]

    def get_profile(self, obj):
        profile = Profile.objects.get(user=obj.pkid)
        
        data = {
            "latitude": profile.latitude,
            "longitude": profile.longitude,
            "bloodGroup": profile.bloodGroup,
            "contact_number": profile.contact_number,
            "address": f"{profile.address}, {profile.state}, {profile.city_province}",
        }
        return data

class InventorySerializer(serializers.ModelSerializer):
    recentActivity = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            "id",
            "pkid",
            "hospitalID",
            "hospital",
            "bloodUnits",
            "bloodGroup",
            "recentActivity",
        ]

    def get_recentActivity(self, obj):
        message = ""
        activity = InventoryActivity.objects.filter(Q(bloodGroup=obj.bloodGroup) & Q(hospital=obj.hospital.pkid)).order_by("-pkid").first()

        print(f"[MESSAGE] :: {activity}")

        message = activity.activity if activity else ""

        return message


class InventoryItemSerializer(serializers.ModelSerializer):
    donorName = serializers.SerializerMethodField()
    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "pkid",
            "bloodGroup",
            "bloodUnits",
            "appointmentID",
            "hospitalID",
            "donor",
            "donorName",
            "inventory",
        ]

    def get_donorName(self, obj):
        donor = User.objects.get(pkid=obj.donor.pkid)

        return donor.fullName


class InventoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryActivity
        fields = [
            "id",
            "pkid",
            "activity",
            "hospital",
            "bloodGroup",
        ]


class CenterSerializer(serializers.ModelSerializer):
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


class AppointmentSerializer(serializers.ModelSerializer):
    donorInfo = serializers.SerializerMethodField()
    recentActivity = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "pkid",
            "date",
            "donor",
            "pints",
            "donationDate",
            "isPaid",
            "isDonated",
            "donorInfo",
            "hospital",
            "message",
            "recentActivity",
        ]

    def get_donorInfo(self, obj):
        donor = User.objects.get(pkid=obj.donor.pkid)
        profile = Profile.objects.get(user=obj.donor.pkid)
        donorKyc = KnowYourCustomer.objects.get(donor=obj.donor.pkid)

        data = {
            "id": donor.id,
            "pkid": donor.pkid,
            "userAvatar": profile.userAvatar.url,
            "donorId": donor.donorID,
            "email": donor.email,
            "fullName": donor.fullName,
            "bloodGroup": donorKyc.bloodGroup,
            "haveDonatedBlood": donorKyc.haveDonatedBlood,
            "lastBloodDonationTime": donorKyc.lastBloodDonationTime,
            "tobaccoUsage": donorKyc.tobaccoUsage,
            "isRecentVaccineRecipient": donorKyc.isRecentVaccineRecipient,
            "hasTattos": donorKyc.hasTattos,
            "created_at": donorKyc.created_at,
        }

        return data

    def get_recentActivity(self, obj):
        message = ""
        try:
            activity = DonationHistory.objects.filter(donor=obj.donor.pkid).first()

            # print(f"[MESSAGE] :: {activity}")

            message = activity.message if activity else ""
            return message
        except DonationHistory.DoesNotExist:
            return message


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "pkid",
            "notificationType",
            "recipient",
            "author",
            "title",
            "message",
            "is_read",
            "created_at",
        ]


class HospitalComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            "id",
            "pkid",
            "title",
            "status",
            "complaintID",
            # "message",
            "hospital",
            "hospitalID",
            "created_at",
        ]


class HospitalComplaintHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintHistory
        fields = [
            "id",
            "pkid",
            "headline",
            "message",
            "complaint",
            "updateType",
            "author",
            "created_at",
        ]
