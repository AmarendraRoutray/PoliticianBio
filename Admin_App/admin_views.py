from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from Admin_App.AuthBackend import AuthBackend
from django.contrib.auth import get_user_model
from Admin_App.models import State,District,Constitution,Desingnation,Politician,Politician_image_slider,Politician_video_slider,Comment,Advertise,CustomUser
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
import json,uuid,os
from django.db.models import Count
# Create your views here.d

def admin_logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('admin_login'))
def admin_dashboard(request):
    top_poli = Politician.objects.all().annotate(total_likes=Count('likes')).order_by('-total_likes')[:10]
    no_of_user = CustomUser.objects.filter(user_type ="3", is_active =True).count()
    no_of_poli = Politician.objects.all().count()
    context={
     "top_poli":top_poli,"no_of_user":no_of_user ,"no_of_poli":no_of_poli  
    }
    return render(request,'admin_template/dashboard.html',context)

#show state page
def states(request):
    state = State.objects.all().order_by("name")
    return render(request,'admin_template/states.html',{'state':state })
def create_state(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get('state_name')
        try:
            if name !='':
                name_exist = State.objects.filter(name = name).exists()
                if not name_exist:
                    state = State(name=name)
                    state.save()
                    messages.success(request,"New State  {} Added".format(name))
                    return HttpResponseRedirect(reverse('states'))
                else:
                    messages.error(request,"State {} Already Exist".format(name))
                    return HttpResponseRedirect(reverse('states'))
            else:
                messages.error(request,"State Name Should Not Be Blank")
                return HttpResponseRedirect(reverse('states'))
        except:
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('states'))

def delete_state(request,id):
    try:
        State.objects.get(id = id).delete()
        messages.success(request,"State Deleted")
        return HttpResponseRedirect(reverse('states'))
    except:
        messages.error(request,"Something Went Wrong")
        return HttpResponseRedirect(reverse('states'))
def update_state(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        name = request.POST.get('edit_state_name')
        state_id = request.POST.get('edit_state_id')
        try:
            if name !='':
                name_exist = State.objects.filter(name = name).exists()
                if not name_exist:
                    state = State.objects.get(id = state_id)
                    state.name = name
                    state.save()
                    messages.success(request," State  {} Updated".format(name))
                    return HttpResponseRedirect(reverse('states'))
                else:
                    messages.error(request,"State {} Already Exist".format(name))
                    return HttpResponseRedirect(reverse('states'))
            else:
                messages.error(request,"State Name Should Not Be Blank")
                return HttpResponseRedirect(reverse('states'))
        except:
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('states'))

#politician Category
@csrf_exempt
def fetch_district(request):
    state_id=request.POST.get('state_id')
    district = District.objects.filter(state = state_id).values('id','name')
    return JsonResponse(json.dumps(list(district)),content_type="application/json",safe=False,)
@csrf_exempt
def fetch_constitution(request):
    district_id=request.POST.get('district_id')
    constitution = Constitution.objects.filter(district = district_id).values('id','name')
    return JsonResponse(json.dumps(list(constitution)),content_type="application/json",safe=False,)
@csrf_exempt
def fetch_desingnation(request):
    constitution_id=request.POST.get('constitution_id')
    desingnation = Desingnation.objects.filter(constitution = constitution_id).values('id','name')
    print('constitution',desingnation)
    return JsonResponse(json.dumps(list(desingnation)),content_type="application/json",safe=False,)

def district(request):
    state = State.objects.all().order_by("name")
    district = District.objects.all().order_by("name").select_related('state')
    return render(request,'admin_template/district.html',{'state':state,'district':district })
def create_district(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        state_id = request.POST.get('state_id')
        name = request.POST.get('district')
        
        try:
            if name !='' and state_id != None:
                state = State.objects.get(id=state_id)
                district = District(state=state,name=name)
                district.save()
                messages.success(request,"New District  {} Added".format(name))
                return HttpResponseRedirect(reverse('district'))
            else:
                messages.error(request,"Please Fill All The Filed")
                return HttpResponseRedirect(reverse('district'))
        except Exception as e:
            print(e)
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('district'))

def delete_district(request,id):
    try:
        District.objects.get(id = id).delete()
        messages.success(request,"District Deleted")
        return HttpResponseRedirect(reverse('district'))
    except:
        messages.error(request,"Something Went Wrong")
        return HttpResponseRedirect(reverse('district'))


