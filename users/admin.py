from django.contrib import admin
from .models import User
from .models import ContactForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'role']

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'event_type', 'start_date', 'end_date', 'participants', 'slot', 'created_at')
    search_fields = ('name', 'mobile', 'email')
    list_filter = ('event_type', 'start_date', 'end_date')