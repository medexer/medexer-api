import os, googlemaps
from . import serializers
from .models import *
from dotenv import load_dotenv
from django.db.models import Q
from apps.user.models import User
from django.shortcuts import render
from datetime import datetime, timedelta
from rest_framework import generics, status
from rest_framework.response import Response

from .tasks import send_contact_us_mail
from apps.profile.models import Profile
from apps.hospital.models import Inventory
from apps.administrator.models import Notification
from rest_framework.permissions import IsAuthenticated
from apps.common.custom_response import CustomResponse
from apps.common.id_generator import appointment_id_generator


load_dotenv()

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
            # donor = User.objects.get(pkid=request.user.pkid)
            last_appointment = Appointment.objects.filter(Q(donor=request.user.pkid)).first()
            
            if last_appointment:
                if last_appointment and datetime.now().date() > (last_appointment.donationDate + timedelta(days=3*30)):
                    data = {
                        "donor": request.user.pkid,
                        "message": request.data["message"],
                        "hospital": request.data["hospital"],
                        "isForAdult": request.data["isForAdult"],
                        "getNotifiedOnBloodUse": request.data["getNotifiedOnBloodUse"],
                        "appointmentID": appointment_id_generator(),
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
                            f"An error occured while booking appointment",
                            "BAD REQUEST",
                            400,
                            serializer.errors,
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(
                    data=CustomResponse(
                        f"You are still in you recovery period, please try again after three months from your last donation which is {last_appointment.donationDate}",
                        f"You are still in you recovery period, please try again after three months from your last donation which is {last_appointment.donationDate}",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                data = {
                    "donor": request.user.pkid,
                    "message": request.data["message"],
                    "hospital": request.data["hospital"],
                    "isForAdult": request.data["isForAdult"],
                    "getNotifiedOnBloodUse": request.data["getNotifiedOnBloodUse"],
                    "appointmentID": appointment_id_generator(),
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
                        f"An error occured while booking appointment",
                        "An error occured while booking appointment",
                        400,
                        serializer.errors,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(f"[CREATE-APPOINTMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while booking appointment. {e}",
                    "An error occured while booking appointment",
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
            query_set = []
            profile = Profile.objects.get(user=request.user.pkid)
            centers = User.objects.filter(Q(is_hospital=True) & Q(is_kyc_updated=True))
            
            if profile.bloodGroup is not None:
                for center in centers:
                    inventory = Inventory.objects.get(Q(hospital=center.pkid) & Q(bloodGroup=profile.bloodGroup))
                    
                    if inventory.bloodUnits < 20:
                        query_set.append(center)

                # serializer = self.serializer_class(centers, many=True)
                serializer = self.serializer_class(query_set, many=True)

                print('[CROSS-MATCH-SUCCESS]')
                return Response(
                    data=CustomResponse(
                        "Donation centers fetched successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                serializer = self.serializer_class(centers, many=True)

                print('- [CROSS-MATCH-SUCCESS]')
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


class DonationCentersLocationDataViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Allows for a donor to fetch the location data for all donation centers
        """
        try:
            geocodeData = []

            gmaps = googlemaps.Client(key=os.getenv("GOOGLEMAP_APIKEY"))

            donation_centers = User.objects.filter(Q(is_hospital=True) & Q(is_kyc_updated=True))
            # _geocode_result = gmaps.geocode("VV28+HM9, 930103, Jos, Plateau")

            for center in donation_centers:
                if center.is_kyc_updated == True:
                    profile = Profile.objects.get(user=center.pkid)
                    _center_geocode_result = gmaps.geocode(
                        f"{center.address}, {center.postalCode}, {center.lga}, {center.state}"
                    )
                    # print(f"{center.address}, {center.postalCode}, {center.lga}, {center.state}")
                    # print(_center_geocode_result)
                    for result in _center_geocode_result:
                        # print(result)
                        geocodeData.append(
                            {
                                "centerName": center.hospitalName,
                                "email": f"{center.email}",
                                "hospitalImage": profile.hospitalImage.url if profile.hospitalImage else None,
                                "address": f"{center.address}, {center.postalCode}, {center.lga}, {center.state} state.",
                                "location": result["geometry"]["location"],
                            }
                        )
                        # print(geocodeData)

            # print(f"[GEO] :: {geocodeData}")
            return Response(
                data=CustomResponse(
                    "Donation center fetched successfully",
                    "SUCCESS",
                    200,
                    geocodeData,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[FETCH-DONATION-CENTER-GEO-LOCATION-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching donation center geo-location.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donation_centers_location_data_viewset = DonationCentersLocationDataViewSet.as_view()


class SearchDonationCentersViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonationCenterSerializer
    
    def get(self, request):
        """
        Allows for a donor to fetch the location data for all donation centers
        """
        try:
            query = self.request.GET.get('query', None)
            centers = User.objects.filter(
                Q(hospitalName__icontains=query)
                | Q(address__icontains=query)
                | Q(lga__icontains=query)
                | Q(state__icontains=query)
                | Q(postalCode__icontains=query)
            )

            serializer = self.serializer_class(centers, many=True)

            return Response(
                data=CustomResponse(
                    "Search successful",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[SEARCH-DONATION-CENTERS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while searching donation centers.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


search_donation_centers_viewset = SearchDonationCentersViewSet.as_view()


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
            notifications = Notification.objects.filter(Q(recipient=request.user) | Q(recipients=request.user))

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