def update_district(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        edit_district = request.POST.get('edit_district')
        edit_state_id = request.POST.get('edit_state_id')
        edit_district_id = request.POST.get('edit_district_id')
        try:
            if edit_district !='' and edit_state_id != None:
                state = State.objects.get(id=edit_state_id)
                district = District.objects.get(id=edit_district_id)
                district.state = state
                district.name = edit_district
                district.save()
                messages.success(request,"District  {} Updated".format(edit_district))
                return HttpResponseRedirect(reverse('district'))
            else:
                messages.error(request,"Please Fill All The Filed")
                return HttpResponseRedirect(reverse('district'))
        except Exception as e:
            print("################## error $$$$$$",e)
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('district'))


def constitution(request):
    state = State.objects.all().order_by("name")
    district = District.objects.all().order_by("name").select_related('state')
    constitution = Constitution.objects.all().order_by("name").select_related('state')
    return render(request,'admin_template/constitution.html',{'state':state,'constitution':constitution,"district":district })

def create_constitution(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        state_id = request.POST.get('state_id')
        district_id = request.POST.get('district_id')
        name = request.POST.get('constitution')
        
        try:
            if name !='' and state_id != None and district_id != None:
                state = State.objects.get(id=state_id)
                district = District.objects.get(id=district_id)
                constitution = Constitution(state=state,district=district,name=name)
                constitution.save()
                messages.success(request,"New Constitution  {} Added".format(name))
                return HttpResponseRedirect(reverse('constitution'))
            else:
                messages.error(request,"Please Fill All The Filed")
                return HttpResponseRedirect(reverse('constitution'))
        except Exception as e:
            print(e)
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('constitution'))

def delete_constitution(request,id):
    try:
        Constitution.objects.get(id = id).delete()
        messages.success(request,"Constitution Deleted")
        return HttpResponseRedirect(reverse('constitution'))
    except:
        messages.error(request,"Something Went Wrong")
        return HttpResponseRedirect(reverse('constitution'))

def update_constitution(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        state_id = request.POST.get('edit_state_id')
        district_id = request.POST.get('edit_district_id')
        name = request.POST.get('edit_constitution')
        edit_constitution_id = request.POST.get('edit_constitution_id')
        
        try:
            if name !='' and state_id != None and district_id != None:
                state = State.objects.get(id=state_id)
                district = District.objects.get(id=district_id)
                constitution = Constitution.objects.get(id = edit_constitution_id)
                constitution.state=state
                constitution.district=district
                constitution.name=name
                constitution.save()
                messages.success(request,"Constitution  {} Updated".format(name))
                return HttpResponseRedirect(reverse('constitution'))
            else:
                messages.error(request,"Please Fill All The Filed")
                return HttpResponseRedirect(reverse('constitution'))
        except Exception as e:
            print(e)
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('constitution'))


def desingnation(request):
    state = State.objects.all().order_by("name")
    desingnation = Desingnation.objects.all().order_by("name")
    return render(request,'admin_template/desingnation.html',{'state':state,'desingnation':desingnation })

