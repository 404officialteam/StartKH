import os
import dj_database_url
from pathlib import Path

# Monkeypatch to bypass MariaDB version check for older XAMPP versions
from django.db.backends.base.base import BaseDatabaseWrapper
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# Disable RETURNING clause for older MariaDB/MySQL versions
from django.db.backends.mysql.features import DatabaseFeatures
DatabaseFeatures.can_return_columns_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-1%opyo8#8#wmcdehov%*dkxn-4_&el+o6l)dk*o%vlletf_chz')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    
    # Custom apps
    'apps.accounts',
    'apps.projects',
    'apps.comments',
    'apps.votes',
    'apps.notifications',
    'apps.categories',
    'apps.teams',
    'apps.analytics',
    'apps.search',
    'apps.dashboard',
    'apps.core',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise static files handler
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.notifications.context_processors.notifications', # custom notifications context
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# If DATABASE_URL is set in environment (Render, Railway, etc.), use it.
# Otherwise, fall back to local MySQL (XAMPP default) with fallback to SQLite.
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'startkh',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }

    try:
        import MySQLdb
        conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", port=3306)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS startkh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
    except Exception as e:
        print(f"MySQL connection failed: {e}. Falling back to SQLite3 database for development.")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Phnom_Penh' # Cambodia Timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media Files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'explore'
LOGOUT_REDIRECT_URL = 'explore'

# Email Settings (for console testing during dev)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'support@startkh.com'
