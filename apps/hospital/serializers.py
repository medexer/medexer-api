from .models import *
from rest_framework import serializers

class InventroySerializer(serializers.ModelSerializer):	
	class Meta:
		model = Inventory
		fields = ["hospitalID","hospital","OPositive","ONegative","ABPositive","ABNegative","APositive","ANegative","BPositive","BNegative"]