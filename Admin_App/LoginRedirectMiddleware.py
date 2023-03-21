from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRedirectMiddleware(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__       
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "Admin_App.admin_views" or modulename == "django.views.static" :
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_dashboard"))
            elif user.user_type == "3":
                if modulename == "User_App.user_views" or modulename == "django.views.static" :
                    pass
                else:
                    return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponseRedirect(reverse("admin_login"))

        else:
            if modulename == "User_App.user_views" or modulename == "Auth_App.auth_views" or  modulename == "django.contrib.auth.views"  or  modulename == "allauth.account.views" or  modulename == "allauth.socialaccount.views" or  modulename == "allauth.socialaccount.providers.oauth2.views"or  modulename == "allauth.socialaccount.providers.oauth.views"  or modulename == "django.views.static" :
                pass
            else:
                print(modulename)
                return HttpResponseRedirect(reverse("home"))