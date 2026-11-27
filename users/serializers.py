import re
from rest_framework import serializers
from .models import Feedback, User, ContactForm, BookingForm, Vendor
import base64
import uuid
import os
from django.core.files.base import ContentFile
import base64
import os
from django.conf import settings
from datetime import datetime
from rest_framework import serializers
from .models import Event
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from rest_framework import serializers
import os
import base64
import uuid
import os
import uuid
import base64
import re
from django.conf import settings
from urllib.parse import urljoin
from django.conf import settings
from rest_framework import serializers
from .models import Event
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

class BookingFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingForm
        fields = '__all__' 
        
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

# class EventSerializer(serializers.ModelSerializer):
#     event_images = serializers.ListField(
#         child=serializers.CharField(), write_only=True, required=False
#     )

#     class Meta:
#         model = Event
#         fields = ['id', 'event_type', 'event_images', 'images']

#     def create(self, validated_data):
#         event_images = validated_data.pop('event_images', [])
#         event_type = validated_data['event_type'].strip().lower()
#         safe_event_type = re.sub(r'[^\w\-]', '_', event_type)

#         if Event.objects.filter(event_type__iexact=event_type).exists():
#             raise serializers.ValidationError({'event_type': 'This event type already exists.'})

#         event = Event.objects.create(event_type=event_type)

#         folder_path = os.path.join(settings.MEDIA_ROOT, safe_event_type)
#         os.makedirs(folder_path, exist_ok=True)

#         saved_paths = []

#         for base64_str in event_images:
#             if ';base64,' not in base64_str:
#                 continue

#             try:
#                 header, data = base64_str.split(';base64,')
#                 ext = header.split('/')[-1].lower()

#                 if ext not in ['jpg', 'jpeg', 'png', 'gif']:
#                     raise serializers.ValidationError({'format': f"Unsupported format: {ext}"})

#                 filename = f"{uuid.uuid4().hex}.{ext}"
#                 filepath = os.path.join(folder_path, filename)

#                 with open(filepath, 'wb') as f:
#                     f.write(base64.b64decode(data))

#                 relative_path = os.path.join(safe_event_type, filename)
#                 saved_paths.append(relative_path)

#             except Exception as e:
#                 raise serializers.ValidationError({'image_error': str(e)})

#         event.images = saved_paths
#         event.save()
#         return event

class     EventSerializer(serializers.ModelSerializer):
    event_images = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Event
        fields = ['id', 'event_type', 'event_images', 'images']


    def create(self, validated_data):
        event_images = validated_data.pop('event_images', [])
        original_event_type = validated_data['event_type']  # Store exactly as sent
        safe_event_type = re.sub(r'[^\w\-]', '_', original_event_type.strip().lower())  # Safe for folder name

        # Ensure event_type uniqueness (case-insensitive)
        if Event.objects.filter(event_type__iexact=original_event_type).exists():
            raise serializers.ValidationError({'event_type': 'This event type already exists.'})

        # Create event without images first
        event = Event.objects.create(event_type=original_event_type)

        # Create folder for this event type inside MEDIA_ROOT
        folder_path = os.path.join(settings.MEDIA_ROOT, safe_event_type)
        os.makedirs(folder_path, exist_ok=True)


        saved_paths = []

        for base64_str in event_images:
            if ';base64,' not in base64_str:
                continue  # or raise ValidationError

            try:
                header, data = base64_str.split(';base64,')
                ext = header.split('/')[-1].lower()


                if ext == 'svg+xml':  # Normalize svg+xml to svg
                    ext = 'svg'

                if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                    raise serializers.ValidationError({'format': f"Unsupported format: {ext}"})

                filename = f"{uuid.uuid4().hex}.{ext}"
                filepath = os.path.join(folder_path, filename)

                # Save image to media folder
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(data))

                # Save relative path (relative to MEDIA_ROOT)
                relative_path = os.path.join(safe_event_type, filename)
                saved_paths.append(relative_path)

            except Exception as e:
                raise serializers.ValidationError({'image_error': str(e)})

        # Save list of relative paths in DB
        event.images = saved_paths
        event.save()
        return event
    
    def update(self, instance, validated_data):

    # Extract and normalize event_type (new or existing)
        original_event_type = validated_data.get('event_type', instance.event_type)
        safe_event_type = re.sub(r'[^\w\-]', '_', original_event_type.strip().lower())
 
    # Update the event_type on the instance
        instance.event_type = original_event_type
 
    # Handle optional base64 image upload
        event_images = validated_data.pop('images', None)
        if event_images is not None:
            saved_image_urls = []
 
        # Ensure directory exists
            folder_path = os.path.join(settings.MEDIA_ROOT, safe_event_type)
            os.makedirs(folder_path, exist_ok=True)
 
        for img_str in event_images:
            try:
                if ';base64,' not in img_str:
                    raise serializers.ValidationError({'image_format': 'Invalid base64 format.'})
 
                format, img_b64 = img_str.split(';base64,')
                ext = format.split('/')[-1].lower()

                if ext == 'svg+xml':
                    ext = 'svg'

                if ext not in ['jpg', 'jpeg', 'png', 'webp', 'svg' ]:
                    raise serializers.ValidationError({'image_format': f'Unsupported type: {ext}'})
 
                filename = f"{uuid.uuid4()}.{ext}"
                filepath = os.path.join(folder_path, filename)
 
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(img_b64))
 
                image_url = f"{settings.MEDIA_URL}{safe_event_type}/{filename}"
                saved_image_urls.append(image_url)
 
            except Exception as e:
                raise serializers.ValidationError({'image_error': str(e)})
 
        # Replace existing image URLs with new ones
        instance.images = saved_image_urls
 
        instance.save()
        return instance
    
# def to_representation(self, instance):
#     rep = super().to_representation(instance)
#     base_url = "http://localhost:8000"  # Or use request.build_absolute_uri()
#     rep['images'] = [urljoin(base_url, f"{settings.MEDIA_URL}{img}") for img in instance.images]
#     return rep

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'