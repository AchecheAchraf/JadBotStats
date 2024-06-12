from django.urls import path
from .views import protocol_list

urlpatterns = [
    path('protocol/', protocol_list, name='protocol_events'),
    # Add other URL patterns as needed
]
