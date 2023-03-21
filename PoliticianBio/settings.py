from pathlib import Path
import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=True)
if READ_DOT_ENV_FILE:
    environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
ENVIRON = env('ENVIRON')
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# if not DEBUG:
#     if ENVIRON == "PRODUCTION":
#         ALLOWED_HOSTS = ['localhost','thenetabook.com/','www.thenetabook.com/', '165.227.103.16','https://thenetabook.com/' ,'https://www.thenetabook.com/']
#     else:
#         ALLOWED_HOSTS = ['localhost']
# else:
#     ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Admin_App',
    'User_App',
    'Auth_App',
    # 3rd party
    # "allauth", # new
    # "allauth.account", # new
    # "allauth.socialaccount", # new
    # # social providers
    # "allauth.socialaccount.providers.google", # new
    # "allauth.socialaccount.providers.facebook", # new
    # "allauth.socialaccount.providers.twitter", # new
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Admin_App.LoginRedirectMiddleware.LoginRedirectMiddleware',
]

ROOT_URLCONF = 'PoliticianBio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',


            ],
        },
    },
]

WSGI_APPLICATION = 'PoliticianBio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTH_USER_MODEL = 'Admin_App.CustomUser'
AUTHENTICATION_BACKENDS = [
    'Admin_App.AuthBackend.AuthBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 2

# Provider specific settings
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email'
#         ],
#         'APP': {
#             'client_id': env("GOOGLE_CID"),
#             'secret': env("GOOGLE_SECRET"),
#             'key': ''
#         }
#     },
#      'twitter': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'APP': {
#             'client_id': env("TWITTER_CID"),
#             'secret': env("TWITTER_SECRET"),
#             'key': ''
#         }
#     },
#     'facebook': {
#         'METHOD': 'oauth2',
#         'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
#         'SCOPE': ['email', 'public_profile'],
#         'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
#         'INIT_PARAMS': {'cookie': True},
#         'FIELDS': [
#             'id',
#             'first_name',
#             'last_name',
#             'middle_name',
#             'name',
#             'name_format',
#             'picture',
#             'short_name'
#         ],
#         'EXCHANGE_TOKEN': True,
#         'LOCALE_FUNC': 'path.to.callable',
#         'VERIFIED_EMAIL': False,
#         'VERSION': 'v13.0',
#         'APP': {
#             'client_id': env("FACEBOOK_CID"),
#             'secret': env("FACEBOOK_SECRET"),
#             'key': ''
#         }
#     }
# }
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_EMAIL_REQUIRED = False
# ACCOUNT_ADAPTER = 'User_App.social_login_adapter.MyAccountAdapter'
# SOCIALACCOUNT_ADAPTER = 'User_App.social_login_adapter.MySocialAccountAdapter'

# Internationalization

# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = "/static/"
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TSL = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_REPLY_TO = env('EMAIL_REPLY_TO')
DOMAIN = env("DOMAIN")
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
