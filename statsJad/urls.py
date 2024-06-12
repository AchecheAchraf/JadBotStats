from django.urls import path
from .views import protocol_list_with_name

urlpatterns = [
    path('protocol/', protocol_list_with_name, name='protocol_events'),
    # Add other URL patterns as needed
]
