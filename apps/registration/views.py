from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.models import User
from apps.common.custom_response import customResponse
from .models import KnowYourBusiness, KnowYourCustomer
from apps.common.validations import registration_validations
from .serializers import DonorKYCSerializer, HospitalKYBSerializer


class DonorKYCViewSet(APIView):
    serializer_class = DonorKYCSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Allows for a donor to process his kyc
        """
        if not registration_validations.validate_donor_kyc_capture(request.data, request.FILES):
            return Response(
                data=customResponse(
                    registration_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            donor = User.objects.get(email=request.user.email)
            kyc = KnowYourCustomer.objects.filter(donorID=donor.donorID).first()

            if kyc:
                return Response(
                    data=customResponse(
                        "Donor KYC already captured",
                        "DUPLICATE-ERROR",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "bloodGroup": request.data["bloodGroup"],
                "genotype": request.data["genotype"],
                "haveDonatedBlood": request.data["haveDonatedBlood"],
                "lastBloodDonationTime": request.data["lastBloodDonationTime"],
                "hasTattos": request.data["hasTattos"],
                "identificationType": request.data["identificationType"],
                "documentUploadCover": request.FILES["documentUploadCover"],
                "documentUploadRear": request.FILES["documentUploadRear"],
                "donorID": donor.donorID,
                "donor": donor.pkid,
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=customResponse(
                        "Donor KYC successfully captured",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data=customResponse(
                    "An error occured while uploading donor kyc.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(f"[DONOR-KYC-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"Failure occurred when uploading donor kyc. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_kyc_viewset = DonorKYCViewSet.as_view()


class HospitalKYBViewSet(APIView):
    serializer_class = HospitalKYBSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Allows for a donor to process his kyc
        """
        if not registration_validations.validate_hospital_kyb_capture(request.data, request.FILES):
            return Response(
                data=customResponse(
                    registration_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            hospital = User.objects.get(hospitalID=request.user.hospitalID)
            kyc = KnowYourBusiness.objects.filter(hospitalID=hospital.hospitalID).first()

            if kyc:
                return Response(
                    data=customResponse(
                        "Hospital KYB already captured",
                        "DUPLICATE-ERROR",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "cacRegistrationID": request.data["cacRegistrationID"],
                "websiteUrl": request.data["websiteUrl"],
                "logo": request.FILES["logo"],
                "address": request.data["address"],
                "description": request.data["description"],
                "identificationType": "CACCERTIFICATE",
                "hospitalID": hospital.hospitalID,
                "hospital": hospital.pkid,
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=customResponse(
                        "Hospital KYB successfully captured",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data=customResponse(
                    "An error occured while uploading hospital kyb.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(f"[HOSPITAL-KYB-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"Failure occurred when uploading hospital kyb. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_kyb_viewset = HospitalKYBViewSet.as_view()
