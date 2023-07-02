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
    DonorProfileSerializer,
    HospitalAuthSerializer,
    DonorProfileUpdateSerializer,
    HospitalProfileUpdateSerializer,
)
from apps.profile.models import Profile



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

                Profile.objects.create(
                    user=User.objects.get(pkid=serializer.data['pkid']),
                    nationality=request.data['nationality'],
                    gender=request.data['gender'],
                    religion=request.data['religion'],
                    address=request.data['address'],
                    state=request.data['state'],
                    city_province=request.data['city_province'],
                    contact_number=request.data['contact_number'],
                    is_profile_updated=True,
                )
                
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
            profile = Profile.objects.filter(user=user.pkid).first()

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
            profile_serializer = DonorProfileSerializer(profile)

            return Response(
                data=CustomResponse(
                    "Donor login successful",
                    "SUCCESS",
                    200,
                    data={
                        "user": serializer.data,
                        "profile": profile_serializer.data,
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


class DonorGoogleSignInViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def post(self, request):
        """
        Allows for a donor to login with google oauth
        """
        try:
            _user = User.objects.filter(Q(email=request.data["email"].strip())).first()

            donorID = donor_id_generator()
            users = User.objects.all()

            for user in users:
                if user.donorID == donorID:
                    donorID = donor_id_generator()

            if _user is None:
                data = {
                    "is_donor": True,
                    "donorID": donorID,
                    "email": request.data["email"],
                    "fullName": request.data["fullName"],
                    "password": request.data["password"],
                }
                
                serializer = self.serializer_class(data=data)
                
                if serializer.is_valid():
                    serializer.save()
            
                    new_user = User.objects.filter(Q(email=request.data["email"].strip())).first()
                    Profile.objects.create(user=new_user)

                    new_user.is_email_login = True
                    new_user.save()

                    profile = Profile.objects.get(user=new_user.pkid)
                        
                    refresh__token = RefreshToken.for_user(new_user)
                    access__token = "Bearer " + str(refresh__token.access_token)

                    serializer = self.serializer_class(new_user)
                    profile_serializer = DonorProfileSerializer(profile)

                    return Response(
                        data=CustomResponse(
                            "Donor login successful",
                            "SUCCESS",
                            200,
                            data={
                                "user": serializer.data,
                                "profile": profile_serializer.data,
                                "access": access__token,
                                "refresh": str(refresh__token),
                            },
                        ),
                        status=status.HTTP_200_OK,
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
                
            user = User.objects.filter(Q(email=request.data["email"].strip())).first()

            user.is_email_login = True
            user.save()

            profile = Profile.objects.get(user=user.pkid)

            refresh__token = RefreshToken.for_user(user)
            access__token = "Bearer " + str(refresh__token.access_token)

            serializer = self.serializer_class(user)
            profile_serializer = DonorProfileSerializer(profile)

            return Response(
                data=CustomResponse(
                    "Donor login successful",
                    "SUCCESS",
                    200,
                    data={
                        "user": serializer.data,
                        "profile": profile_serializer.data,
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


donor_googlesignin_viewset = DonorGoogleSignInViewSet.as_view()


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


class DonorSignoutViewSet(APIView):
    serializer_class = DonorAuthSerializer

    def put(self, request):
        """
        Allows for a donor to generate update his email login field on signout
        """
        try:
            user = User.objects.get(pkid=request.user.pkid)

            user.is_email_login = False
            user.save()

            return Response(
                data=CustomResponse(
                    "Donor info updated successfully",
                    "SUCCESS",
                    200,
                    None,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[DONOR-RESET-EMAIL-LOGIN-INFO-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"Failure occurred during donor email login info on signout. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_signout_viewset = DonorSignoutViewSet.as_view()


class DonorDeleteAccountViewSet(APIView):
    def delete(self, request):
        """
        Allows for a donor to delete his account
        """
        try:
            user = User.objects.get(pkid=request.user.pkid)

            user.delete()
            
            return Response(
                data=CustomResponse(
                    "Donor account deleted successfully",
                    "SUCCESS",
                    200,
                    None,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[DONOR-DELETE-ACCOUNT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"Failure occurred during donor delete account. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_delete_account_viewset = DonorDeleteAccountViewSet.as_view()


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
    serializer_class = DonorProfileUpdateSerializer

    def put(self, request):
        try:
            user = User.objects.get(pkid=request.user.pkid)
            profile = Profile.objects.get(user=request.user.pkid)

            if user.check_password(request.data["password"]):
                # print(request.data)
                # print(request.FILES["avatar"])

                data = {
                    "email": request.data["email"],
                    "avatar": request.FILES["avatar"]
                }

                serializer = self.serializer_class(user, data=data)
                user_serializer = DonorAuthSerializer(user)
                profile_serializer = DonorProfileSerializer(profile)

                if serializer.is_valid():
                    serializer.save()
                    
                    profile.nationality = request.data['nationality']
                    profile.gender = request.data['gender']
                    profile.religion = request.data['religion']
                    profile.address = request.data['address']
                    profile.state = request.data['state']
                    profile.city_province = request.data['city_province']
                    profile.contact_number = request.data['contact_number']
                    profile.save()

                    if request.data["new_password"]:
                        user.set_password = request.data["new_password"]
                        user.save()

                    return Response(
                        data=CustomResponse(
                            "Donor profile updated successfully.",
                            "SUCCESS",
                            200,
                            {
                                "user": user_serializer.data,
                                "profile": profile_serializer.data,
                            },
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


class DonorUpdateSignupProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonorProfileSerializer

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user.pkid)

            data = {
                "is_profile_updated": True,
                "nationality": request.data["nationality"],
                "gender": request.data["gender"],
                "religion": request.data["religion"],
                "address": request.data["address"],
                "state": request.data["state"],
                "city_province": request.data["city_province"],
                "contact_number": request.data["contact_number"],
            }

            serializer = self.serializer_class(profile, data=data)

            if serializer.is_valid():
                serializer.save()

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


donor_update_signup_profile_viewset = DonorUpdateSignupProfileViewSet.as_view()


class DonorUpdateProfileWithGoogleSigninViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonorProfileUpdateSerializer

    def put(self, request):
        try:
            user = User.objects.get(pkid=request.user.pkid)
            profile = Profile.objects.get(user=request.user.pkid)
            
            data = {
                "email": request.data["email"],
                # "password": request.user.password,
                "avatar": request.FILES["avatar"]
            }

            serializer = self.serializer_class(user, data=data)
            user_serializer = DonorAuthSerializer(user)
            profile_serializer = DonorProfileSerializer(profile)

            if serializer.is_valid():
                serializer.save()

                profile.nationality = request.data['nationality']
                profile.gender = request.data['gender']
                profile.religion = request.data['religion']
                profile.address = request.data['address']
                profile.state = request.data['state']
                profile.city_province = request.data['city_province']
                profile.contact_number = request.data['contact_number']
                profile.save()

                return Response(
                    data=CustomResponse(
                        "Donor profile updated successfully.",
                        "SUCCESS",
                        200,
                        {
                            "user": user_serializer.data,
                            "profile": profile_serializer.data,
                        },
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


donor_update_profile_with_google_signin_viewset = DonorUpdateProfileWithGoogleSigninViewSet.as_view()


def geeks_view(request):
    return render(request, "user/hospital_welcome_template.html")
