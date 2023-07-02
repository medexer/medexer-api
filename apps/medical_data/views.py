from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import MedicalTest
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
                    "Donor medical history fetch successfully.",
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