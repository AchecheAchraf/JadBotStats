from django.urls import path
from .views import  index,form,protocol

urlpatterns = [
    # path('protocolrooms/', protocolrooms, name='protocolrooms'),
    # path('protocolday/', protocolday, name='protocolday'),
    path('protocol/', protocol, name='protocol'),
    path('index/', index, name='index'),
    path('form/', form, name='form'),
    # Add other URL patterns as needed
]
