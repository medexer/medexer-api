from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . import serializers  
from .models import *



# Create your views here.
class InventroyListView(generics.GenericAPIView):

    serializer_class = serializers.InventroySerializer
    queryset = Inventory.objects.all()

    def get(self,request):
        inventroy = Inventory.objects.all()
        serializer = self.serializer_class(instance=inventroy,many=True)		
        return Response(data=serializer.data,status=status.HTTP_200_OK)

inventory_list_viewset = InventroyListView.as_view()


class InventroyDetailView(generics.GenericAPIView):
    
    serializer_class = serializers.InventroySerializer
    queryset = Inventory.objects.all()

    def get(self,request,id):    		
        inventory = get_object_or_404(Inventory, pk=id)
        serializer = self.serializer_class(instance=inventory)
        if serializer.is_valid:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        data = request.data	
        instance = Inventory.objects.get(pkid=id)		
        serializer = self.serializer_class(instance,data=data)		
    
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        inventory = get_object_or_404(Inventroy, pk=id)
        inventory.delete()
        return Response(data={'message':'success'}, status=status.HTTP_200_OK)

inventroy_detail_viewset = InventroyDetailView.as_view() 	


class CenterListView(generics.GenericAPIView):
    
    serializer_class =  serializers.CenterSerializer
    queryset = User.objects.filter(is_hospital=True)

    def get(self, request):        
        centers = User.objects.filter(is_hospital=True)
        serializer = self.serializer_class(instance=centers,many=True)		
        return Response(data=serializer.data,status=status.HTTP_200_OK)

center_list_viewset = CenterListView.as_view()