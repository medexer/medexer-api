from .models import *
from apps.user.models import User
from rest_framework import serializers
from apps.administrator.models import *
from apps.registration.models import KnowYourCustomer
from apps.donor.models import Appointment, DonationHistory


class InventorySerializer(serializers.ModelSerializer):
    recentActivity = serializers.SerializerMethodField()
    class Meta:
        model = Inventory
        fields = [
            "id",
            "pk",
            "hospitalID",
            "hospital",
            "bloodUnits",
            "bloodGroup",
            "recentActivity",
        ]

    def get_recentActivity(self, obj):
        message = ""
        activity = InventoryActivity.objects.filter(bloodGroup=obj.bloodGroup).first()

        # print(f"[MESSAGE] :: {activity}")

        message = activity.activity if activity else ""
        
        return message


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
            "donorInfo",
            "hospital",
            "message",
            "recentActivity",
        ]

    def get_donorInfo(self, obj):
        donor = User.objects.get(pkid=obj.donor.pkid)
        donorKyc = KnowYourCustomer.objects.get(donor=obj.donor.pkid)

        data = {
            "id": donor.id,
            "pkid": donor.pkid,
            "fullName": donor.fullName,
            "bloodGroup": donorKyc.bloodGroup,
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
        fields = ["id","recipient", "author"]
