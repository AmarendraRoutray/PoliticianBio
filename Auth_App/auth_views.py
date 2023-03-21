from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from Admin_App.AuthBackend import AuthBackend
from Admin_App.models import State,District,Constitution,Desingnation,Politician,Politician_image_slider,Politician_video_slider,Comment
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings

import json,uuid,os
# Create your views here.
def admin_login(request):
    return render(request,'auth_template/login.html')
def admin_verify_login(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=AuthBackend.authenticate(request,email=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            if user.is_active==True and user.user_type=="1":
                user.backend = 'Admin_App.AuthBackend.AuthBackend' 
                log_in(request,user)
                return HttpResponseRedirect(reverse("admin_dashboard"))
            else:
                messages.error(request,"Your Account Is Disable ! Contact Company Owner")
                return HttpResponseRedirect(reverse('admin_login'))

        else:
            print("invalid cred")
            messages.error(request,"Invalid Credintial")
            return HttpResponseRedirect(reverse('admin_login'))


