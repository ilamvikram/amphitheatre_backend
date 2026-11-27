from django.urls import path
from .views import BookingAvailabilityCheckAPIView, DeleteEventFolderAPIView, EventCreateView, EventListView, FeedbackCreateView, FeedbackListView, FeedbackRetrieveUpdateDestroyView, RegisterAPIView, CustomLoginView
from . import views
from .views import PricingAPIView, FeaturesAPIView, TestimonialsAPIView, ContactFormCreateAPIView, ContactFormListAPIView, BookingCreateAPIView,BookingListAPIView, VendorUpdateAPIView, VendorCreateAPIView, VendorListAPIView, SuperuserLoginView, ContactUpdateAPIView
from django.conf import settings
from .views import EventDetailView
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-availability/', BookingAvailabilityCheckAPIView.as_view(), name='check-availability'),
    path('contact-form/', ContactFormCreateAPIView.as_view(), name='contact-form-submit'),
    path('contact/update/<int:id>/', ContactUpdateAPIView.as_view(), name='contact-form-update'),
    path('contact-form-list/', ContactFormListAPIView.as_view(), name='contact-form-list'),
    path('bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings-list/', BookingListAPIView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/update/', views.update_booking, name='booking-update'),
    path('vendors/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('vendors-list/', VendorListAPIView.as_view(), name='vendor-list'),
    path('vendors/<int:id>/update/', VendorUpdateAPIView.as_view(), name='update_vendor'),
    path('events/', EventCreateView.as_view(), name='create-event'),
    path('events-list/', EventListView.as_view(), name='events-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('delete-folder/<str:event_type>/', DeleteEventFolderAPIView.as_view(), name='delete-folder'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback-list/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedbackupdate/<int:id>/', FeedbackRetrieveUpdateDestroyView.as_view(), name='feedback-detail'),
    path('get-services/', views.get_services, name='get_services'),
    path('pricing/', PricingAPIView.as_view(), name='pricing'),
    path('features/', FeaturesAPIView.as_view(), name='features'),
    path('testimonials/', TestimonialsAPIView.as_view(), name='testimonials'),  
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    