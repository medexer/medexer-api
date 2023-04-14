from django.shortcuts import render
from . import serializers
from .models import *
from rest_framework import generics,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class DonorCreateListView(generics.GenericAPIView):
	'''set serializer class and query set'''
	queryset = Appointment.objects.all()
	permission_classes = [IsAuthenticated]
	serializer_class = serializers.DonorSerializer

	def get(self,request):
		try:
			appointment = Appointment.objects.filter(donor=request.user.pkid)
  
			serializer = self.serializer_class(instance=appointment,many=True)		
			return Response(data=CustomResponse("Donor appointments fetched successfully","SUCCESS",200,
						serializer.data,),status=status.HTTP_200_OK,)
		except Exception as e:
			print(f"[FETCH-DONOR-APPOINTMENTS-ERROR] :: {e}")
			return Response(data=CustomResponse(
					f"An error occured while fetching donor appointment. {e}",
					"BAD REQUEST",
					400,
					None,
				),
				status=status.HTTP_400_BAD_REQUEST,
			)

		

	def post(self,request):
		data = request.data
		serializer = self.serializer_class(data=data)
		user = request.user

		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_201_CREATED)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	

donor_create_list_viewset = DonorCreateListView.as_view()


class DonorDetailView(generics.GenericAPIView):
    
	serializer_class = serializers.DonorSerializer
	queryset = Appointment.objects.all()

	def get(self,request,id):    		
		appointment = get_object_or_404(Appointment, pk=id)
		serializer = self.serializer_class(instance=appointment)
		if serializer.is_valid:
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, id):
		data = request.data	
		instance = Appointment.objects.get(pkid=id)		
		serializer = self.serializer_class(instance,data=data)		
			
		if serializer.is_valid():
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
	def delete(self, request, id):
		appointment = get_object_or_404(Appointment, pk=id)
		appointment.delete()
		return Response(data={'message':'success'}, status=status.HTTP_200_OK)


donor_detail_viewset = DonorDetailView.as_view() 	
