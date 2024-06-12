from django.urls import path
from .views import protocol_list_with_name, index

urlpatterns = [
    path('protocol/', protocol_list_with_name, name='protocol_events'),
    path('index/', index, name='index'),
    # Add other URL patterns as needed
]
