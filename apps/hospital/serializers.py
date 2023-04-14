from .models import *
from rest_framework import serializers
from apps.user.models import User
from apps.administrator.models import *

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


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model= Notification
        fields = ['message','notificationType','id','userID','author','hospitalID']