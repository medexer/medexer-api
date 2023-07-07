import cloudinary
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import Profile
from apps.user.serializers import DonorProfileSerializer
from apps.common.custom_response import CustomResponse


class HospitalProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfileSerializer
    
    def get(self, request):
        """
        Allows for a hospital to fetch their profile
        """
        try:
            profile = Profile.objects.get(user=request.user.pkid)
            
            serializer = self.serializer_class(profile)

            return Response(
                data=CustomResponse(
                    "Hospital profile fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-PROFILE-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital profile ",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
    def put(self, request):
        """
        Allows for a hospital to update their profile
        """
        try:
            data = {
                "address": request.data['address'],
                "state": request.data["state"],
                "city_province": request.data["city_province"],
                "contact_number": request.data["contact_number"],
                "about_hospital": request.data["about_hospital"],
                # "hospitalImage": request.FILES["hospitalImage"],
            }

            instance = Profile.objects.get(user=request.user.pkid)
            
            serializer = self.serializer_class(instance, data=data)
           
            if serializer.is_valid():
                
                if len(request.FILES) > 0 and 'hospitalImage' in request.FILES:
                    delete_old_file = cloudinary.uploader.destroy(instance.hospitalImagePublicId, resource_type="raw")
                    
                    print(f"[DELETE-OLD-FILE]  :: {delete_old_file}")
                    
                    file = cloudinary.uploader.upload_large(
                        request.FILES["hospitalImage"], folder="Medexer-API/media/hospital-profile/"
                    )

                    serializer.save(hospitalImage=file['secure_url'], hospitalImagePublicId=file['public_id'])
                else:
                    serializer.save()
                    
                if len(request.FILES) > 0 and 'hospitalLogo' in request.FILES:
                    delete_old_file = cloudinary.uploader.destroy(instance.hospitalLogoPublicId, resource_type="raw")
                    
                    print(f"[DELETE-OLD-FILE]  :: {delete_old_file}")
                    
                    file = cloudinary.uploader.upload_large(
                        request.FILES["hospitalLogo"], folder="Medexer-API/media/hospital-profile/"
                    )

                    serializer.save(hospitalLogo=file['secure_url'], hospitaLlogoPublicId=file['public_id'])
                else:
                    serializer.save()
                    
                return Response(
                    data=CustomResponse(
                        "Hospital profile updated successfully.",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured while updating hospital profile.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[UPDATE-HOSPITAL-PROFILE-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating hospital profile. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
hospital_profile_viewset = HospitalProfileViewSet.as_view()


class DonorProfileLocationViewSet(APIView):
    serializer_class = serializers.DonorProfileLocationSerializer
    
    def put(self, request):
        """
        Allows for a donor to update their profile location
        """
        try:
            data = {
                "latitude": request.data['latitude'],
                "longitude": request.data["longitude"],
            }

            instance = Profile.objects.get(user=request.user.pkid)
            
            serializer = self.serializer_class(instance, data=data)
           
            if serializer.is_valid():
                serializer.save()

                return Response(
                    data=CustomResponse(
                        "Donor profile location updated successfully.",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured while updating donor profile location.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[UPDATE-DONOR-PROFILE-LOCATION-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating donor profile location. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
donor_profile_location_viewset = DonorProfileLocationViewSet.as_view()