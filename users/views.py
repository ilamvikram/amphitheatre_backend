from email.utils import parsedate
import re
import shutil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import ContactForm
from .serializers import ContactFormSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactForm
from datetime import datetime
from .models import BookingForm
from .serializers import BookingFormSerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view 
import base64
import base64
import os
from django.conf import settings
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer
from io import BytesIO
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer
from django.utils.dateparse import parse_date
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import base64
import uuid
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer
from .models import Event
from users import serializers
from rest_framework import generics
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.permissions import AllowAny
class RegisterAPIView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data
    
class EventCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Debug print for context
        # context = self.get_serializer_context()
        print(serializer.data,'kotii')
        if(serializer.data):
            for img in range(len(serializer.data)):
                for childimg in range(len(serializer.data[img]['images'])):
                    serializer.data[img]['images'][childimg] = f"http://{settings.IP_ADDRESS}:{settings.APP_PORT}/api"+serializer.data[img]['images'][childimg]

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(null,status=status.HTTP_204_NO_CONTENT)
        
        # serializer.data['images'] = "http://   


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class DeleteEventFolderAPIView(APIView):
    def delete(self, request, event_type):
        # Normalize and sanitize event_type to match folder name
        safe_event_type = re.sub(r'[^\w\-]', '_', event_type.strip().lower())
        folder_path = os.path.join(settings.MEDIA_ROOT, safe_event_type)

        # Check if folder exists
        if not os.path.exists(folder_path):
            return Response(
                {"detail": "Folder not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Delete folder and all its contents
            shutil.rmtree(folder_path)

            # Optionally delete event record from DB (optional)
            Event.objects.filter(event_type__iexact=event_type).delete()

            return Response(
                {"detail": f"Folder '{safe_event_type}' and related event deleted successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SuperuserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")  # This will be phone_number from frontend
        password = request.data.get("password")

        try:
            user = User.objects.get(phone_number=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # user = authenticate(request, username=user.username, password=password)

        if user is not None and user.is_superuser:
            return Response({
                "role": "admin"
            })
        return Response({"detail": "Invalid credentials or not a superuser"}, status=status.HTTP_401_UNAUTHORIZED)

class CustomLoginView(TokenObtainPairView): 
    serializer_class = CustomTokenObtainPairSerializer

class ContactFormCreateAPIView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can submit

class ContactUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class ContactFormListAPIView(generics.ListAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    # permission_classes = [permissions.IsAdminUser]  # Admin only

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = BookingForm.objects.all()
    serializer_class = BookingFormSerializer
    permission_classes = [permissions.AllowAny]

    # def post(self, request):
    #     start_date_str = request.data.get('start_date', '').strip()
    #     end_date_str = request.data.get('end_date', '').strip()
    #     slot = request.data.get('slot', '').strip().title()
    #     # Parse and validate dates
    #     start_date = parse_date(start_date_str)
    #     end_date = parse_date(end_date_str)

    #     if not start_date or not end_date or not slot:
    #         return Response(
    #             {"message": "Invalid or missing start_date, end_date, or slot."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if start_date > end_date:
    #         return Response(
    #             {"message": "start_date must be before end_date."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )


    #     selected_slots = set()
    #     date = start_date
    #     while date <= end_date:
    #         selected_slots.add((date, slot))
    #         date += timedelta(days=1)

    #     # Build a set of (booked_date, booked_slot) from existing bookings
    #     booked_slots = set()
    #     for booking in BookingForm.objects.all():
    #         b_date = booking.start_date
    #         while b_date <= booking.end_date:
    #             booked_slots.add((b_date, booking.slot))
    #             b_date += timedelta(days=1)

    #     available = all(item not in booked_slots for item in selected_slots)

    #     print(booked_slots,'dhanes',selected_slots)

    #     if not available:
    #         return Response(
    #             {"available": False, "message": "The selected date range is not available."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     return Response(
    #         {"available": True, "message": "The selected date range is available and has been booked."},
    #         status=status.HTTP_201_CREATED
    #     )

    # def post(self, request):
    #     start_date_str = request.data.get('start_date', '').strip()
    #     end_date_str = request.data.get('end_date', '').strip()
    #     slot = request.data.get('slot', '').strip().title()

    #     # Parse and validate dates
    #     start_date = parse_date(start_date_str)
    #     end_date = parse_date(end_date_str)

    #     if not start_date or not end_date or not slot:
    #         return Response(
    #             {"message": "Invalid or missing start_date, end_date, or slot."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if start_date > end_date:
    #         return Response(
    #             {"message": "start_date must be before end_date."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     try:
    #         requested_slot_type = get_slot_type(slot)
    #         if requested_slot_type == "invalid":
    #             raise ValueError()
    #     except:
    #         return Response(
    #             {"message": "Invalid slot value. Must be 1–24 or 'Full Day'."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # Step 1: Build a dict with date -> set of existing slot types
    #     booked_slot_types = {}
    #     for booking in BookingForm.objects.all():
    #         b_date = booking.start_date
    #         while b_date <= booking.end_date:
    #             b_slot_type = get_slot_type(booking.slot)
    #             if b_date not in booked_slot_types:
    #                 booked_slot_types[b_date] = set()
    #             booked_slot_types[b_date].add(b_slot_type)
    #             b_date += timedelta(days=1)

    #     # Step 2: Check for conflicts
    #     date = start_date
    #     while date <= end_date:
    #         existing = booked_slot_types.get(date, set())

    #         if requested_slot_type == "full":
    #             if "morning" in existing or "evening" in existing or "full" in existing:
    #                 return Response(
    #                     {"available": False, "message": f"Cannot book Full Day on {date}, part of the day is already booked."},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
    #         elif requested_slot_type in ("morning", "evening"):
    #             if "full" in existing or requested_slot_type in existing:
    #                 return Response(
    #                     {"available": False, "message": f"{slot} on {date} is already booked or blocked by a Full Day booking."},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )
    #         date += timedelta(days=1)

    #     # If no conflicts, create the booking
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     return Response(
    #         {"available": True, "message": "The selected date range is available and has been booked."},
    #         status=status.HTTP_201_CREATED
    #     )

    def post(self, request):
        start_date_str = request.data.get('start_date', '').strip()
        end_date_str = request.data.get('end_date', '').strip()
        slot = request.data.get('slot', '').strip().title()

        # Parse and validate dates
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date or not slot:
            return Response(
                {"message": "Invalid or missing start_date, end_date, or slot."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start_date > end_date:
            return Response(
                {"message": "start_date must be before end_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if slot not in ["Morning", "Evening", "Full Day"]:
            return Response(
                {"message": "Invalid slot value. Must be 'Morning', 'Evening', or 'Full Day'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 1: Build date -> set of existing slot types
        booked_slot_types = {}
        for booking in BookingForm.objects.all():
            b_date = booking.start_date
            while b_date <= booking.end_date:
                b_slot = booking.slot.strip().title()
                if b_date not in booked_slot_types:
                    booked_slot_types[b_date] = set()
                booked_slot_types[b_date].add(b_slot)
                b_date += timedelta(days=1)

        # Step 2: Conflict checking logic
        date = start_date
        while date <= end_date:
            existing = booked_slot_types.get(date, set())

            if "Full Day" in existing:
                return Response(
                    {"available": False, "message": f"{date} is already booked as Full Day."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if slot == "Full Day":
                if "Morning" in existing or "Evening" in existing:
                    return Response(
                        {"available": False, "message": f"Cannot book Full Day on {date}, part of the day is already booked."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            elif slot in existing:
                return Response(
                    {"available": False, "message": f"{slot} on {date} is already booked."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            date += timedelta(days=1)

        # Step 3: Create booking
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"available": True, "message": "The selected date range is available and has been booked."},
            status=status.HTTP_201_CREATED
        )

class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingFormSerializer

    def get_queryset(self):
        queryset = BookingForm.objects.all()

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            # Parse dates from string to Python date objects
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if start_date and end_date:
                # Adjust 'date' to the actual field name in your model
                queryset = queryset.filter(date__range=(start_date, end_date))

        return queryset



@api_view(['PUT'])
def update_booking(request, pk):

    start_date_str = request.data.get('start_date', '').strip()
    end_date_str = request.data.get('end_date', '').strip()
    slot = request.data.get('slot', '').strip().title()

    # Parse and validate dates
    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)

    if not start_date or not end_date or not slot:
        return Response(
            {"message": "Invalid or missing start_date, end_date, or slot."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if start_date > end_date:
        return Response(
            {"message": "start_date must be before end_date."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if slot not in ["Morning", "Evening", "Full Day"]:
        return Response(
            {"message": "Invalid slot value. Must be 'Morning', 'Evening', or 'Full Day'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Step 1: Build date -> set of existing slot types
    booked_slot_types = {}
    for booking in BookingForm.objects.exclude(pk=pk):
        b_date = booking.start_date
        while b_date <= booking.end_date:
            b_slot = booking.slot.strip().title()
            if b_date not in booked_slot_types:
                booked_slot_types[b_date] = set()
            booked_slot_types[b_date].add(b_slot)
            b_date += timedelta(days=1)

    # Step 2: Conflict checking logic
    date = start_date
    while date <= end_date:
        existing = booked_slot_types.get(date, set())

        if "Full Day" in existing:
            return Response(
                {"available": False, "message": f"{date} is already booked as Full Day."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if slot == "Full Day":
            if "Morning" in existing or "Evening" in existing:
                return Response(
                    {"available": False, "message": f"Cannot book Full Day on {date}, part of the day is already booked."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif slot in existing:
            return Response(
                {"available": False, "message": f"{slot} on {date} is already booked."},
                status=status.HTTP_400_BAD_REQUEST
            )

        date += timedelta(days=1)

    try:
        booking = BookingForm.objects.get(pk=pk)
    except BookingForm.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=404)

    serializer = BookingFormSerializer(booking, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


    return Response(
        {"available": True, "message": "The selected date range is available and has been booked."},
        status=status.HTTP_201_CREATED
    )

    


class VendorCreateAPIView(APIView):
    
    def post(self, request):
        try:
            data = request.data
            document_name = data.get('document_name')
            if not document_name:
                return Response({'error': 'document_name is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Call instance method (self.save_base64_file)
            document_path, saved_name = self.save_base64_file(data['document'], document_name)

            # Create the vendor entry
            vendor = Vendor.objects.create(
                name=data['name'],
                company_name=data['company_name'],
                mobile=data['mobile'],
                email=data['email'],
                address=data['address'],
                gst_no=data['gst_no'],
                document_path=document_path,
                
            )

            return Response({'message': 'Vendor created successfully', 'vendor_id': vendor.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Make sure this is indented inside the class
    def save_base64_file(self, base64_data, original_filename):
        try:
            header, encoded_file = base64_data.split(',', 1)

            # Sanitize and define paths
            original_filename = os.path.basename(original_filename)
            upload_dir = 'vendors'
            upload_path = os.path.join(settings.MEDIA_ROOT, upload_dir)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, original_filename)

            # Write file
            with open(file_path, 'wb') as file:
                file.write(base64.b64decode(encoded_file))

            # Return path and filename
            return os.path.join(upload_dir, original_filename), original_filename

        except Exception as e:
            raise ValueError("Error saving the base64 file") from e

class VendorListAPIView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)

        modified_data = []
        for vendor in serializer.data:
            vendor_data = dict(vendor)
            document_path = vendor_data.get('document_path')

            if document_path:
                # Full URL to the document
                full_url = f"http://{settings.IP_ADDRESS}:{settings.APP_PORT}/api/media/{document_path}"

                # Extract file name from path
                document_name = os.path.basename(document_path)

                vendor_data['document_path'] = full_url
                vendor_data['document_name'] = document_name  # new field

            modified_data.append(vendor_data)

        return Response(modified_data, status=status.HTTP_200_OK)
        #  for vendorsData in range(len(serializer.data)):
        #     # Check if the 'document_path' exists and is not empty
        #     document_path = serializer.data[vendorsData].get('document_path', None)
            
        #     if document_path:
        #         # If document exists, add full URL
        #         serializer.data[vendorsData]['document_path'] = "http://192.168.1.134:8000/api/media/" + document_path
        #     else:
        #         # If document doesn't exist, set to "No document"
        #         serializer.data[vendorsData]['document_path'] = "No document"

        # return Response(serializer.data, status=status.HTTP_200_OK)




class VendorUpdateAPIView(APIView):
    def patch(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            data = request.data

            # Only update document if a valid base64 string is provided
            if 'document' in data and isinstance(data['document'], str) and data['document'].startswith('data:'):
                document_name = data.get('document_name') or 'uploaded_file.pdf'  # Default name if None or empty
                document_path, saved_name = self.save_base64_file(data['document'], document_name)
                vendor.document_path = document_path
            else:
                vendor.document_path=None

            # Update other fields as usual
            vendor.name = data.get('name', vendor.name)
            vendor.company_name = data.get('company_name', vendor.company_name)
            vendor.mobile = data.get('mobile', vendor.mobile)
            vendor.email = data.get('email', vendor.email)
            vendor.address = data.get('address', vendor.address)
            vendor.gst_no = data.get('gst_no', vendor.gst_no)
            vendor.save()

            return Response({'message': 'Vendor updated successfully'}, status=status.HTTP_200_OK)

        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def save_base64_file(self, base64_data, original_filename):
        try:
            header, encoded_file = base64_data.split(',', 1)

            # Sanitize filename and create path
            original_filename = os.path.basename(original_filename)
            upload_dir = 'vendors'
            upload_path = os.path.join(settings.MEDIA_ROOT, upload_dir)
            os.makedirs(upload_path, exist_ok=True)
            file_path = os.path.join(upload_path, original_filename)

            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(encoded_file))

            return os.path.join(upload_dir, original_filename), original_filename

        except Exception as e:
            raise ValueError("Error saving the base64 file") from e

# class BookingAvailabilityCheckAPIView(APIView):
 
#     def get(self, request):
#         # Retrieve the query parameters
#         start_date_str = request.query_params.get('start_date')
#         end_date_str = request.query_params.get('end_date')
 
#         # Parse the date strings into date objects
#         start_date = parse_date(start_date_str)
#         end_date = parse_date(end_date_str)
 
#         if not start_date or not end_date:
#             return Response(
#                 {"message": "Invalid or missing start_date or end_date query parameters."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
 
#         # Check for overlapping bookings
#         conflicting_bookings = BookingForm.objects.filter(
#             start_date__lte=end_date,
#             end_date__gte=start_date
#         )
 
#         if conflicting_bookings.exists():
#             return Response(
#                 {"available": False, "message": "The selected date range is not available."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         else:
#             return Response(
#                 {"available": True, "message": "The selected date range is available."},
#                 status=status.HTTP_200_OK
#             )
 
class BookingAvailabilityCheckAPIView(APIView):

    # def get(self, request):
    #     start_date_str = request.query_params.get('start_date', '').strip()
    #     end_date_str = request.query_params.get('end_date', '').strip()

    #     # Parse and validate dates
    #     start_date = parse_date(start_date_str)
    #     end_date = parse_date(end_date_str)

    #     if not start_date or not end_date:
    #         return Response(
    #             {"message": "Invalid or missing start_date or end_date."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if start_date > end_date:
    #         return Response(
    #             {"message": "start_date must be before end_date."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # Check for overlap with existing bookings
    #     overlapping_bookings = BookingForm.objects.filter(
    #         start_date__lte=end_date,
    #         end_date__gte=start_date
    #     )

    #     available = not overlapping_bookings.exists()

    #     message = (
    #         "The selected date range is available."
    #         if available else   
    #         "The selected date range is not available."
    #     )

    #     return Response(
    #         {"available": available, "message": message},
    #         status=status.HTTP_200_OK
    #     )
    
    def get(self, request):
        start_date_str = request.query_params.get('start_date', '').strip()
        end_date_str = request.query_params.get('end_date', '').strip()

        # Parse and validate dates
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response(
                {"message": "Invalid or missing start_date or end_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start_date > end_date:
            return Response(
                {"message": "start_date must be before end_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        selected_dates = set()
        date = start_date
        while date <= end_date:
            selected_dates.add(date)
            date += timedelta(days=1)

        booked_dates = set()
        for booking in BookingForm.objects.all(): 
            b_date = booking.start_date
            while b_date <= booking.end_date:
                booked_dates.add(b_date)
                b_date += timedelta(days=1)

        available = any(item not in booked_dates for item in selected_dates)

        message = (
            "The selected date range is available."
            if available else
            "The selected date range is not available."
        )

        return Response(
            {"available": available, "message": message},
            status=status.HTTP_200_OK
        )

    


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

    
class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all().order_by('-submitted_at')
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]

# RETRIEVE, UPDATE, DELETE by ID
class FeedbackRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
   
  
def get_services(request):
    data = [
        {
            "icon": "bi-stars",
            "title": "Event Planners",
            "description": "Professional event planning services",
            "services": [
                "Complete event coordination",
                "Custom event design",
                "Timeline management",
                "On-site coordination",
            ],
        },
        {
            "icon": "bi-music-note-list",
            "title": "Audio/Visual Teams",
            "description": "Technical production services",
            "services": [
                "Sound system setup",
                "Lighting design",
                "Video projection",
                "Live streaming services",
            ],
        },
        {
            "icon": "bi-egg-fried",
            "title": "Catering Services",
            "description": "Food and beverage options",
            "services": [
                "Custom menu creation",
                "Buffet & plated service",
                "Beverage packages",
                "Staff & equipment rental",
            ],
        },
        {
            "icon": "bi-camera",
            "title": "Photography & Video",
            "description": "Event documentation services",
            "services": [
                "Professional photography",
                "Videography & editing",
                "Drone footage",
                "Same-day highlights",
            ],
        },
        {
            "icon": "bi-person-badge",
            "title": "Staffing Solutions",
            "description": "Event personnel services",
            "services": [
                "Event security",
                "Hosts & hostesses",
                "Registration staff",
                "Technical support team",
            ],
        },
    ]
    return JsonResponse(data, safe=False)

class PricingAPIView(APIView):
    def get(self, request):
        data = [
            {
                "title": "Basic",
                "description": "Perfect for small gatherings and presentations",
                "price": "₹ 1,500/day",
                "features": [
                    "8-hour venue access",
                    "Basic lighting setup",
                    "Sound system",
                    "Seating for up to 150 people",
                    "1 technician included",
                    "Basic cleaning included",
                ],
            },
            {
                "title": "Standard",
                "description": "Ideal for conferences and performances",
                "price": "₹ 2,500/day",
                "features": [
                    "10-hour venue access",
                    "Advanced lighting setup",
                    "Professional sound system",
                    "Seating for up to 250 people",
                    "2 technicians included",
                    "Green room access",
                    "Basic video projection",
                    "Full cleaning included",
                ],
            },
            {
                "title": "Premium",
                "description": "Complete package for major events",
                "price": "₹ 3,500/day",
                "popular": True,
                "features": [
                    "12-hour venue access",
                    "Custom lighting design",
                    "Premium sound system",
                    "Full capacity seating (350)",
                    "3 technicians included",
                    "Multiple green rooms",
                    "Advanced AV setup",
                    "Live streaming capability",
                    "Full cleaning service",
                    "Security personnel included",
                ],
            },
            {
                "title": "Custom",
                "description": "Tailored solutions for unique events",
                "price": "Custom",
                "features": [
                    "Flexible hours",
                    "Custom technical setup",
                    "Personalized seating arrangement",
                    "Custom staffing plan",
                    "Specialized equipment rental",
                    "Additional services as needed",
                    "Contact us for a custom quote",
                ],
            },
        ]
        return Response(data)
    

class BookingAPIView(APIView):
    def get(self, request):
        data = [
            {
                "title": "Complete Venue",
                "description": "Full-day or multi-day rentals for exclusive use of our entire venue.",
                "price": "Starting from ₹ 2,500/day",
            },
            {
                "title": "Hourly Booking",
                "description": "Flexible time-based reservations for rehearsals or shorter events.",
                "price": "Starting from ₹ 300/hour",
            },
            {
                "title": "Vendor Packages",
                "description": "Full event management or standalone services from our trusted partners.",
                "price": "Custom pricing",
            },
        ]
        return Response(data)
    
class FeaturesAPIView(APIView):
    def get(self, request):
        data = [
            {
                "icon": "bi-people-fill",
                "title": "350-Seater Auditorium",
                "description": "Spacious seating to accommodate your audience comfortably.",
            },
            {
                "icon": "bi-soundwave",
                "title": "Advanced Sound System",
                "description": "Experience crystal-clear audio for every performance.",
            },
            {
                "icon": "bi-lightbulb",
                "title": "Professional Lighting",
                "description": "Stage lighting that brings your event to life.",
            },
            {
                "icon": "bi-camera-reels",
                "title": "LED Screens & Projectors",
                "description": "Visual aids for presentations, movies, and more.",
            },
            {
                "icon": "bi-door-open",
                "title": "Green Rooms & Facilities",
                "description": "Comfortable backstage areas for performers.",
            },
            {
                "icon": "bi-wifi",
                "title": "High-Speed Wi-Fi",
                "description": "Stay connected with reliable internet access.",
            },
            {
                "icon": "bi-camera",
                "title": "Security Surveillance",
                "description": "Advanced security systems ensuring safety for all your events.",
            },
            {
                "icon": "bi-clock-history",
                "title": "Hourly Booking",
                "description": "Pay only for the hours you need.",
            },
            {
                "icon": "bi-calendar-check",
                "title": "Full-Day Rentals",
                "description": "Enjoy uninterrupted access for the entire day.",
            },
            {
                "icon": "bi-bag-check",
                "title": "Vendor Packages",
                "description": "Catering, decor, and more in one convenient bundle.",
            },
        ]
        return Response(data)

class TestimonialsAPIView(APIView):
    def get(self, request):
        data = [
            {
                "name": "Sarah Johnson",
                "role": "Event Organizer",
                "rating": 5,
                "feedback": "The booking process was incredibly smooth, and the theatre was magnificent. I've already booked my next event here!",
            },
            {
                "name": "Michael Chen",
                "role": "Marketing Director",
                "rating": 4,
                "feedback": "I was impressed by the state-of-the-art facilities and professional staff. My corporate event was a huge success.",
            },
            {
                "name": "Emily Rodriguez",
                "role": "Theatre Enthusiast",
                "rating": 5,
                "feedback": "From the booking process to the final curtain call, everything was perfect. Highly recommend!",
            },
        ]
        return Response(data)

