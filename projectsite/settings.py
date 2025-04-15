from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'widget_tweaks',

    # Local apps
    'projectsite',
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['fireappboilerplate.pythonanywhere.com', 'localhost', '127.0.0.1']

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = '/home/fireappboilerplate/fireApp-boilerplate/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/fireappboilerplate/fireApp-boilerplate/media'