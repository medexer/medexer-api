from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Inventory
from apps.user.models import User
from apps.donor.models import Appointment
from apps.common.custom_response import CustomResponse
from . import serializers  
from .models import *
from apps.administrator.models import *


# Create your views here.
class InventoryListView(generics.GenericAPIView):
    serializer_class = serializers.InventorySerializer
    queryset = Inventory.objects.all()

    def get(self, request):
        inventroy = Inventory.objects.all()
        serializer = self.serializer_class(instance=inventroy, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


inventory_list_viewset = InventoryListView.as_view()


class InventoryListView(generics.GenericAPIView):
    serializer_class = serializers.InventorySerializer
    queryset = Inventory.objects.all()

    def get(self, request, id):
        inventory = get_object_or_404(Inventory, pk=id)
        serializer = self.serializer_class(instance=inventory)
        if serializer.is_valid:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        data = request.data
        instance = Inventory.objects.get(pkid=id)
        serializer = self.serializer_class(instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        inventory = get_object_or_404(Inventory, pk=id)
        inventory.delete()
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)


inventroy_detail_viewset = InventoryListView.as_view()


class CenterListView(generics.GenericAPIView):

    serializer_class = serializers.CenterSerializer
    queryset = User.objects.filter(is_hospital=True)

    def get(self, request):
        centers = User.objects.filter(is_hospital=True)
        serializer = self.serializer_class(instance=centers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


center_list_viewset = CenterListView.as_view()


class CenterDetailView(generics.GenericAPIView):

    serializer_class = serializers.CenterSerializer
    queryset = User.objects.filter(is_hospital=True)

    def get(self, request, id):
        center = get_object_or_404(User, pk=id)
        serializer = self.serializer_class(instance=center)
        if serializer.is_valid:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, id):
    #     data = request.data
    #     instance = User.objects.get(pkid=id)
    #     serializer = self.serializer_class(instance,data=data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_200_OK)
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


center_detail_viewset = CenterDetailView.as_view()


class AppointmentViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    def get(self, request):
        try:
            appointments = Appointment.objects.filter(hospital=request.user.pkid)

            serializer = self.serializer_class(appointments, many=True)

            return Response(
                data=CustomResponse(
                    "Hospital appointments fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-APPOINTMENTS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital donations. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


appointment_viewset = AppointmentViewSet.as_view()

class GetCenterNotificationView(generics.GenericAPIView):
    
    serializer_class =  serializers.NotificationSerializer
    queryset = Notification.objects.all()

    def get(self,request):    		
        notification = Notification.objects.filter(hospitalID=request.user.hospitalID)
        serializer = self.serializer_class(instance=notification)
        if serializer.is_valid:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

notification_viewset = GetCenterNotificationView.as_view()
