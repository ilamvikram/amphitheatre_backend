from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import os
import uuid
from django.db import models
class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, role='customer'):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(username=username, phone_number=phone_number, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password):
        user = self.create_user(username, phone_number, password, role='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('customer', 'Customer'),
    )
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    
class CustomUser(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.phone_number
    
class ContactForm(models.Model):
    name = models.CharField(max_length=100)  # required
    country_code = models.CharField(max_length=5, null=True, blank=True)
    mobile = models.CharField(max_length=10)  # required
    email = models.EmailField()  # required
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    participants = models.CharField(max_length=400, null=True, blank=True)
    slot = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(max_length=100, null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event_type}"

class BookingForm(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, default='+91')
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    slot = models.CharField(max_length=100, null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    participants = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
     
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, default='+91')
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    gst_no = models.CharField(max_length=30)
    document_path = models.CharField(max_length=255, default='there_is_no_document', null=True, blank=True)  # Provide a default value
    document_name = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return self.name


class Event(models.Model):
    event_type = models.CharField(max_length=255, unique=True)
    images = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.event_type

from django.db import models

class Feedback(models.Model):
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Optional name of the person giving feedback"
    )

    email = models.EmailField(
        null=True,
        blank=True,
        help_text="Email address for contact (optional)"
    )

    mobile = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="10-digit mobile number (optional)"
    )

    message = models.TextField(
        null=True,
        blank=True,
        help_text="Feedback message"
    )

    rating = models.IntegerField(
        help_text="Rating given by user (e.g., 1 to 5)"
    )

    feedback_status = models.BooleanField(
        default=False,  # ✅ Required for BooleanField
        help_text="Status flag for internal use (e.g., reviewed)"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when feedback was submitted"
    )

    def __str__(self):
        return f"{self.name or 'Anonymous'} - {self.rating}★"

