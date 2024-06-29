from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
)


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


INSTALLED_APPS = [
    "jazzmin",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users_app",
    "reports_app",
    "statistics_app",
    "appointments_app",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "main_app.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = ["http://localhost:4200", "https://unisafeudsm.nucci.live"]

# CORS_ALLOW_ALL_ORIGINS = True

WSGI_APPLICATION = "main_app.wsgi.application"


# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Dar_es_Salaam"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_PERMISSION_CLASSES": (
    #     "rest_framework.permissions.IsAuthenticated",
    # ),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=50),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # "USER_ID_FIELD": "id",
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


AUTH_USER_MODEL = "users_app.User"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "unisafe.reports@gmail.com"
EMAIL_HOST_PASSWORD = "paxg ssje brxd zepl"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "UniSafe"


JAZZMIN_SETTINGS = {
    "site_title": "UniSafe | Admin Dashboard",
    "site_header": "UniSafe",
    "site_brand": "UniSafe",
    "site_logo": "logo.png",
    "welcome_sign": "Welcome to UniSafe",
    "site_icon": "favicon.ico",
    "show_ui_builder": True,
    # "copyright": "UniSafe © 2024. All rights reserved"
}

JAZZMIN_UI_TWEAKS = {
    "theme": "sandstone",
    # "theme": "materia",
    # "theme": "simplex",
}


MEDIA_URL = "assets/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets")

CELERY_BEAT_SCHEDULE = {
    'mark-missed-appointments-every-hour': {
        'task': 'appointment_app.tasks.mark_missed_appointments',
        'schedule': 3600,  # Run every hour
    },
}

# CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'



