from . import serializers
from .models import *
from django.db.models import Q
from apps.user.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.common.custom_response import CustomResponse
from .tasks import send_integration_request_mail
from apps.donor.models import Appointment
from apps.hospital.serializers import HospitalComplaintHistorySerializer

class DashboardViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Allows for an administrator to fetch his dashboard info
        """
        try:
            donors = User.objects.filter(is_donor=True).count()
            hospitals = User.objects.filter(is_hospital=True).count()

            return Response(
                data=CustomResponse(
                    "Dashboard info fetched successfully",
                    "SUCCESS",
                    200,
                    {
                        "donors": donors,  
                        "hospitals": hospitals,  
                    },
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-DASHBOARD-INFO-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching dashboard info. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


dashboard_viewset = DashboardViewSet.as_view()


class IntegrationViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.IntegrationSerializer

    def get(self, request):
        """
        Allows for an administrator to fetch medexer integration requests
        """
        try:
            integrations = Integration.objects.filter(is_approved=False)
            
            serializer = self.serializer_class(integrations, many=True)
            
            return Response(
                data=CustomResponse(
                    "Integrations fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-INTEGRATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching interations info. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    
    def patch(self, request, organization):
        """
        Allows for an administrator to patch an organization integration request
        """
        try:
            integration = Integration.objects.get(pkid=organization)
            
            data = {
                "is_approved": True,
                "accessKey": request.data['accessKey'],
            }
            
            serializer = self.serializer_class(integration, data=data)
            
            if serializer.is_valid():
                serializer.save()

                send_integration_request_mail(request.data['email'], request.data['accessKey'])
            
                return Response(
                    data=CustomResponse(
                        "Integration updated successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured while updating interation info.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[PATCH-INTEGRATION-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating interation info. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


integrations_viewset = IntegrationViewSet.as_view()


class HospitalsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HospitalSerializer

    def get(self, request):
        """
        Allows for an administrator to fetch medexer hospitals
        """
        try:
            hospitals = User.objects.filter(is_hospital=True)
            
            serializer = self.serializer_class(hospitals, many=True)
            
            return Response(
                data=CustomResponse(
                    "Hospitals fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITALS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospitals. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, hospital):
        """
        Allows for an administrator to patch a hospital info
        """
        try:
            hospital = User.objects.get(pkid=hospital)
            
            data = {
                "email": request.data['email'],
                "hospitalName": request.data['hospitalName'],
            }
            
            serializer = self.serializer_class(hospital, data=data)
            
            if serializer.is_valid():
                serializer.save()
                
                if request.data['password']:
                    hospital.set_password(request.data['password'])
                    hospital.save()
                
                return Response(
                    data=CustomResponse(
                        "Hospital info updated successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    "An error occured while updating hospital info.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[PATCH-HOSPITAL-INFO-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating hospital info. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    
    
hospitals_viewset = HospitalsViewSet.as_view()


class DonorsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorSerializer

    def get(self, request):
        """
        Allows for an administrator to fetch medexer donors
        """
        try:
            donors = User.objects.filter(is_donor=True)
            
            serializer = self.serializer_class(donors, many=True)
            
            return Response(
                data=CustomResponse(
                    "Donors fetched successfully",
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
                    f"An error occured while fetching donors. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def patch(self, request, donor):
        """
        Allows for an administrator to patch a donor info
        """
        try:
            donor = User.objects.get(pkid=donor)
            
            data = {
                "email": request.data['email'],
                "fullName": request.data['fullName'],
            }
            
            serializer = self.serializer_class(donor, data=data)
            
            if serializer.is_valid():
                serializer.save()
                
                if request.data['password']:
                    donor.set_password(request.data['password'])
                    donor.save()
                
                return Response(
                    data=CustomResponse(
                        "Donor info updated successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    "An error occured while updating donor info.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[PATCH-DONOR-INFO-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating donor info. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    
    
donors_viewset = DonorsViewSet.as_view()


class DonationsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonationSerializer

    def get(self, request):
        """
        Allows for an administrator to fetch donations
        """
        try:
            donations = Appointment.objects.filter(isDonated=True)
            
            serializer = self.serializer_class(donations, many=True)
            
            return Response(
                data=CustomResponse(
                    "Donations fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-DONATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching donations. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    
donations_viewset = DonationsViewSet.as_view()


class ComplaintsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ComplaintSerializer

    def get(self, request):
        """
        Allows for an administrator to fetch complaints
        """
        try:
            complaints = Complaint.objects.all()
            
            serializer = self.serializer_class(complaints, many=True)
            
            return Response(
                data=CustomResponse(
                    "Complaints fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-COMPLAINTS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching complaints. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, complaint):
        """
        Allows for an administrator to update a complaint status
        """
        try:
            complaint = Complaint.objects.get(pkid=complaint)
            print(request.data)
            data = {
                "status": request.data['status']
            }
            
            serializer = self.serializer_class(complaint, data=data)
            
            if serializer.is_valid():
                serializer.save()
            
                return Response(
                    data=CustomResponse(
                        "Complaints fetched successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    "An error occured while updating complaint status.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[PATCH-COMPLAINT-STATUS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating complaint status. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    
complaints_viewset = ComplaintsViewSet.as_view()


class ComplaintHistoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HospitalComplaintHistorySerializer

    def get(self, request, complaint):
        """
        Allows for an administrator to fetch a complaint history
        """
        try:
            history = ComplaintHistory.objects.filter(complaint=complaint)
            
            serializer = self.serializer_class(history, many=True)
            
            return Response(
                data=CustomResponse(
                    "Complaint history fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-COMPLAINT-HISTORY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching complaint history. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def post(self, request, complaint):
        """
        Allows for an administrator to reply a complaint history
        """
        try:
            complaint = Complaint.objects.get(pkid=complaint)
            # print(request.data)
            data = {
                'complaint': complaint.pkid,
                'author': request.user.pkid,
                'headline': 'Medexer Replied',
                "message": request.data['message'],
            }
            
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():
                serializer.save()
            
                return Response(
                    data=CustomResponse(
                        "Complaint history created successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            print(f"[PATCH-COMPLAINT-STATUS-ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    "An error occured while creating complaint history.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[PATCH-COMPLAINT-STATUS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while creating complaint history. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    
complaint_history_viewset = ComplaintHistoryViewSet.as_view()


class NotificationsViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    def get(self, request):
        """
        Allows for an administrator to fetch notifications
        """
        try:
            notifications = Notification.objects.filter(authorType="ADMIN")
            
            serializer = self.serializer_class(notifications, many=True)
            
            return Response(
                data=CustomResponse(
                    "Notifications fetched successfully",
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
                    f"An error occured while fetching notifications. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        """
        Allows for an administrator to create a notification
        """
        try:
            recipients = []
            
            if request.data['sendToAll'] and len(request.data['recipients']) == 0:
                users = User.objects.filter(is_administrator=False)
                for user in users:
                    recipients.append(user.pkid)
            if request.data['sendToHospitals'] and len(request.data['recipients']) == 0:
                users = User.objects.filter(is_hospital=True)
                for user in users:
                    recipients.append(user.pkid)
            if request.data['sendToDonors'] and len(request.data['recipients']) == 0:
                users = User.objects.filter(is_donor=True)
                for user in users:
                    recipients.append(user.pkid)
            
            data = {
                "notificationType": request.data['notificationType'],
                "authorType": 'ADMIN',
                "title": request.data['title'],
                "message": request.data['message'],
                "author": request.user.pkid,
                "recipient": request.data['recipient'] if request.data['recipient'] else None,
                "recipients": recipients  if len(recipients) > 0 else request.data['recipients'],
            }
            
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid():
                serializer.save()
            
                return Response(
                    data=CustomResponse(
                        "Notification created successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            print(f"[CREATE-NOTIFICATION-ERRORR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    "An error occured while creating a notification.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[CREATE-NOTIFICATION-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while creating a notification. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
    

notifications_viewset = NotificationsViewSet.as_view()


class SearchCustomersViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CustomerSearchSerializer

    def get(self, request, query):
        """
        Allows for an administrator to fetch search for customers
        """
        try:
            users = User.objects.filter(Q(fullName__contains=query) | Q(hospitalName__contains=query) & Q(is_administrator=False))
            
            serializer = self.serializer_class(users, many=True)
            
            return Response(
                data=CustomResponse(
                    "Search query successful",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[SEARCH-CUSTOMERS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while searching customers. {e}",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
search_customers_viewset = SearchCustomersViewSet.as_view()