from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import MedicalTest
from apps.user.models import User
from apps.donor.models import Appointment
from apps.profile.models import Profile
from apps.common.custom_response import CustomResponse


class DonorMedicalHistoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorMedicalHistorySerializer

    def get(self, request):
        """
        Allows for a donor to fetch his medical history
        """
        try:
            history = MedicalTest.objects.filter(donor=request.user.pkid)

            serializer = self.serializer_class(history, many=True)
            
            return Response(
                data=CustomResponse(
                    "Donor medical history fetched successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[FETCH-DONOR-MEDICAL-HISTORY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    "An error occured while fetching donor medical history.",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_medical_history_viewset = DonorMedicalHistoryViewSet.as_view()


class HospitalMedicalHistoryDonorsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorSerializer

    def get(self, request):
        """
        Allows for a hospital to fetch all donors that have donated blood to their organization
        """
        try:
            donors = []
            
            appointments = Appointment.objects.filter(hospital=request.user.pkid)

            for appointment in appointments:
                donors.append(appointment.donor.pkid)                

            donors_set = list(set(donors))

            users = User.objects.filter(pkid__in=donors_set)

            serializer = self.serializer_class(users, many=True)
            
            return Response(
                data=CustomResponse(
                    "Donors fetched successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[FETCH-DONORS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    "An error occured while fetching donors.",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_medical_history_donors_viewset = HospitalMedicalHistoryDonorsViewSet.as_view()


class DonorRecentAppointmentsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorRecentAppointmentSerializer

    def get(self, request, donor):
        """
        Allows for a hospital to fetch a donors medical history
        """
        try:
            history = Appointment.objects.filter(donor=donor)[:3]

            serializer = self.serializer_class(history, many=True)
            
            return Response(
                data=CustomResponse(
                    "Donor recent donation appointments fetch successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-RECENT-DONOR-APPOINTMENTS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    "An error occured while fetching donor recent donation appointments.",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_recent_appointments_viewset = DonorRecentAppointmentsViewSet.as_view()


class HospitalDonorMedicalHistoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorMedicalHistorySerializer

    def get(self, request, donor):
        """
        Allows for a hospital to fetch a donors medical history
        """
        try:
            history = MedicalTest.objects.filter(donor=donor)

            serializer = self.serializer_class(history, many=True)
            
            return Response(
                data=CustomResponse(
                    "Donor medical history fetch successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(f"[FETCH-DONORS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    "An error occured while fetching donor medical history.",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
    def post(self, request, donor, appointment):
        """
        Allows for a hospital to add a new record of a donors medical data
        """
        try:
            print(f"[DATA] :: {request.data}")
            _donor = User.objects.get(pkid=donor)
            _profile = Profile.objects.get(user=donor)
            _appointment = Appointment.objects.get(pkid=appointment)

            data = {
                "donor": _donor.pkid,
                "appointment": _appointment.pkid,
                "hiv": request.data["hiv"],
                "hepatitisB": request.data["hepatitisB"],
                "hepatitisC": request.data["hepatitisC"],
                "vdrl": request.data["vdrl"],
                "bloodPressure": request.data["bloodPressure"],
                "bodyTemperature": request.data["bodyTemperature"],
                "bloodGroup": request.data["bloodGroup"],
                "genotype": request.data["genotype"],
                "pcv": request.data["pcv"],
                "weight": request.data["weight"],
                "height": request.data["height"],
                "author": request.user.pkid,
            }
           
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()

                _profile.bloodGroup = request.data['bloodGroup']
                _profile.genotype = request.data['genotype']
                _profile.save()

                return Response(
                    data=CustomResponse(
                        "Donor medical test record added successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            print(f"[ADD-DONOR-MEDICAL-TEST-ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    f"An error occured while adding donor medical test record",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[ADD-DONOR-MEDICAL-TEST-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while adding donor medical test record. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )



hospital_donor_medical_history_viewset = HospitalDonorMedicalHistoryViewSet.as_view()