from typing import Text
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from Admin_App.AuthBackend import AuthBackend
from django.views.decorators.csrf import csrf_exempt
from Admin_App.models import State, District, Constitution, Desingnation, Politician, Otp, Politician_image_slider, CustomUser, Comment, Advertise, Politician_video_slider
import json
import random
from datetime import date
from django.db.models import Count
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.conf import settings

# Create your views here.


def index(request):
    state = State.objects.all().order_by('name')
    district = District.objects.all().order_by('name')
    constitution = Constitution.objects.all().order_by('name')
    desingnation = Desingnation.objects.all().order_by('name')
    politician = Politician.objects.all().order_by('name')
    top_poli = Politician.objects.all().annotate(
        total_likes=Count('likes')).order_by('-total_likes')[:10]
    adv = Advertise.objects.all()
    context = {
        "state": state,
        "district": district,
        "constitution": constitution,
        "desingnation": desingnation,
        "politician": politician, 'top_poli': top_poli, "adv": adv
    }
    return render(request, 'user_template/index.html', context)
    # return render(request, 'user_template/comming_soon.html', context)


def desingnation(request, id):
    # state= State.objects.all().order_by('name')
    # district= District.objects.all().order_by('name')
    # constitution = Constitution.objects.all().order_by('name')
    #desingnation = Desingnation.objects.all().order_by('name')
    politician = Politician.objects.filter(
        desingnation=id).order_by('-created_at').first()
    #desing = Desingnation.objects.get(id = id)
    return HttpResponseRedirect(reverse('politician_details', kwargs={"id": politician.id}))


def politician_details(request, id):
    poli = Politician.objects.get(id=id)
    img_slider = Politician_image_slider.objects.filter(politician=id)
    video_slider = Politician_video_slider.objects.filter(politician=id)
    is_like = poli.likes.filter(id=request.user.id).exists()
    is_dislike = poli.dislikes.filter(id=request.user.id).exists()
    all_comments = Comment.objects.filter(
        politician=id).order_by('-created_at')
    comment_count = Comment.objects.filter(politician=id).count()
    state = State.objects.all().order_by('name')
    district = District.objects.all().order_by('name')
    constitution = Constitution.objects.all().order_by('name')
    desingnation = Desingnation.objects.all().order_by('name')
    #politician = Politician.objects.all().order_by('name')
    recomonded_politician = Politician.objects.filter(state=poli.state.id).exclude(
        id=poli.id).annotate(total_likes=Count('likes')).order_by('-total_likes')[:10]
    video_slider_count = Politician_video_slider.objects.filter(
        politician=id).count()
    img_slider_count = Politician_image_slider.objects.filter(
        politician=id).count()
    context = {
        "poli": poli,
        "img_slider": img_slider,
        'total_likes': poli.total_likes(),
        'total_dislikes': poli.total_dislikes(),
        "is_like": is_like,
        "is_dislike": is_dislike, "comment_count": comment_count, "all_comments": all_comments,
        "state": state,
        "district": district,
        "constitution": constitution,
        "desingnation": desingnation,
        "video_slider": video_slider, "video_slider_count": video_slider_count, "img_slider_count": img_slider_count,
        "DOMAIN": settings.DOMAIN,
        "recomonded_politician": recomonded_politician
    }
    return render(request, 'user_template/politician_details.html', context)


