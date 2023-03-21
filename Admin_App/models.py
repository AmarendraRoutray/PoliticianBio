import profile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid ,random
from .ModelManager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    user_type_data=((1,"Admin"),(2,"Editor"),(3,"User"))
    user_type=models.CharField(default=3,choices=user_type_data,max_length=10)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=225)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    profile = models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while CustomUser.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(CustomUser,self).save()

class State(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    name = models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while State.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(State,self).save()
    def state_id(self):
        return self.id.__str__()
class District(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while District.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(District,self).save()
class Constitution(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Constitution.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Constitution,self).save()
class Desingnation(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    constitution = models.ForeignKey(Constitution, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Desingnation.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Desingnation,self).save()

class Politician(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    constitution = models.ForeignKey(Constitution, on_delete=models.CASCADE)
    desingnation = models.ForeignKey(Desingnation, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    desc = models.TextField()
    meta_desc = models.TextField(blank=True)
    meta_keyword = models.TextField(blank=True)
    desc = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(CustomUser, related_name='dislikes', blank=True)
    profile = models.ImageField(upload_to='politician_profile/')
    party_logo = models.ImageField(upload_to='party_logo/', blank= True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Politician.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Politician,self).save()
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()

class Politician_image_slider(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='politician_imgage_slider/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Politician_image_slider.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Politician_image_slider,self).save()
class Politician_video_slider(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    video = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Politician_video_slider.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Politician_video_slider,self).save()

class Comment(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.FileField(upload_to='comment_image/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Comment.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Comment,self).save()
class Advertise(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    image = models.FileField(upload_to='advertise_slider/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Advertise.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Advertise,self).save()
class Otp(models.Model):
    id=models.CharField(editable=False,primary_key=True,max_length=225)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def save(self ,*args ,**kwargs):
        if not self.id:
            self.id = random.randint(1000000000,9999999999)
            while Otp.objects.filter(id=self.id).exists():
                self.id = random.randint(1000000000,9999999999)
        super(Otp,self).save()