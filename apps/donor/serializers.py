import os, googlemaps
from .models import *
from dotenv import load_dotenv
from apps.user.models import User
from rest_framework import serializers
from apps.hospital.models import Inventory
from apps.administrator.models import Notification

load_dotenv()

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
            "location": hospital.location,
            "email": hospital.email,
        }

        return data


class DonationCenterSerializer(serializers.ModelSerializer):
    centerAddress = serializers.SerializerMethodField()
    inventoryBalance = serializers.SerializerMethodField()
    centerGeoLocation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "pkid",
            "hospitalName",
            "email",
            "hospitalID",
            "is_active",
            "centerAddress",
            "inventoryBalance",
            "centerGeoLocation",
        ]

    def get_centerAddress(self, obj):
        center = User.objects.get(pkid=obj.pkid)

        return f"{center.address}, {center.postalCode}, {center.lga}, {center.state} state."

    def get_inventoryBalance(self, obj):
        balance = 0
        inventoryItems = Inventory.objects.filter(hospital=obj.pkid)

        for item in inventoryItems:
            balance += item.bloodUnits

        return balance

    def get_centerGeoLocation(self, obj):
        data = ""
        gmaps = googlemaps.Client(key=os.getenv("GOOGLEMAP_APIKEY"))
        center = User.objects.get(pkid=obj.pkid)

        geocode_result = gmaps.geocode(
            f"{center.address}, {center.postalCode}, {center.lga}, {center.state}"
        )


        for result in geocode_result:
            print(result)
            data = result["geometry"]["location"]

        return data


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