@csrf_exempt
def add_user(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        exist_user = CustomUser.objects.filter(
            email=email, is_active=True).exists()
        if not exist_user:
            uv_user = CustomUser.objects.filter(email=email, is_active=False)
            if len(uv_user) > 0:
                for o in uv_user:
                    otp_exp_time = o.created_at + timedelta(minutes=2)
                    if otp_exp_time < timezone.now():
                        o.delete()
                    else:
                        pass
            else:
                pass
            user = CustomUser.objects.create_user(
                password=password, email=email, name=name, user_type=3, is_active=False)
            user.save()
            otp = random.randint(100000, 999999)
            old_otp = Otp.objects.filter(customuser=user.id)
            if len(old_otp) > 0:
                old_otp.delete()
            gen_opt = Otp(customuser=user, text=otp)
            gen_opt.save()
            # sendotp Function email
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            message = "Your One Time Password (OTP) is " + str('otp')
            subject = "Amaneta Email Verification OTP"
            print("send amaneta")
            msg = EmailMessage(
                subject,
                message,
                email_from,
                email_to,
            )
            # msg.send()
            print("OTP is #############  ", otp)
            data = {"message": "success", "email": email}
            return JsonResponse(data, content_type="application/json", safe=False,)
        else:
            data = {"message": "userexist"}
            return JsonResponse(data, content_type="application/json", safe=False,)
    except Exception as e:
        print(e)
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def verify_otp(request):
    otp = request.POST.get('otp')
    email = request.POST.get('email')
    try:
        exist_user = CustomUser.objects.filter(email=email).exists()
        if exist_user:
            user = CustomUser.objects.get(email=email)
            otp_object = Otp.objects.get(customuser=user.id)
            original_otp = otp_object.text
            if int(original_otp) == int(otp):
                user.is_active = True
                user.save()
                otp_object.delete()
                log_in(request, user)
                data = {"message": "success", "email": email}
                return JsonResponse(data, content_type="application/json", safe=False,)
            else:
                data = {"message": "invalid_otp", "email": email}
                return JsonResponse(data, content_type="application/json", safe=False,)
        else:
            data = {"message": "userexist"}
            return JsonResponse(data, content_type="application/json", safe=False,)
    except Exception as e:
        print(e)
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def resend_otp(request):
    email = request.POST.get('email')
    try:
        exist_user = CustomUser.objects.filter(email=email).exists()
        if exist_user:
            user = CustomUser.objects.get(email=email)
            otp_object = Otp.objects.filter(customuser=user.id)
            if len(otp_object) > 0:
                otp_object.delete()
            otp = random.randint(100000, 999999)
            gen_opt = Otp(customuser=user, text=otp)
            gen_opt.save()
            # sendotp Function email
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            message = "Your One Time Password (OTP) is " + str('otp')
            subject = "Amaneta Email Verification OTP"

            msg = EmailMessage(
                subject,
                message,
                email_from,
                email_to,
            )
            msg.send()
            print("OTP is #############  ", otp)
            data = {"message": "success", "email": email}
            return JsonResponse(data, content_type="application/json", safe=False,)
        else:
            data = {"message": "userexist"}
            return JsonResponse(data, content_type="application/json", safe=False,)
    except Exception as e:
        print(e)
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def exist_user(request):
    email = request.POST.get('email')
    try:
        exist_user = CustomUser.objects.filter(
            email=email, user_type=3).exists()
        if exist_user:
            data = {"message": "success"}
            return JsonResponse(data, content_type="application/json", safe=False,)
        else:
            data = {"message": "error"}
            return JsonResponse(data, content_type="application/json", safe=False,)
    except Exception as e:
        print(e)
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return HttpResponse("method Not allowed")
    else:
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_check = CustomUser.objects.filter(email=email, user_type ='3')
            if not  user_check.exists():
                print("failed")
                data = {"message": "Invalid Email"}
                return JsonResponse(data, content_type="application/json", safe=False,)
            user=AuthBackend.authenticate(request,email,password)
            if user != None:
                log_in(request, user)
                data = {"message": "success"}
                return JsonResponse(data, content_type="application/json", safe=False,)
            else:
                print("failed")
                data = {"message": "Invalid Password"}
                return JsonResponse(data, content_type="application/json", safe=False,)
        except Exception as e:
            print(e)
            data = {"message": "somethingwrong"}
            return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        log_out(request)
        data = {"message": "success"}
        return JsonResponse(data, content_type="application/json", safe=False,)
    else:
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def politician_like(request):
    user_id = request.POST.get('user_id')
    poli_id = request.POST.get('poli_id')
    politician = Politician.objects.get(id=poli_id)
    if not politician.likes.filter(id=user_id).exists():
        politician.likes.add(CustomUser.objects.get(id=user_id))
        if politician.dislikes.filter(id=user_id).exists():
            politician.dislikes.remove(CustomUser.objects.get(id=user_id))
            data = {"message": "likeadd", 'total_likes': politician.total_likes(
            ), "message2": "dislike_plus", 'total_dislikes': politician.total_dislikes()}
            return JsonResponse(data, content_type="application/json", safe=False)
        else:
            pass
        data = {"message": "likeadd", 'total_likes': politician.total_likes()}
        return JsonResponse(data, content_type="application/json", safe=False)
    else:
        politician.likes.remove(CustomUser.objects.get(id=user_id))
        data = {"message": "likeremove",
                'total_likes': politician.total_likes()}
        return JsonResponse(data, content_type="application/json", safe=False)


@csrf_exempt
def politician_dislike(request):
    user_id = request.POST.get('user_id')
    poli_id = request.POST.get('poli_id')
    politician = Politician.objects.get(id=poli_id)
    if not politician.dislikes.filter(id=user_id).exists():
        politician.dislikes.add(CustomUser.objects.get(id=user_id))
        if politician.likes.filter(id=user_id).exists():
            politician.likes.remove(CustomUser.objects.get(id=user_id))
            data = {"message": "likeadd", 'total_dislikes': politician.total_dislikes(
            ), "message2": "like_plus", 'total_likes': politician.total_likes()}
            return JsonResponse(data, content_type="application/json", safe=False,)
        else:
            pass
        data = {"message": "dislikeadd",
                'total_dislikes': politician.total_dislikes()}
        return JsonResponse(data, content_type="application/json", safe=False,)
    else:
        politician.dislikes.remove(CustomUser.objects.get(id=user_id))
        data = {"message": "dislikeremove",
                'total_dislikes': politician.total_dislikes()}
        return JsonResponse(data, content_type="application/json", safe=False,)


def add_comment(request):
    user_id = request.POST.get('user_id')
    poli_id = request.POST.get('poli_id')
    text = request.POST.get('comment_text')
    comment_image = request.FILES.get('comment_image')
    print('text is ', comment_image)
    politician = Politician.objects.get(id=poli_id)
    customuser = CustomUser.objects.get(id=user_id)
    if text != '':
        comment = Comment(politician=politician,
                          customuser=customuser, text=text, image=comment_image)
        comment.save()
        return HttpResponseRedirect(reverse('politician_details', kwargs={"id": poli_id}))
    else:
        return HttpResponseRedirect(reverse('politician_details', kwargs={"id": poli_id}))


@csrf_exempt
def update_comment(request):
    com_id = request.POST.get('com_id')
    print(com_id)
    comment_text = request.POST.get('comment')
    if comment_text != '':
        comment = Comment.objects.get(id=com_id)
        comment.text = comment_text
        comment.save()
        data = {"message": "commentupdated"}
        return JsonResponse(data, content_type="application/json", safe=False,)
    else:
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)


@csrf_exempt
def delete_comment(request):
    com_id = request.POST.get('com_id')
    if com_id != '':
        comment = Comment.objects.get(id=com_id)
        comment.delete()
        data = {"message": "commentdelete"}
        return JsonResponse(data, content_type="application/json", safe=False,)
    else:
        data = {"message": "somethingwrong"}
        return JsonResponse(data, content_type="application/json", safe=False,)
