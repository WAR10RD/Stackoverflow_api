from . import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from .views import * 
app_name = 'frontend'

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    
    
]