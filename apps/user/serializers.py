from .models import User
from rest_framework import serializers


class DonorAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "pkid",
            "fullName",
            "email",
            "donorID",
            "is_active",
            "is_donor",
            "otp",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self, validated_data):
        user = User.objects.create(
            fullName=validated_data["fullName"],
            email=validated_data["email"],
            is_donor=validated_data["is_donor"],
            donorID=validated_data["donorID"],
        )
        
        user.set_password(validated_data["password"])
        user.save()

        return user


class HospitalAuthSerializer(serializers.ModelSerializer):
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
            "is_hospital",
            "otp",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}
    
        
    def create(self, validated_data):
        user = User.objects.create(
            hospitalName=validated_data["hospitalName"],
            email=validated_data["email"],
            location=validated_data["location"],
            is_hospital=validated_data["is_hospital"],
            hospitalID=validated_data["hospitalID"],
        )
        
        user.set_password(validated_data["password"])
        user.save()

        return user