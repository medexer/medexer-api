from django.shortcuts import render
from . import serializers
from .models import *
from apps.user.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.administrator.models import Notification
from rest_framework.permissions import IsAuthenticated
from apps.common.custom_response import CustomResponse
from .tasks import send_contact_us_mail


class DonorAppointmentViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorAppointmentSerializer

    def get(self, request):
        """
        Allows for a donor to fetch his/her appointments
        """
        try:
            appointment = Appointment.objects.filter(donor=request.user.pkid)

            serializer = self.serializer_class(instance=appointment, many=True)
            return Response(
                data=CustomResponse(
                    "Donor appointments fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-DONOR-APPOINTMENTS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching donor appointment. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            data = {
                # "date": request.data["date"],
                "donor": request.user.pkid,
                "message": request.data["message"],
                "hospital": request.data["hospital"],
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    data=CustomResponse(
                        "Donor appointment created successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured while generating appointment",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[CREATE-APPOINTMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while generating appointment. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_appointment_viewset = DonorAppointmentViewSet.as_view()


class DonationCentersViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonationCenterSerializer

    def get(self, request):
        """
        Allows for a donor to fetch donation centers
        """
        try:
            centers = User.objects.filter(is_hospital=True)

            serializer = self.serializer_class(centers, many=True)

            return Response(
                data=CustomResponse(
                    "Donation centers fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[FETCH-DONATION-CENTERS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching donation centers ",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donation_centers_viewset = DonationCentersViewSet.as_view()


class DonationCenterDetailViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonationCenterSerializer

    def get(self, request, centerId):
        """
        Allows for a donor to fetch a donation center
        """
        try:
            center = User.objects.get(pkid=centerId)

            serializer = self.serializer_class(center)

            return Response(
                data=CustomResponse(
                    "Donation center fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[FETCH-DONATION-CENTER-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching donation center.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donation_center_detail_viewset = DonationCenterDetailViewSet.as_view()


class DonorContactUsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonationCenterSerializer

    def post(self, request):
        """
        Allows for a donor to fetch a donation center
        """
        try:
            donor = User.objects.get(pkid=request.user.pkid)

            send_mail = send_contact_us_mail(
                donor.email,
                request.data["subject"],
                donor.fullName,
                request.data["message"],
            )

            if send_mail:
                return Response(
                    data=CustomResponse(
                        "Contact us mail sent successfully",
                        "SUCCESS",
                        200,
                        None,
                    ),
                    status=status.HTTP_200_OK,
                )
                
            print(f"[SEND-CONTACT-US-MAIL-ERROR]")
            return Response(
                data=CustomResponse(
                    "An error occured while sending contact us mail",
                    "SUCCESS",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(f"[SEND-CONTACT-US-MAIL-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    "An error occured while sending contact us mail",
                    "SUCCESS",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_contact_us_viewset = DonorContactUsViewSet.as_view()




class DonorNotificationsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    def get(self, request):
        try:
            notifications = Notification.objects.filter(recipient=request.user)

            serializer = self.serializer_class(notifications, many=True)

            return Response(
                data=CustomResponse(
                    "Hospital notification fetched successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-NOTIFICATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital notifications. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, notificationId):
        try:
            notification = Notification.objects.get(pkid=notificationId)

            data = {"is_read": True}

            serializer = self.serializer_class(notification, data=data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    data=CustomResponse(
                        "Hospital notification fetched successfully.",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    "An error occured while updating notification unread status.",
                    "ERROR",
                    400,
                    serializer.data,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[UPDATE-NOTIFICATION-STATUS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating notification unread status. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_notifications_viewset = DonorNotificationsViewSet.as_view()
