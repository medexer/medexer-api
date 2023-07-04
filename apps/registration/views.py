import os, googlemaps
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
from apps.user.models import User
from apps.common.custom_response import CustomResponse
from .models import KnowYourBusiness, KnowYourCustomer
from apps.common.validations import registration_validations
from .serializers import DonorKYCSerializer, HospitalKYBSerializer
from apps.user.serializers import HospitalAuthSerializer, DonorAuthSerializer
from apps.profile.models import Profile

load_dotenv()

class DonorKYCViewSet(APIView):
    serializer_class = DonorKYCSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Allows for a donor to process his kyc
        """
        # if not registration_validations.validate_donor_kyc_capture(
        #     request.data, request.FILES
        # ):
        #     print(f"[DONOR-KYC-ERROR] :: ")
        #     return Response(
        #         data=CustomResponse(
        #             registration_validations.validation_message,
        #             "BAD REQUEST",
        #             400,
        #             None,
        #         ),
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        try:
            donor = User.objects.get(email=request.user.email)
            kyc = KnowYourCustomer.objects.filter(donorID=donor.donorID).first()

            print(request.data)

            if kyc:
                return Response(
                    data=CustomResponse(
                        "Donor KYC already captured",
                        "DUPLICATE-ERROR",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "bloodGroup": request.data["bloodGroup"] if request.data["bloodGroup"] else None,
                "genotype": request.data["genotype"] if request.data["genotype"] else None,
                "haveDonatedBlood": request.data["haveDonatedBlood"],
                "lastBloodDonationTime": request.data["lastBloodDonationTime"],
                "hasTattos": request.data["hasTattos"],
                "tobaccoUsage": request.data["tobaccoUsage"],
                "isRecentVaccineRecipient": request.data["isRecentVaccineRecipient"],
                "identificationType": request.data["identificationType"],
                "documentUploadCover": request.FILES["documentUploadCover"],
                "documentUploadRear": request.FILES["documentUploadRear"],
                "donorID": donor.donorID,
                "donor": donor.pkid,
            }

            serializer = self.serializer_class(data=data)
            _serializer = DonorAuthSerializer(donor)

            if serializer.is_valid():
                serializer.save()
                
                donor.is_kyc_updated = True
                donor.save()

                return Response(
                    data=CustomResponse(
                        "Donor KYC successfully captured",
                        "SUCCESS",
                        201,
                        {
                            "data": serializer.data,
                            "user": _serializer.data,
                        },
                    ),
                    status=status.HTTP_201_CREATED,
                )
            print(f"[DONOR-KYC-E] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    "An error occured while uploading donor kyc.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(f"[DONOR-KYC-ERROR] ::: {e}")
            return Response(
                data=CustomResponse(
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
        if not registration_validations.validate_hospital_kyb_capture(
            request.data, request.FILES
        ):
            return Response(
                data=CustomResponse(
                    registration_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            gmaps = googlemaps.Client(key=os.getenv("GOOGLEMAP_APIKEY"))
            
            profile = Profile.objects.get(user=request.user.pkid)
            hospital = User.objects.get(hospitalID=request.user.hospitalID)
            kyc = KnowYourBusiness.objects.filter(
                hospitalID=hospital.hospitalID
            ).first()

            # print(f'[DATA] :: {request.data}')
        
            if kyc:
                return Response(
                    data=CustomResponse(
                        "Hospital KYB already captured",
                        "DUPLICATE-ERROR",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "cacRegistrationID": request.data["cacRegistrationID"],
                "websiteUrl": request.data["websiteUrl"]
                if request.data["websiteUrl"]
                else "",
                # "logo": request.FILES["logo"],
                "address": request.data["address"],
                "state": request.data["state"],
                "city": request.data["city_province"],
                "business_type": request.data["business_type"],
                "incorporation_date": request.data["incorporation_date"],
                "description": request.data["description"],
                "identificationType": "CACCERTIFICATE",
                "hospitalID": hospital.hospitalID,
                "hospital": hospital.pkid,
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                
                geoData = ""
                geocode_result = gmaps.geocode(
                    f"{request.data['address']}, {hospital.postalCode}, {request.data['city_province']}, {request.data['state']}"
                )

                for result in geocode_result:
                    geoData = result["geometry"]["location"]
                
                print(f'[DATA]  ::  {geoData}')
                
                hospital.is_kyc_updated = True
                hospital.city = request.data["city_province"]
                hospital.state = request.data["state"]
                hospital.address = request.data["address"]
                hospital.save()
                
                profile.latitude = geoData['lat']
                profile.longitude = geoData['lng']
                profile.state = request.data["state"]
                profile.address = request.data["address"]
                profile.city_province = request.data["city_province"]
                profile.about_hospital = request.data["description"]
                profile.hospitalImage = request.FILES['hospitalImage']
                profile.save()
                
                hospital_serializer = HospitalAuthSerializer(hospital)

                return Response(
                    data=CustomResponse(
                        "Hospital KYB successfully captured",
                        "SUCCESS",
                        201,
                        {
                            "data": serializer.data,
                            "hospital": hospital_serializer.data,
                        },
                    ),
                    status=status.HTTP_201_CREATED,
                )
                
            print(f"[HOSPITAL-KYB-ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
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
                data=CustomResponse(
                    f"Failure occurred when uploading hospital kyb. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_kyb_viewset = HospitalKYBViewSet.as_view()