def create_desingnation(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        state_id = request.POST.get('state_id')
        district_id = request.POST.get('district_id')
        constitution_id = request.POST.get('constitution_id')
        name = request.POST.get('desingnation')
        try:
            if name !='' and state_id != None and district_id != None and constitution_id != None:
                state = State.objects.get(id=state_id)
                district = District.objects.get(id=district_id)
                constitution = Constitution.objects.get(id=constitution_id)
                desingnation = Desingnation(state=state,district=district,constitution=constitution,name=name)
                desingnation.save()
                messages.success(request,"New Desingnation  {} Added".format(name))
                return HttpResponseRedirect(reverse('desingnation'))
            else:
                messages.error(request,"Please Fill All The Filed")
                return HttpResponseRedirect(reverse('desingnation'))
        except Exception as e:
            print(e)
            messages.error(request,"Something Went Wrong")
            return HttpResponseRedirect(reverse('desingnation'))
def delete_desingnation(request,id):
    try:
        Desingnation.objects.get(id = id).delete()
        messages.success(request,"Desingnation Deleted")
        return HttpResponseRedirect(reverse('desingnation'))
    except:
        messages.error(request,"Something Went Wrong")
        return HttpResponseRedirect(reverse('desingnation'))

def politician(request):
    state = State.objects.all().order_by("name")
    poli_cat = District.objects.all().order_by("name")
    return render(request,'admin_template/politician.html',{'state':state,'poli_cat':poli_cat })
def create_politician(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        state_id = request.POST.get('state_id')
        district_id = request.POST.get('district_id')
        constitution_id = request.POST.get('constitution_id')
        desingnation_id = request.POST.get('desingnation_id')
        name = request.POST.get('polician_name')
        desc = request.POST.get('desc')
        profile_image = request.FILES.get('profile_image')
        party_logo = request.FILES.get('party_logo')
        try:
            if name != '' and desc != '' and profile_image != None and state_id != None and district_id != None and constitution_id != None and desingnation_id != None:
                state = State.objects.get(id =state_id)
                district = District.objects.get(id= district_id)
                constitution = Constitution.objects.get(id = constitution_id)
                desingnation = Desingnation.objects.get(id = desingnation_id)
                if party_logo != None:
                    politician = Politician(state=state,district= district,constitution= constitution,desingnation=desingnation,name=name,desc=desc,profile=profile_image, party_logo = party_logo)
                else:
                    politician = Politician(state=state,district= district,constitution= constitution,desingnation=desingnation,name=name,desc=desc,profile=profile_image)
                politician.save()
                politician_id = politician.id
                messages.success(request,"New Politician {} Added".format(name))
                return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
            else:
                messages.error(request,"Please Fill All The Fileds")
                return HttpResponseRedirect(reverse('politician'))
        except Exception as e:
            messages.error(request,"Something Went Wrong {}".format(e))
            return HttpResponseRedirect(reverse('politician'))
def view_politician(request):
    politician = Politician.objects.all().order_by("name")
    poli_cat = District.objects.all().order_by("name")
    return render(request,'admin_template/view_politician.html',{'politician':politician,'poli_cat':poli_cat })
def delete_politician(request,id):
    img = Politician_image_slider.objects.filter(politician = id)
    video = Politician_video_slider.objects.filter(politician = id)
    for i in img:
        if i:
            os.remove(os.path.join(settings.MEDIA_ROOT,str(i.image)))
    for v in video:
        if v:
            os.remove(os.path.join(settings.MEDIA_ROOT,str(v.video)))
    pp = Politician.objects.get(id=id).profile
    os.remove(os.path.join(settings.MEDIA_ROOT,str(pp)))
    Politician.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('view_politician'))
########-----------about_politician view function----------------###################
''' show all the details of a particular politician 
Here edit option will show for politician details  , his images slider also video slider update
'''
def about_politician(request,id):
    politician = Politician.objects.get(id = id)
    like = politician.total_likes()
    dislike = politician.total_dislikes()
    last_comment= Comment.objects.filter(politician = id).order_by('-created_at')[:2]
    all_comment= Comment.objects.filter(politician = id).order_by('-created_at')
    poli_img_slider = Politician_image_slider.objects.filter(politician=id)
    poli_video_slider = Politician_video_slider.objects.filter(politician=id)
    comment = Comment.objects.filter(politician = id).count()
    context ={'politician':politician ,"like":like,"dislike":dislike,
    "comment":comment,"last_comment":last_comment,"all_comment":all_comment,
    "poli_img_slider":poli_img_slider,"poli_video_slider":poli_video_slider}
    return render(request,'admin_template/about_politician.html',context)
def edit_politician(request,id):
    state = State.objects.all().order_by("name")
    all_data = Politician.objects.all().select_related('state')
    district = District.objects.all().order_by("name").select_related('state')
    constitution = Constitution.objects.all().order_by("name").select_related('state')
    desingnation = Desingnation.objects.all().order_by("name").select_related('state')
    politician = Politician.objects.get(id = id)
    context={'politician':politician,"all_data":all_data,"state":state,"district":district,"constitution":constitution,"desingnation":desingnation}
    return render(request,'admin_template/edit_politician.html',context)
####################-----------update politician view function--------------################################### 
def update_politician(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        politician_id = request.POST.get('politician_id')
        state_id = request.POST.get('state_id')
        district_id = request.POST.get('district_id')
        print("districy_id",district_id)
        constitution_id = request.POST.get('constitution_id')
        desingnation_id = request.POST.get('desingnation_id')
        name = request.POST.get('polician_name')
        desc = request.POST.get('desc')
        profile_image = request.FILES.get('profile_image')
        party_logo = request.FILES.get('party_logo')
        try:
            if name != '' and desc != '' and state_id != None and district_id != None and constitution_id != None and desingnation_id != None:
                state = State.objects.get(id =state_id)
                district = District.objects.get(id= district_id)
                constitution = Constitution.objects.get(id = constitution_id)
                desingnation = Desingnation.objects.get(id = desingnation_id)
                politician = Politician.objects.get(id = politician_id)
                politician.state = state
                politician.district = district
                politician.constitution = constitution
                politician.desingnation = desingnation
                politician.name = name
                politician.desc = desc
                #if profile image is something then delete old image and set new image as profile image
                if profile_image != None:
                    old_pic_path = os.path.join(settings.MEDIA_ROOT,str(politician.profile))
                    if os.path.isfile(old_pic_path): 
                        os.remove(old_pic_path)
                    politician.profile = profile_image

                if party_logo != None:
                    old_logo_path = os.path.join(settings.MEDIA_ROOT,str(politician.party_logo))
                    if os.path.isfile(old_logo_path):
                        os.remove(old_logo_path)
                    politician.party_logo = party_logo
                
                
                politician.save()
                messages.success(request,"Politician {} Updated Successfully".format(name))
                return HttpResponseRedirect(reverse('edit_politician',kwargs={'id':politician_id}))
            else:
                messages.error(request,"Please Fill All The Fileds")
                return HttpResponseRedirect(reverse('edit_politician',kwargs={'id':politician_id}))
        except Exception as e:
            messages.error(request,"Something Went Wrong {}".format(e))
            return HttpResponseRedirect(reverse('edit_politician',kwargs={'id':politician_id}))
def delete_user_comment(request,id,poli_id):
    Comment.objects.get(id = id).delete()
    messages.success(request,"Comment Deleted")
    return HttpResponseRedirect(reverse('about_politician', kwargs={"id":poli_id}))
def politician_image_video(request,poli_id):
    politician = Politician.objects.get(id=poli_id)
    poli_img_slider = Politician_image_slider.objects.filter(politician=poli_id)
    img_slider_count=Politician_image_slider.objects.filter(politician=poli_id).count()
    poli_video_slider = Politician_video_slider.objects.filter(politician=poli_id)
    video_slider_count=Politician_video_slider.objects.filter(politician=poli_id).count()
    context ={'politician':politician,'poli_img_slider':poli_img_slider,
    "img_slider_count":img_slider_count,'poli_video_slider':poli_video_slider,
    "video_slider_count":video_slider_count}
    return render(request,'admin_template/politician_image_video.html',context)
def upload_image_slider(request):
    politician_id =request.POST.get('poli_id')
    image_slider = request.FILES.getlist('image_slider')
    if len(image_slider) >0:
        try:
            politician = Politician.objects.get(id = politician_id)
            no_img = Politician_image_slider.objects.filter(politician=politician_id).count()
            if no_img + len(image_slider)<7:
                for img in image_slider:
                    politician_img_slider = Politician_image_slider(politician=politician,image = img)
                    politician_img_slider.save()
                messages.success(request,"Image Upload Successfully")
                return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
            else:
                messages.error(request,"Already {} Exists ! Choose {} Image Only . Upload Images Limit 6".format(no_img ,6-(no_img)))
                return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
            
        except:
            messages.error(request," Failed To Upload Slider Image")
            return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
    else:
        messages.error(request,"Please Choose Atleast One Image")
        return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
def delete_image_slider(request,id,poli_id):
    try:
        img = Politician_image_slider.objects.get(id = id).image
        path = os.path.join(settings.MEDIA_ROOT,str(img))
        if os.path.exists(path):
            os.remove(path)
        Politician_image_slider.objects.get(id = id).delete()
        messages.success(request,"Image Upload Successfully")
        return HttpResponseRedirect(reverse("politician_image_video",kwargs={'poli_id':poli_id}))
    except:
        messages.error(request,"Failed To Delete Image")
        return HttpResponseRedirect(reverse("politician_image_video",kwargs={'poli_id':poli_id}))

def upload_video_slider(request):
    politician_id =request.POST.get('poli_id')
    video_slider = request.POST.getlist('video_slider')
    if len(video_slider) >0:
        try:
            politician = Politician.objects.get(id = politician_id)
            no_video = Politician_video_slider.objects.filter(politician=politician_id).count()
            if no_video + len(video_slider)<7:
                for video in video_slider:
                    politician_video_slider = Politician_video_slider(politician=politician,video = video)
                    politician_video_slider.save()
                messages.success(request,"Video  Upload Successfully")
                return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
            else:
                messages.error(request,"Already {} Exists ! Choose {} Video Only . Upload Videos Limit 6".format(no_video ,6-(no_video)))
                return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
                
        except:
            messages.error(request," Failed To Upload Slider Video")
            return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
    else:
        messages.error(request,"Please Choose Atleast One Video")
        return HttpResponseRedirect(reverse('politician_image_video',kwargs={'poli_id':politician_id}))
def delete_video_slider(request,id,poli_id):
    try:
        # video = Politician_video_slider.objects.get(id = id).video
        # video.close()
        # os.remove(os.path.join(settings.MEDIA_ROOT,str(video)))
        Politician_video_slider.objects.get(id = id).delete()
        messages.success(request,"Delete Video Sucssfully")
        return HttpResponseRedirect(reverse("politician_image_video",kwargs={'poli_id':poli_id}))
    except Exception as e:
        print(e)
        messages.error(request,"Failed To Delete Video ")
        return HttpResponseRedirect(reverse("politician_image_video",kwargs={'poli_id':poli_id}))


#advertisement slider 
def advertise_image_slider(request):
    adv_img_count=Advertise.objects.all().count()
    adv_img=Advertise.objects.all()
    return render(request,'admin_template/adv_slider.html',{"adv_img_count":adv_img_count,"adv_img":adv_img})
def delete_advertise_image_slider(request, id):
    try:
        adv = Advertise.objects.get(id=id).image
        path = os.path.join(settings.MEDIA_ROOT, str(adv))
        if os.path.exists(path):
            os.remove(path)
        Advertise.objects.get(id=id).delete()
        messages.success(request, "Delete Video Sucssfully")
        return HttpResponseRedirect(reverse("advertise_image_slider"))
    except Exception as e:
        messages.error(request, "Failed To Delete Video")
        return HttpResponseRedirect(reverse("advertise_image_slider"))
def save_advertise_image_slider(request):
    adv_img = request.FILES.getlist('adv_img')
    if len(adv_img) >0:
        try:
            for img in adv_img:
                adv_img_slider = Advertise(image = img)
                adv_img_slider.save()
            messages.success(request," Advertise Slider Image Upload Successfully")
            return HttpResponseRedirect(reverse('advertise_image_slider'))
        except Exception as e:
            messages.error(request," Failed To Upload Advertise Slider Image")
            return HttpResponseRedirect(reverse('advertise_image_slider'))
    else:
        messages.error(request,"Please Choose Atleast One Image")
        return HttpResponseRedirect(reverse('advertise_image_slider'))
# admin profile
def admin_profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    return render(request,"admin_template/profile.html",{"user":user})
def admin_change_email(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    u_id = request.user.id
    name = request.POST.get("name")
    email = request.POST.get("change_email")
    try:
        customuser = CustomUser.objects.get(id=u_id)
        customuser.name = name
        customuser.email = email
        customuser.save()
        messages.success(request, "Changes Applied Successfully")
        return HttpResponseRedirect(reverse("admin_profile"))
    except Exception as e:
        messages.error(request, "Failed To Change Mobile")
        return HttpResponseRedirect(reverse("admin_profile"))

def admin_change_password(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    new_c_password = request.POST.get("new_c_password")
    u_id = request.user.id
    if old_password != '' and new_c_password != '':
        try:
            if new_password == new_c_password:
                UserModel = get_user_model()
                user = UserModel.objects.get(id=u_id)
                if user.check_password(old_password):
                    customuser = CustomUser.objects.get(id=u_id)
                    customuser.set_password(new_password)
                    customuser.save()
                    return HttpResponseRedirect(reverse("admin_logout"))
                else:
                    messages.error(request, "Current Password Is Wrong")
                    return HttpResponseRedirect(reverse("admin_profile"))
            else:
                messages.error(request, "Confirm Password Is Not Matched")
                return HttpResponseRedirect(reverse("admin_profile"))
        except Exception as e:
            messages.error(request, "Failed To Change Password ")
            return HttpResponseRedirect(reverse("admin_profile"))
    else:
        messages.error(request, "Please Fill All The Filed")
        return HttpResponseRedirect(reverse("admin_profile"))


from django.core.mail import send_mail,send_mass_mail,EmailMessage
from django.conf import settings
def send_mail_test(request):
    email_from=settings.EMAIL_HOST_USER
    email_to = ["prashan2299@gmail.com",]
    message = "Your One Time Password (OTP) is 8898866" 
    subject="Amaneta Email Verification OTP"
    msg = EmailMessage(
        subject,
        message,
        email_from,
        email_to,
    )
    msg.send()
    print("############# mail send ")
    return HttpResponse("mail send")