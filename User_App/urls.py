from django.contrib import admin
from django.urls import path
from User_App import user_views

urlpatterns = [
    path('',user_views.index,name="home"), 
    path('desingnation/<str:id>',user_views.desingnation,name="desingnation"), 
    path('politician/<str:id>',user_views.politician_details,name="politician_details"), 
    path('add_user',user_views.add_user,name="add_user"), 
    path('verify_otp',user_views.verify_otp,name="verify_otp"), 
    path('resend_otp',user_views.resend_otp,name="resend_otp"), 
    path('login_user',user_views.login_user,name="login_user"), 
    path('logout_user',user_views.logout_user,name="logout_user"), 
    path('exist_user',user_views.exist_user,name="exist_user"), 
    path('politician_like',user_views.politician_like,name="politician_like"), 
    path('politician_dislike',user_views.politician_dislike,name="politician_dislike"), 
    path('add_comment',user_views.add_comment,name="add_comment"), 
    path('update_comment',user_views.update_comment,name="update_comment"), 
    path('delete_comment',user_views.delete_comment,name="delete_comment"), 
]