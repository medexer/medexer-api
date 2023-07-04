import os, requests, json
from dotenv import load_dotenv
from rest_framework import generics, status
from django.db.models.functions import Cast
from django.db.models import Q, IntegerField
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import Inventory
from apps.user.models import User
from . import serializers
from .models import *
from datetime import datetime
from apps.administrator.models import *
from apps.profile.models import *
from apps.registration.models import KnowYourCustomer
from apps.donor.models import Appointment, DonationHistory
from apps.common.validations import hospital_validations
from apps.common.id_generator import complaint_id_generator
from apps.common.custom_response import CustomResponse, CurrentTimeStamp

load_dotenv()


class DashboardViewSet(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventoryHistorySerializer

    def get(self, request):
        try:
            
            return Response(
                data=CustomResponse(
                    f"Fetched hospital dashboard data successfully.",
                    "SUCCESS",
                    200,
                    None,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-INVENTORY-ACTIVITY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching dashboard data. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


dashboard_viewset = DashboardViewSet.as_view()


class DonorSearchViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DonorSearchSerializer

    def get(self, request, query):
        try:
            query_set = []
            
            inventories = Inventory.objects.filter(hospital=request.user.pkid)
            profiles = Profile.objects.filter(
                Q(user__fullName__icontains=query) 
                | 
                Q(state__icontains=query) 
                |
                Q(city_province__icontains=query)
                |
                Q(bloodGroup__icontains=query)
            )
            
            for item in inventories:
                for profile in profiles:
                    if profile.bloodGroup and item.bloodGroup == profile.bloodGroup:    
                        if item.bloodUnits < 20:
                            if profile.is_profile_updated and profile.latitude:
                                donor = User.objects.get(pkid=profile.user.pkid)
                                
                                if donor.is_donor:
                                    query_set.append(donor)
                    else:
                        if profile.is_profile_updated and profile.latitude:
                            donor = User.objects.get(pkid=profile.user.pkid)
                            
                            if donor.is_donor:
                                query_set.append(donor)    

            serializer = self.serializer_class(query_set, many=True)
            
            return Response(
                data=CustomResponse(
                    f"Donor search successfull.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[DONOR-SEARCH-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while searhing donors. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_search_viewset = DonorSearchViewSet.as_view()


class InventoryItemHistoryViewSet(generics.GenericAPIView):
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventoryHistorySerializer

    def get(self, request, bloodGroup):
        try:
            inventory = InventoryActivity.objects.filter(
                Q(bloodGroup=bloodGroup) & Q(hospital=request.user.pkid)
            )

            serializer = self.serializer_class(instance=inventory, many=True)

            return Response(
                data=CustomResponse(
                    f"Fetched hospital inventory item activity successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-INVENTORY-ACTIVITY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching inventory item activity. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


inventory_item_history_viewset = InventoryItemHistoryViewSet.as_view()


class InventoryItemViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventoryItemSerializer

    def put(self, request, inventoryItem):
        try:
            activity = ""
            data = {
                "bloodUnits": int(request.data["units"]),
            }

            instance = InventoryItem.objects.get(
                pkid=inventoryItem, hospitalID=request.user.hospitalID
            )
            inventory = Inventory.objects.get(
                bloodGroup=instance.bloodGroup, hospital=request.user.pkid
            )

            if instance.bloodUnits < int(data["bloodUnits"]):
                activity = f"{request.data['count']} pint added on {CurrentTimeStamp()}"
            else:
                activity = f"{request.data['count']} pint removed on {CurrentTimeStamp()}"

            serializer = self.serializer_class(instance, data=data)

            if serializer.is_valid():
                serializer.save()

                inventory.bloodUnits = inventory.bloodUnits - int(request.data['count'])
                inventory.save()

                InventoryActivity.objects.create(
                    activity=activity,
                    hospital=request.user,
                    bloodGroup=request.data["bloodGroup"],
                )
                Notification.objects.create(
                    notificationType="APPOINTMENT",
                    author=request.user,
                    recipient=instance.donor,
                    title=f"Blood Usage",
                    message=f"{request.data['units']} pints of your blood was used in {request.user.hospitalName}.",
                )

                return Response(
                    data=CustomResponse(
                        "Inventory item updated successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            print(f"[UPDATE-INVENTORY-ITEM-ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating inventory item.",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[UPDATE-INVENTORY-ITEM-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching inventory item. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


inventory_item_detail_viewset = InventoryItemViewSet.as_view()


class HospitalInventoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventorySerializer

    def get(self, request):
        try:
            inventoryItems = Inventory.objects.filter(hospital=request.user.pkid)

            serializer = self.serializer_class(instance=inventoryItems, many=True)

            return Response(
                data=CustomResponse(
                    f"Fetched hospital inventory successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-INVENTORY-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital inventory. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_inventory_viewset = HospitalInventoryViewSet.as_view()


class HospitalInventoryItemViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.InventoryItemSerializer

    def get(self, request, bloodGroup):
        try:
            inventoryItems = InventoryItem.objects.annotate(text_int=Cast('bloodUnits', output_field=IntegerField())).filter(Q(hospitalID=request.user.hospitalID) & Q(bloodGroup=bloodGroup) & Q(bloodUnits__gte=0))

            serializer = self.serializer_class(instance=inventoryItems, many=True)

            return Response(
                data=CustomResponse(
                    f"Fetched hospital inventory items successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-INVENTORY-ITEM-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital inventory items. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_inventory_item_viewset = HospitalInventoryItemViewSet.as_view()


class HospitalAppointmentViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    def get(self, request):
        try:
            appointments = Appointment.objects.filter(
                Q(hospital=request.user.pkid) & Q(isPaid=False)
            )
            serializer = self.serializer_class(appointments, many=True)

            return Response(
                data=CustomResponse(
                    "Hospital appointments fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-APPOINTMENTS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital appointment ",
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pkid):
        try:
            data = {
                "date": request.data["date"],
            }

            instance = Appointment.objects.get(pkid=pkid)
            serializer = self.serializer_class(instance, data=data)
           
            if serializer.is_valid():
                serializer.save()

                Notification.objects.create(
                    notificationType="APPOINTMENT",
                    author=request.user,
                    recipient=instance.donor,
                    title=f"Appointment Schedule from {request.user.hospitalName}",
                    message=request.data["message"],
                )

                return Response(
                    data=CustomResponse(
                        "Hospital appointment rescheduled successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured during appointment reschedule",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[RESCHEDULE-APPOINTMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured during appointment reschedule. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_appointment_viewset = HospitalAppointmentViewSet.as_view()


class HospitalProcessDonationViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    def put(self, request, pkid):
        try:
            data = {
                "isDonated": True,
                "pints": request.data["pints"],
                "donationDate": request.data["donationDate"],
            }

            instance = Appointment.objects.get(pkid=pkid)
            donor = User.objects.get(pkid=instance.donor.pkid)
            donorProfile = KnowYourCustomer.objects.get(donor=instance.donor.pkid)
            inventory = Inventory.objects.filter(Q(hospital=instance.hospital.pkid) & Q(bloodGroup=request.data['bloodGroup'])).first()
            
            serializer = self.serializer_class(instance, data=data)
           
            if serializer.is_valid():
                serializer.save()

                inventory.bloodUnits = inventory.bloodUnits + int(request.data['pints'])

                inventory.save()
                
                donorProfile.bloodGroup = request.data['bloodGroup']
                
                donorProfile.save()
                
                donor.in_recovery = True
                donor.lastDonationDate = datetime.now().strftime('%Y-%m-%d')
                
                donor.save()

                InventoryItem.objects.create(
                    bloodGroup=request.data['bloodGroup'],
                    bloodUnits=request.data['pints'],
                    appointmentID=instance.appointmentID,
                    hospitalID=instance.hospital.hospitalID,
                    donor=donorProfile.donor.pkid,
                    inventory=inventory.pkid,
                )
                Notification.objects.create(
                    notificationType="APPOINTMENT",
                    author=request.user.pkid,
                    recipient=instance.donor.pkid,
                    title=f"Donation Alert",
                    message=f"You donation with {instance.hospital.hospitalName} has been successfully processed. We appreciate your patience as we handle your incentives within two working days.",
                )
                DonationHistory.objects.create(
                    donor=instance.donor.pkid,
                    message=f"Donated {instance.pints} pints of blood on {instance.created_at}"
                )

                return Response(
                    data=CustomResponse(
                        "Donor appointment processed successfully",
                        "SUCCESS",
                        200,
                        serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            return Response(
                data=CustomResponse(
                    f"An error occured while processing donation.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[RESCHEDULE-APPOINTMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while processing donation. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_process_donation_viewset = HospitalProcessDonationViewSet.as_view()


class HospitalDonationPaymentViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer
    
    def get(self, request, reference):
        """
        Allows for a hospital to verify a donation payment
        """
        try:
            url = f"https://api.paystack.co/transaction/verify/{reference}"
            headers = {
                "authorization": f"Bearer {os.getenv('PAYSTACK_SECRET')}"
            }

            r = requests.get(url, headers=headers)

            response = r.json()
            
            return Response(
                data=CustomResponse(
                    "Donation payment verification successful",
                    "SUCCESS",
                    200,
                    response,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[VERIFY-DONATION-PAYMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while verifying donation payment. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, donation):
        try:
            donation = Appointment.objects.get(pkid=donation)
            hospital = User.objects.get(pkid=request.user.pkid)
            
            url = "https://api.paystack.co/transaction/initialize"
            headers = {
                "authorization": f"Bearer {os.getenv('PAYSTACK_SECRET')}"
            }

            data = {
                "email": hospital.email,
                "amount": (7650 * 100),
                "callback_url": "http://localhost:3003/payment/verify",
                "metadata": json.dumps({
                    "cart_id": donation.pkid,
                    "custom_fields": [
                        {
                            "display_name": "Appointment ID",
                            "variable_name": "appointment_id",
                            "value": f"{donation.pkid}",
                        },
                        {
                            "display_name": "Hospital ID",
                            "variable_name": "donation_id",
                            "value": f"{donation.hospital.hospitalID}",
                        },
                        {
                            "display_name": "Donor name",
                            "variable_name": "donor_name",
                            "value": f"{donation.donor.fullName}",
                        },
                        {
                            "display_name": "Blood pints",
                            "variable_name": "blood_pints",
                            "value": f"{donation.pints}",
                        },
                        {
                            "display_name": "Hospital name",
                            "variable_name": "hospital_name",
                            "value": f"{donation.hospital.hospitalName}",
                        },
                        {
                            "display_name": "Donation date",
                            "variable_name": "donation_date",
                            "value": f"{donation.donationDate}",
                        },
                    ]
                })
            }

            r = requests.post(url, headers=headers, data=data)

            response = r.json()

            return Response(
                data=CustomResponse(
                    "Donation payment initialization generated successfully",
                    "SUCCESS",
                    200,
                    response['data'],
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[INITIALIZE-DONATION-PAYMENT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while initializing donation payment. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_donation_payment_viewset = HospitalDonationPaymentViewSet.as_view()


class DonorDonationHistoryViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    queryset = Appointment.objects.all()

    def get(self, request, donorId):
        try:
            donor_activity = DonationHistory.objects.filter(donor=donorId)

            serializer = self.serializer_class(instance=donor_activity, many=True)

            return Response(
                data=CustomResponse(
                    "Donor donation history fetched successfully.",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-HOSPITAL-NOTIFICATIONS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching donor donation activity. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


donor_donation_history_viewset = DonorDonationHistoryViewSet.as_view()


class HospitalComplaintViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HospitalComplaintSerializer

    def get(self, request):
        """
        Allows for a hospital to fetch thier complaints
        """
        try:
            complaints = Complaint.objects.filter(hospital=request.user.pkid)

            serializer = self.serializer_class(complaints, many=True)

            return Response(
                data=CustomResponse(
                    "Complaint fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-COMPLAINT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching hospital complaints. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        """
        Allows for a hospital to generate a complaint
        """
        if not hospital_validations.validate_generate_complaint(request.data):
            return Response(
                data=CustomResponse(
                    hospital_validations.validation_message,
                    "BAD REQUEST",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            hospital = User.objects.get(pkid=request.user.pkid)

            data = {
                "status": "OPENED",
                "hospital": hospital.pkid,
                "title": request.data["title"],
                "hospitalID": hospital.hospitalID,
                "complaintID": complaint_id_generator(),
            }

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()

                complaint = Complaint.objects.get(pkid=serializer.data["pkid"])

                # ComplaintHistory.objects.create(
                #     complaint=complaint,
                #     headline=f"{hospital.hospitalName} Created this Complaint",
                #     author=request.user,
                # )
                ComplaintHistory.objects.create(
                    # status="THREAD",
                    headline=f"{hospital.hospitalName} Replied",
                    message=request.data["message"],
                    complaint=complaint,
                    author=request.user,
                )

                return Response(
                    data=CustomResponse(
                        "Complaint generated successfully",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            # print(f"[GENERATE-COMPLAINT-ERROR] :: {serializer.errors}")
            return Response(
                data=CustomResponse(
                    "An error occured while generating complaint.",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"[GENERATE-COMPLAINT-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while generating complaint. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, complaintId):
        """
        Allows for a hospital to update a complaint status
        """
        try:
            complaint = Complaint.objects.get(pkid=complaintId)

            data = {
                "status": request.data["status"],
            }

            serializer = self.serializer_class(complaint, data=data)

            if serializer.is_valid():
                serializer.save()

                ComplaintHistory.objects.create(
                    updateType="STATUS",
                    complaint=complaint,
                    headline=f"You updated the status to {request.data['status']}".upper(),
                )

                return Response(
                    data=CustomResponse(
                        "Complaint status updated successfully",
                        "SUCCESS",
                        201,
                        serializer.data,
                    ),
                    status=status.HTTP_201_CREATED,
                )
            # print(f"[UPDATE-COMPLAINT-STATUS-ERROR] :: {serializer.errors}")
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
            print(f"[UPDATE-COMPLAINT-STATUS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while updating complaint status. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


hospital_complaint_viewset = HospitalComplaintViewSet.as_view()


class HospitalComplaintThreadViewSet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HospitalComplaintHistorySerializer

    def get(self, request, complaintId):
        """
        Allows for a hospital to fetch threads for a complaint
        """
        try:
            complaintsThreads = ComplaintHistory.objects.filter(
                complaint=complaintId
            ).order_by("-pkid")

            serializer = self.serializer_class(complaintsThreads, many=True)

            return Response(
                data=CustomResponse(
                    "Complaint threads fetched successfully",
                    "SUCCESS",
                    200,
                    serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"[FETCH-COMPLAINT-THREADS-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while fetching complaint thread. {e}",
                    "ERROR",
                    400,
                    None,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, complaintId):
        """
        Allows for a hospital to reply to a complaint thread
        """
        try:
            complaint = Complaint.objects.get(pkid=complaintId)

            data = {
                "updateType": "THREAD",
                "headline": "You replied",
                "complaint": complaint.pkid,
                "message": request.data["message"],
            }

            serializer = self.serializer_class(data=data)

        except Exception as e:
            print(f"[GENERATE-COMPLAINT-THREAD-ERROR] :: {e}")
            return Response(
                data=CustomResponse(
                    f"An error occured while generating complaint thread. {e}",
                    "BAD REQUEST",
                    400,
                    serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


complaint_thread_viewset = HospitalComplaintThreadViewSet.as_view()


class HospitalNotificationsViewSet(generics.GenericAPIView):
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


hospital_notifications_viewset = HospitalNotificationsViewSet.as_view()
