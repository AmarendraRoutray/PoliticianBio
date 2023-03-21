from django.contrib import admin
from django.urls import path
from Auth_App import auth_views

urlpatterns = [
    
    path('',auth_views.admin_login,name="admin_login"), 
    path('Verify/login',auth_views.admin_verify_login,name="admin_verify_login"), 
]