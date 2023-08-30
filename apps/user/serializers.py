from .models import User
from apps.profile.models import Profile
from rest_framework import serializers


class DonorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "pkid",
            "dateOfBirth",
            "nationality",
            "gender",
            # "religion",
            "address",
            "state",
            "city_province",
            "contact_number",
            "userAvatar",
            "is_profile_updated",
        ]


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
            "avatar",
            "is_donor",
            "is_email_login",
            "otp",
            "password",
            "is_kyc_updated",
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
    
    
class DonorProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "pkid",
            "email",
            # "avatar",
        ]
    
    
class DonorProfileAvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "pkid",
            "userAvatar",
        ]
    
    
class DonorSignupProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "pkid",
            "user",
            "nationality",
            "gender",
            "religion",
            "address",
            "state",
            "city_province",
            "contact_number",
            "is_profile_updated",
        ]


class HospitalAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "pkid",
            "hospitalName",
            "email",
            "hospitalID",
            # "location",
            "address",
            "state",
            # "city",
            "lga",
            "postalCode",
            "is_active",
            "is_hospital",
            "is_approved",
            "otp",
            "password",
            "is_kyc_updated",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(
            hospitalName=validated_data["hospitalName"],
            email=validated_data["email"],
            # location=validated_data["location"],
            address=validated_data["address"],
            state=validated_data["state"],
            # city=validated_data["city"],
            lga=validated_data["lga"],
            postalCode=validated_data["postalCode"],
            is_hospital=validated_data["is_hospital"],
            hospitalID=validated_data["hospitalID"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class HospitalProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "hospitalName",
            "email",
            # "password",
        ]
