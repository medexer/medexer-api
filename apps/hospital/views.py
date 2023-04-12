from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers  
from .models import *


# Create your views here.
class HospitalListView(generics.GenericAPIView):
    serializer_class = serializers.InventroySerializer
    queryset = Inventory.objects.all()

    def get(self,request):
        inventroy = Inventory.objects.all()
        serializer = self.serializer_class(instance=inventroy,many=True)		
        return Response(data=serializer.data,status=status.HTTP_200_OK)

inventory_list_viewset = HospitalListView.as_view()