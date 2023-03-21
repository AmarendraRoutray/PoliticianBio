"""PoliticianBio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Admin_App import admin_views

urlpatterns = [
    
    # path('',admin_views.admin_login,name="admin_login"), 
    # path('Verify/login',admin_views.admin_verify_login,name="admin_verify_login"), 
    path('logout',admin_views.admin_logout,name="admin_logout"), 
    path('dashboard',admin_views.admin_dashboard,name="admin_dashboard"),

    path('states',admin_views.states,name="states"),
    path('create_state',admin_views.create_state,name="create_state"),
    path('update_state',admin_views.update_state,name="update_state"),
    path('delete_state/<str:id>',admin_views.delete_state,name="delete_state"),

    path('district',admin_views.district,name="district"),  
    path('create_district',admin_views.create_district,name="create_district"),
    path('update_district',admin_views.update_district,name="update_district"),
    path('delete_district/<str:id>',admin_views.delete_district,name="delete_district"),

    path('constitution',admin_views.constitution,name="constitution"),  
    path('create_constitution',admin_views.create_constitution,name="create_constitution"),
    path('update_constitution',admin_views.update_constitution,name="update_constitution"),
    path('delete_constitution/<str:id>',admin_views.delete_constitution,name="delete_constitution"),

    path('desingnation',admin_views.desingnation,name="desingnation"),  
    path('create_desingnation',admin_views.create_desingnation,name="create_desingnation"),
    path('delete_desingnation/<str:id>',admin_views.delete_desingnation,name="delete_desingnation"),

    path('edit_politician/<str:id>',admin_views.edit_politician,name="edit_politician"),
    path('update_politician',admin_views.update_politician,name="update_politician"), 
    path('view_politician',admin_views.view_politician,name="view_politician"), 
    path('about_politician/<str:id>',admin_views.about_politician,name="about_politician"), 
    path('delete_user_comment/<str:id>/<str:poli_id>',admin_views.delete_user_comment,name="delete_user_comment"), 
    path('politician',admin_views.politician,name="politician"), 
    path('create_politician',admin_views.create_politician,name="create_politician"), 
    path('delete_politician<str:id>',admin_views.delete_politician,name="delete_politician"), 
    path('fetch_district',admin_views.fetch_district,name="fetch_district"), 
    path('fetch_constitution',admin_views.fetch_constitution,name="fetch_constitution"), 
    path('fetch_desingnation',admin_views.fetch_desingnation,name="fetch_desingnation"), 
    path('politician_image_video/<str:poli_id>',admin_views.politician_image_video,name="politician_image_video"), 
    path('upload_image_slider',admin_views.upload_image_slider,name="upload_image_slider"), 
    path('delete_image_slider/<str:id>/<str:poli_id>',admin_views.delete_image_slider,name="delete_image_slider"), 
    path('upload_video_slider',admin_views.upload_video_slider,name="upload_video_slider"),     
    path('delete_video_slider/<str:id>/<str:poli_id>',admin_views.delete_video_slider,name="delete_video_slider"),     
    path('advertise_image_slider',admin_views.advertise_image_slider,name="advertise_image_slider"), 
    path('save_advertise_image_slider',admin_views.save_advertise_image_slider,name="save_advertise_image_slider"), 
    path('delete_advertise_image_slider/<str:id>',admin_views.delete_advertise_image_slider,name="delete_advertise_image_slider"),
    path('admin_profile',admin_views.admin_profile,name='admin_profile'),
    path('admin_change_email',admin_views.admin_change_email,name='admin_change_email'),
    path('admin_change_password',admin_views.admin_change_password,name="admin_change_password"),
    path('send_mail_test',admin_views.send_mail_test,name="send_mail_test"),

 

]
