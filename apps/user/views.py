from django.shortcuts import render

from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .tasks import send_forgotpassword_mail
from apps.common.validations import auth_validations
from apps.common.custom_response import customResponse
from .serializers import DonorAuthSerializer, HospitalAuthSerializer
from apps.common.id_generator import (
    donor_id_generator,
    otp_id_generator,
    hospital_id_generator,
)


class DonorSignUpViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def post(self, request):
        """
        Allows for a donor to signup
        """
        if not auth_validations.validate_donor_signup(request.data):
            return Response(
                data=customResponse(
                    auth_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            donorID = donor_id_generator()
            users = User.objects.all()

            for user in users:
                if user.donorID == donorID:
                    donorID = donor_id_generator()

            print(f"[DONOR-ID] :: {donorID}")

            data = {
                "is_donor": True,
                "donorID": donorID,
                "email": request.data["email"],
                "fullName": request.data["fullName"],
                "password": request.data["password"],
            }

            print(f"[DATA] :: {data}")

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=customResponse(
                        "Donor signup successful",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data=customResponse(
                    "An error occured during donor signup.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[DONOR-SIGNUP-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"An error occured during donor signup. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_signup_viewset = DonorSignUpViewSet.as_view()


class DonorSignInViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def post(self, request):
        """
        Allows for a donor to login
        """
        if not auth_validations.validate_donor_signin(request.data):
            return Response(
                data=customResponse(
                    auth_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.filter(Q(email=request.data["email"].strip())).first()

            if user is None:
                return Response(
                    data=customResponse(
                        "Donor is not registered",
                        "NOT-FOUND",
                        400,
                        None,
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not user.check_password(request.data["password"]):
                return Response(
                    data=customResponse(
                        "Unauthorized",
                        "INVALID-CREDENTIALS",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refresh__token = RefreshToken.for_user(user)
            access__token = "Bearer " + str(refresh__token.access_token)

            serializer = self.serializer_class(user)

            return Response(
                data=customResponse(
                    "Donor login successful",
                    "SUCCESS",
                    200,
                    data={
                        "user": serializer.data,
                        "access": access__token,
                        "refresh": str(refresh__token),
                    },
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[DONOR-LOGIN-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"An error occured during donor login. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_signin_viewset = DonorSignInViewSet.as_view()


class DonorForgotPasswordViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def put(self, request):
        """
        Allows for a donor to generate a forgot password token
        """
        if not auth_validations.validate_donor_forgotpassword(request.data):
            return Response(
                data=customResponse(
                    auth_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=request.data["email"])

            user.otp = otp_id_generator()
            user.save()

            send_forgotpassword_mail.delay(user.email, user.otp)

            return Response(
                data=customResponse(
                    "Email successfully sent",
                    "SUCCESS",
                    200,
                    None,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[DONOR-FORGOT-PASSWORD-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"Failure occurred during donor forgot password. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_forgotpassword_viewset = DonorForgotPasswordViewSet.as_view()


class DonorResetPasswordViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def put(self, request):
        """
        Allows for a donor to generate a forgot password token
        """
        if not auth_validations.validate_donor_resetpassword(request.data):
            return Response(
                data=customResponse(
                    auth_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(otp=request.data["otp"])

            user.set_password(request.data["newPassword"])
            user.otp = None
            user.save()

            return Response(
                data=customResponse(
                    "Password reset successfully",
                    "SUCCESS",
                    200,
                    None,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[DONOR-RESET-PASSWORD-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"Failure occurred during donor reset password. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_resetpassword_viewset = DonorResetPasswordViewSet.as_view()


class HospitalSignUpViewSet(APIView):
    serializer_class = HospitalAuthSerializer

    def post(self, request):
        """
        Allows for a hospital to signup
        """
        if not auth_validations.validate_hospital_signup(request.data):
            return Response(
                data=customResponse(
                    auth_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            hospitalID = hospital_id_generator()
            users = User.objects.all()

            for user in users:
                if user.hospitalID == hospitalID:
                    hospitalID = hospital_id_generator()

            data = {
                "is_hospital": True,
                "hospitalID": hospitalID,
                "email": request.data["email"],
                "location": request.data["location"],
                "password": request.data["password"],
                "hospitalName": request.data["hospitalName"],
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=customResponse(
                        "Hospital signup successful",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data=customResponse(
                    "An error occured during hospital signup.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[HOSPITAL-SIGNUP-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"An error occured during hospital signup. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_signup_viewset = HospitalSignUpViewSet.as_view()


class HospitalSignInViewSet(APIView):
    serializer_class = HospitalAuthSerializer

    def post(self, request):
        """
        Allows for a hospital to login
        """
        if not auth_validations.validate_hospital_signin(request.data):
            return Response(
                data=customResponse(
                    auth_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            hospital = User.objects.filter(
                Q(email=request.data["email"].strip())
                & Q(hospitalID=request.data["hospitalID"].strip())
            ).first()

            if hospital is None:
                return Response(
                    data=customResponse(
                        "Hospital is not registered",
                        "NOT-FOUND",
                        400,
                        None,
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not hospital.check_password(request.data["password"]):
                return Response(
                    data=customResponse(
                        "Unauthorized",
                        "INVALID-CREDENTIALS",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refresh__token = RefreshToken.for_user(hospital)
            access__token = "Bearer " + str(refresh__token.access_token)

            serializer = self.serializer_class(hospital)

            return Response(
                data=customResponse(
                    "Hospital login successful",
                    "SUCCESS",
                    200,
                    data={
                        "hospital": serializer.data,
                        "access": access__token,
                        "refresh": str(refresh__token),
                    },
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[HOSPITAL-LOGIN-ERROR] :: {e}")
            return Response(
                data=customResponse(
                    f"An error occured during hospital login. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_signin_viewset = HospitalSignInViewSet.as_view()


def geeks_view(request):
    return render(request, "user/forgotpassword.html")
