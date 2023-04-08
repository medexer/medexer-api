from .models import *
from rest_framework import serializers

class DonorSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Appointment
		fields = ['pkid','id','date','donor','message','hospital']
	