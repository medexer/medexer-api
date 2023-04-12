from .models import *
from rest_framework import serializers
from apps.user.models import User

class InventroySerializer(serializers.ModelSerializer):	
	class Meta:
		model = Inventory
		fields = ["id","pk","hospitalID","hospital","OPositive","ONegative","ABPositive","ABNegative","APositive","ANegative","BPositive","BNegative"]



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