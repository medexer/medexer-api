from .models import *
from rest_framework import serializers
from apps.user.models import User
from apps.registration.models import KnowYourCustomer
from apps.donor.models import Appointment, DonationActivity
from apps.administrator.models import *


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            "id",
            "pk",
            "hospitalID",
            "hospital",
            "OPositive",
            "ONegative",
            "ABPositive",
            "ABNegative",
            "APositive",
            "ANegative",
            "BPositive",
            "BNegative",
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
    # donorInfo = serializers.SerializerMethodField()
    # recentActivity = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "pkid",
            "date",
            "donor",
            # "donorInfo",
            "hospital",
            "message",
            # "recentActivity",
        ]

    # def get_donorInfo(self, obj):
    #     donor = User.objects.get(pkid=obj.donor.pkid)
    #     donorKyc = KnowYourCustomer.objects.get(donor=obj.donor.pkid)

    #     data = {
    #         "id": donor.id,
    #         "pkid": donor.pkid,
    #         "fullName": donor.fullName,
    #         "bloodGroup": donorKyc.bloodGroup,
    #     }

    #     return data

    # def get_recentActivity(self, obj):
    #     message = ""
    #     activity = DonationActivity.objects.filter(appointment=obj.pkid).first()

    #     if activity:
    #         message = activity.message

    #     return message


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["message", "notificationType", "id", "userID", "author", "hospitalID"]
