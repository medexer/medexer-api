from .models import *
from rest_framework import serializers

class DonorSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Appointment
		fields = ['pkid','id','date','donor','message','hospital','IsDonated:']
	

	def hospitals(self):
		hospital = User.objects.filter(is_hospital=True)
		return hospital