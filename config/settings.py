import os
import platform               ##? Detect OS
from pathlib import Path 
from django.utils.translation import gettext_lazy as _

from config.env import BASE_DIR, env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(os.path.join(BASE_DIR, '.env'))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)
LIVE  = env.bool('LIVE', default=False)


##! Allow Hosts
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS',
    # default = [] ## ⚠️ Only for development!
    default=['localhost', '127.0.0.1', '0.0.0.0']
)



##! CORS Headers Allowd
## Allow All Origins (Not Recommended for Production)
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=False) ## ⚠️ Only for development! (True)

if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
        "http://localhost:3000", ## React/Vue development server
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
    ])



##! CSRF Trusted Origins     
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    # default=[] ## ⚠️ Only for development!
    default=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]
)

##! CORS Additional Settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET','POST','PUT','PATCH','DELETE','OPTIONS',]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

##! Application definition

##? For Custom Apps Creat (apps/my_apps )
CUSTOM_APPS = [
    'core.apps.CoreConfig',                ## core
    'users.apps.UsersConfig',              ## users
    'apps.company.apps.CompanyConfig',     ## company
    'apps.supplier.apps.SupplierConfig',    ## supplier
    'apps.product.apps.ProductConfig',     ## product
    'apps.purchase.apps.PurchaseConfig',   ## purchase
    'apps.stock.apps.StockConfig',         ## stock
    'apps.sales.apps.SalesConfig',         ## sales
    'apps.order.apps.OrderConfig',         ## order
]


##? For Third Party Apps
THIRD_PARTY_APPS = [
    'django_cleanup.apps.CleanupConfig',   ## Django Cleanup
    'mptt',                                ## MPTT [ Recursive Tree ]
]

## Only add tailwind and theme if they exist
try:
    import tailwind
    THIRD_PARTY_APPS.insert(0, 'tailwind')
    THIRD_PARTY_APPS.insert(0, 'theme')
except ImportError:
    print("Tailwind not installed, skipping...")


##? Deffault Apps + Django Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'django_filters',
    
] + THIRD_PARTY_APPS + CUSTOM_APPS 


##! Tailwind CSS & Theme
TAILWIND_APP_NAME = 'theme'
# NPM_BIN_PATH = 'npm.cmd'

if platform.system() == "Windows":
    NPM_BIN_PATH = "npm.cmd"
else:
    ##* Linux/Mac (check with `which npm` in server)
    # NPM_BIN_PATH = "/usr/bin/npm"
    NPM_BIN_PATH = "/home/rakib1515hassan/.nvm/versions/node/v24.12.0/bin/npm"
    
if not LIVE:
    ##* Add django_browser_reload only in DEBUG mode
    INSTALLED_APPS += ['django_browser_reload']


##! Middleware Setup
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',                    ##? CROS Header Middleware
    "django.middleware.locale.LocaleMiddleware",                ##? Language Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if not LIVE:
    # Add django_browser_reload middleware only in DEBUG mode
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware", ##? For Tailwind CSS
    ]


##! Custom User Model
AUTH_USER_MODEL = 'users.User'
swappable = 'AUTH_USER_MODEL'


##! URL Config
ROOT_URLCONF = 'config.urls'



##! Template Config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
                
                ## Apps Template Setup
                os.path.join(BASE_DIR, 'apps/components/templates'),
                os.path.join(BASE_DIR, 'apps/auth/templates'),
                os.path.join(BASE_DIR, 'apps/roles/templates'),
                os.path.join(BASE_DIR, 'apps/dashboard/templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
 
                ##? Custom Context Processor -----------------------------
                'core.context_processors.debug.debug',  
                'core.context_processors.sidebar_color.sidebar_color',  
                'core.context_processors.jwt_token.jwt_access_token', 
                'core.context_processors.user_groups.user_groups_processor', 
                ##?-------------------------------------------------------
                
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'

LOGIN_URL = 'auth:login'

##! Database Setup
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Try to read PostgreSQL config, fallback to None
DB_NAME     = env('DB_NAME', default=None)
DB_USER     = env('DB_USER', default=None)
DB_PASSWORD = env('DB_PASSWORD', default=None)
DB_HOST     = env('DB_HOST', default=None)
DB_PORT     = env('DB_PORT', default=None)

if all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
    DATABASES = {
        "default": {
            "ENGINE"   : "django.db.backends.postgresql",
            "NAME"     : DB_NAME,
            "USER"     : DB_USER,
            "PASSWORD" : DB_PASSWORD,
            "HOST"     : DB_HOST,
            "PORT"     : DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE' : 'django.db.backends.sqlite3',
            'NAME'   : os.path.join(BASE_DIR, 'db.sqlite3'),
            'OPTIONS': {
                'timeout': 20,
                'check_same_thread': False,  # Multi-threading support
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


##! Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True





##! Static and Media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

##? Only add theme/static if it exists
theme_static_path = os.path.join(BASE_DIR, 'theme', 'static')
if os.path.exists(theme_static_path):
    STATICFILES_DIRS.append(theme_static_path)
    

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



##! Internationalization Configuration
LANGUAGE_CODE = 'en'  ##? Default Language

LANGUAGES = [
    ('en', _('English')),
    ('bn', _('Bangla')),
    ('hi', _('Hindi')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('de', _('German')),
    ('zh-hans', _('Simplified Chinese')),
    ('zh-hant', _('Traditional Chinese')),
    ('ko', _('Korean')),
    ('ja', _('Japanese')),
    ('ru', _('Russian')),
    ('pt', _('Portuguese')),
    ('tr', _('Turkish')),
    ('ar', _('Arabic')),
]

USE_I18N = True
USE_L10N = True

# Locale paths
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


##! Some Important Configuration
DEFAULT_USER_PASSWORD = "ChangeMe@123"
MAX_LOGIN_ATTEMPTS = 4
ACCOUNT_LOCK_MINUTES = 3

OTP_TIMEOUT = 3                          ## OTP timeout set 3 minutes
OTP_TOKEN_TIMEOUT = 10                   ## OTP Token timeout set 10 minutes
DEFAULT_PAGINATION_LIMIT = 20            ## Deffault Pagination Limit

##? Session settings for Remember Me functionality
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days in seconds (for "Remember Me")
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14    # 14 days in seconds (for "Remember Me")
SESSION_EXPIRE_AT_BROWSER_CLOSE = True    # Session expires when browser closes
SESSION_SAVE_EVERY_REQUEST = False        # Don't update session on every request

# Security settings for sessions
SESSION_COOKIE_SECURE   = False           # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# If you're using Django's built-in authentication
LOGIN_URL           = 'auth:login'       # Your login URL name
LOGIN_REDIRECT_URL  = 'dashboard:home'   # Redirect after login
LOGOUT_REDIRECT_URL = 'auth:login'       # Redirect after logout


##! ================= Package ===================================
from config.packege.drf import *
from config.packege.jwt import *



##! ================= Service ===================================
# from service.email import *
