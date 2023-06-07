import os
from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from apps.common.validations import auth_validations
from apps.common.custom_response import CustomResponse
from .tasks import send_forgotpassword_mail, send_hospital_welcome_mail
from apps.common.id_generator import (
    donor_id_generator,
    otp_id_generator,
    hospital_id_generator,
)
from .serializers import (
    DonorAuthSerializer,
    HospitalAuthSerializer,
    HospitalProfileUpdateSerializer,
)



class AdminSignInViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def post(self, request):
        """
        Allows for a donor to login
        """
        if not auth_validations.validate_donor_signin(request.data):
            return Response(
                data=CustomResponse(
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
                    data=CustomResponse(
                        "Admin is not registered",
                        "NOT-FOUND",
                        400,
                        None,
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not user.check_password(request.data["password"]):
                return Response(
                    data=CustomResponse(
                        "Unauthorized",
                        "INVALID-CREDENTIALS",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not user.is_administrator:
                return Response(
                    data=CustomResponse(
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
                data=CustomResponse(
                    "Admin login successful",
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
            print(f"[ADMIN-LOGIN-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured during admin login. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


admin_signin_viewset = AdminSignInViewSet.as_view()


class AdminProfileUpdateViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def patch(self, request):
        """
        Allows for an admin to patch their password
        """
        try:
            user = User.objects.filter(Q(email=request.data["email"].strip())).first()

            data = {
                "email": request.data['email'],
                "fullName": request.data['fullName'],
            }
            
            user.email = request.data['email']
            user.fullName = request.data['fullName']
            user.save()

            serializer = self.serializer_class(user)
            # serializer = self.serializer_class(user, data=data)

            # if serializer.is_valid():
            #     serializer.save()

            return Response(
                data=CustomResponse(
                    "Admin profile update successful",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
            # print(f"[ADMIN-PASSWORD-UPDATE-ERROR] :: {serializer.errors}")
            # return Response(
            #     data=CustomResponse(
            #         f"An error occured during admin password update.",
            #         "BAD REQUEST",
            #         400,
            #         serializer.errors,
            #     ),
            #     status=status.HTTP_400_BAD_REQUEST,
            # )
        except Exception as e:
            print(f"[ADMIN-PASSWORD-UPDATE-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured during admin password update. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


admin_profile_update_viewset = AdminProfileUpdateViewSet.as_view()


class AdminPasswordUpdateViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def patch(self, request):
        """
        Allows for an admin to patch their password
        """
        try:
            user = User.objects.filter(Q(email=request.data["email"].strip())).first()

            if not user.check_password(request.data["currentPassword"]):
                return Response(
                    data=CustomResponse(
                        "Unauthorized",
                        "INVALID-CREDENTIALS",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print(f"[PASSWORD] :: {request.data['newPassword']}")
            user.set_password(request.data['newPassword'])
            user.save()
    
            return Response(
                data=CustomResponse(
                    "Admin password update successful",
                    "SUCCESS",
                    200,
                    None,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[ADMIN-PASSWORD-UPDATE-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured during admin password update. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


admin_password_update_viewset = AdminPasswordUpdateViewSet.as_view()


class DonorSignUpViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def post(self, request):
        """
        Allows for a donor to signup
        """
        if not auth_validations.validate_donor_signup(request.data):
            return Response(
                data=CustomResponse(
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
                    data=CustomResponse(
                        "Donor signup successful",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            print(f"[DONOR-SIGNUP-ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                    data=CustomResponse(
                        "Donor is not registered",
                        "NOT-FOUND",
                        400,
                        None,
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not user.check_password(request.data["password"]):
                return Response(
                    data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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

            # send_forgotpassword_mail.delay(user.email, user.otp)
            send_forgotpassword_mail(user.email, user.otp)

            return Response(
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                # "location": request.data["location"],
                "address": request.data["address"],
                "state": request.data["state"],
                # "city": request.data["city"],
                "lga": request.data["lga"],
                "postalCode": request.data["postalCode"],
                "password": request.data["password"],
                "hospitalName": request.data["hospitalName"],
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                send_hospital_welcome_mail(
                    serializer.data["email"],
                    serializer.data["hospitalName"],
                    serializer.data["hospitalID"],
                )
                return Response(
                    data=CustomResponse(
                        "Hospital signup successful",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
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
                    data=CustomResponse(
                        "Hospital is not registered",
                        "NOT-FOUND",
                        400,
                        None,
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )
            if not hospital.check_password(request.data["password"]):
                return Response(
                    data=CustomResponse(
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
                data=CustomResponse(
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
                data=CustomResponse(
                    f"An error occured during hospital login. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_signin_viewset = HospitalSignInViewSet.as_view()


class UpdateHospitalViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HospitalProfileUpdateSerializer

    def put(self, request):
        try:
            instance = User.objects.get(pkid=request.user.pkid)

            if not instance.check_password(request.data["currentPassword"]):
                return Response(
                    data=CustomResponse(
                        f"Unauthorized",
                        "ERROR",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.serializer_class(instance, data=request.data)

            if serializer.is_valid():
                serializer.save()

                instance.set_password(request.data["newPassword"])
                instance.save()

                _serializer = HospitalAuthSerializer(instance)

                return Response(
                    data=CustomResponse(
                        "Hospital profile updated successfully",
                        "SUCCESS",
                        200,
                        _serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            print(f"[ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    f"An error occured during hospital update",
                    "ERROR",
                    400,
                    None,
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


class DonorUpdateProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonorAuthSerializer

    def put(self, request):
        try:
            user = User.objects.get(pkid=request.user.pkid)

            if user.check_password(request.data["password"]):
                # print(request.data)
                # print(request.FILES["avatar"])

                data = {
                    "email": request.data["email"],
                }

                if len(request.FILES) > 0 and "avatar" in request.FILES:
                    print("[AVATAR-PRESENT]")
                    os.remove(user.avatar.path)
                    data["avatar"] = request.FILES["avatar"]

                serializer = self.serializer_class(user, data=data)

                if serializer.is_valid():
                    serializer.save()

                    if request.data["new_password"] != "":
                        user.set_password = request.data["new_password"]
                        user.save()

                    return Response(
                        data=CustomResponse(
                            "Donor profile updated successfully.",
                            "SUCCESS",
                            200,
                            serializer.data,
                        ),
                        status=status.HTTP_200_OK,
                    )
                print(f"[ERROR] :: {serializer.errors}")
                return Response(
                    data=CustomResponse(
                        "An error occured while updating donor profile.",
                        "ERROR",
                        400,
                        serializer.errors,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    data=CustomResponse(
                        "Invalid credentials.",
                        "ERROR",
                        400,
                        None,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            print(f"[UPDATE-DONOR-PROFILE-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating donor profile. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_update_profile_viewset = DonorUpdateProfileViewSet.as_view()


def geeks_view(request):
    return render(request, "user/hospital_welcome_template.html")
