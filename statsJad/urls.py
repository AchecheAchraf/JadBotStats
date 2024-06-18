from django.urls import path
from .views import protocol_list_with_name, index,form,protocol,protocolrooms,protocolday

urlpatterns = [
    # path('protocolrooms/', protocolrooms, name='protocolrooms'),
    # path('protocolday/', protocolday, name='protocolday'),
    path('protocol/', protocol, name='protocol'),
    path('index/', index, name='index'),
    path('form/', form, name='form'),
    # Add other URL patterns as needed
]
