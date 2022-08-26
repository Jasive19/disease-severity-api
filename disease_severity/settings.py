from pathlib import Path
import os
import django_heroku

BASE_DIR = Path(__file__).resolve().parent.parent
#SECRET_KEY = 'django-insecure-7w3p-#l02smkpog(!3a4!d^2xc&pz@_e20xwx8@67eecb%)jwn'
DEBUG = True
ALLOWED_HOSTS = []

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.users',
    'apps.analysis',
    'apps.authentication',
    'apps.severity',
]

EXTERNAL_APPS = [
    'django_heroku',
    'rest_framework',
    'rest_framework.authtoken',
    # 'django_rest_passwordreset',
    'corsheaders',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + EXTERNAL_APPS

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

ROOT_URLCONF = 'disease_severity.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'disease_severity.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd3ecj6p5uvp377',
        'USER': 'ttvvtweteprkih',
        'PASSWORD': '2728169ae34cc6f317b236cb61b38fd3a5c23db73498fb9acd511233f70d0f8b',
        'HOST': 'ec2-44-206-89-185.compute-1.amazonaws.com',
        'PORT': '5432',
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.69:3000",
    "https://disease-severity-test.netlify.app"
]

CORS_ORIGIN_WHITELIST = ["http://localhost:3000",
                         "http://127.0.0.1:3000", "http://192.168.1.69:3000", "https://disease-severity-test.netlify.app",]
CORS_ALLOW_CREDENTIALS = True

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_L10N = True
STATIC_URL = 'static/'

MODELS = os.path.join(BASE_DIR, 'model')
"import django_heroku" 
