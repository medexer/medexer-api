from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Inventory
from apps.user.models import User
from . import serializers
from .models import *
from django.db.models import Q
from apps.administrator.models import *
from apps.donor.models import Appointment, DonationHistory
from apps.common.custom_response import CustomResponse, CurrentTimeStamp


class InventoryItemHistoryViewSet(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventoryHistorySerializer

    def get(self, request, bloodGroup):
        try:
            inventory = InventoryActivity.objects.filter(
                Q(bloodGroup=bloodGroup) & Q(hospital=request.user.pkid)
            )

            serializer = self.serializer_class(instance=inventory, many=True)

            return Response(
                data=CustomResponse(
                    f"Fetched hospital inventory item activity successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-INVENTORY-ACTIVITY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching inventory item activity. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


inventory_item_history_viewset = InventoryItemHistoryViewSet.as_view()


class InventoryItemViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventorySerializer

    def put(self, request, bloodGroup):
        try:
            activity = ""
            data = {
                "bloodUnits": int(request.data["units"]),
            }

            instance = Inventory.objects.get(
                bloodGroup=bloodGroup, hospital=request.user.pkid
            )

            if instance.bloodUnits < int(data['bloodUnits']):
                activity = f"{request.data['count']} added on {CurrentTimeStamp()}"
            else:
                activity = f"{request.data['count']} removed on {CurrentTimeStamp()}"

            serializer = self.serializer_class(instance, data=data)

            if serializer.is_valid():
                serializer.save()

                InventoryActivity.objects.create(
                    activity=activity,
                    hospital=request.user,
                    bloodGroup=request.data['bloodGroup'],
                )
                
                _serializer = self.serializer_class(instance)
                
                return Response(
                    data=CustomResponse(
                        "Inventory item updated successfully",
                        "SUCCESS",
                        200,
                        _serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured while updating inventory item.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[UPDATE-INVENTORY-ITEM-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching inventory item. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


inventory_item_detail_viewset = InventoryItemViewSet.as_view()

class HospitalInventoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventorySerializer

    def get(self, request):
        try:
            inventoryItems = Inventory.objects.filter(hospital=request.user.pkid)

            serializer = self.serializer_class(instance=inventoryItems, many=True)

            return Response(
                data=CustomResponse(
                    f"Fetched hospital inventory successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-INVENTORY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital inventory. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_inventory_viewset = HospitalInventoryViewSet.as_view()


class CenterListView(generics.GenericAPIView):

    serializer_class = serializers.CenterSerializer
    queryset = User.objects.filter(is_hospital=True)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        centers = User.objects.filter(is_hospital=True)
        serializer = self.serializer_class(instance=centers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


center_list_viewset = CenterListView.as_view()


class CenterDetailView(generics.GenericAPIView):

    serializer_class = serializers.CenterSerializer
    queryset = User.objects.filter(is_hospital=True)
    permission_classes = [IsAuthenticated]

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


class HospitalAppointmentViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    def get(self, request):
        appointments = Appointment.objects.filter(
            Q(hospital=request.user.pkid) & Q(isDonated=False)
        )
        serializer = self.serializer_class(appointments, many=True)

        if serializer.is_valid:
            return Response(
                data=CustomResponse(
                    "Hospital appointments fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=CustomResponse(
                f"An error occured while fetching hospital appointment ",
                "BAD REQUEST",
                400,
                None,
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request, pkid):
        try:
            data = {"date": request.data["date"]}

            instance = Appointment.objects.get(pkid=pkid)
            serializer = self.serializer_class(instance, data=data)
            print(data)
            if serializer.is_valid():
                serializer.save()

                Notification.objects.create(
                    notificationType="DONOR",
                    author=request.user,
                    recipient=instance.donor,
                    message=request.data["message"],
                )

                return Response(
                    data=CustomResponse(
                        "Hospital appointment rescheduled successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured during appointment reschedule",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[RESCHEDULE-APPOINTMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured during appointment reschedule. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_appointment_viewset = HospitalAppointmentViewSet.as_view()


class GetCenterNotificationView(generics.GenericAPIView):
    serializer_class = serializers.NotificationSerializer
    queryset = Notification.objects.all()

    def get(self, request):
        try:
            notification = Notification.objects.filter(recipient=request.user.pkid)
            serializer = self.serializer_class(instance=notification, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"[FETCH-HOSPITAL-NOTIFICATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital notifications. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


notification_viewset = GetCenterNotificationView.as_view()


class DonorDonationHistoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    queryset = Appointment.objects.all()

    def get(self, request, donorId):
        try:
            # appointment = Appointment.objects.get(pkid=pkid)
            donor_activity = DonationHistory.objects.filter(donor=donorId)

            serializer = self.serializer_class(instance=donor_activity, many=True)

            return Response(
                data=CustomResponse(
                    "Donor donation history fetched successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-NOTIFICATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital notifications. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_donation_history_viewset = DonorDonationHistoryViewSet.as_view()


class GetHospitalNotifictionViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    queryset = Notification.objects.all()

    def get(self, request):
        try:
            print(request.user)
            notification = Notification.objects.filter(recipient=request.user)

            serializer = self.serializer_class(instance=notification, many=True)

            return Response(
                data=CustomResponse(
                    "hospital notification fetched successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-NOTIFICATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital notifications. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

hospital_notification_viewset = GetHospitalNotifictionViewSet.as_view()



class UpdateHospitalViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UpdateHospitalSerializer  

    def put(self, request):
        try:       

            instance = User.objects.get(pkid=request.user.pkid)
            serializer = self.serializer_class(instance, data=request.data)
            print(request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=CustomResponse(
                        "Hospital updated successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured during hospital update",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[HOSPITAL-UPDATE-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured during hospital update. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


update_hospital_viewset = UpdateHospitalViewSet.as_view()