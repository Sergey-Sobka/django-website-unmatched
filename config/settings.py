import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_local_env():
    env_path = BASE_DIR / '.env'

    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        os.environ.setdefault(
            key.strip(),
            value.strip().strip('"').strip("'")
        )


load_local_env()


SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-t8$#1fc5=m$_1$qo=62*8bxl(qay^*fo6c9^^f4qum!vv^gr=k'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,testserver',
).split(',')

USE_CLOUDINARY = bool(
    os.environ.get('CLOUDINARY_URL')
    or (
        os.environ.get('CLOUDINARY_CLOUD_NAME')
        and os.environ.get('CLOUDINARY_API_KEY')
        and os.environ.get('CLOUDINARY_API_SECRET')
    )
)


INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'allauth',
    'allauth.account',

    # project apps
    'apps.users',
    'apps.wiki',
    'apps.stats',
    'apps.tierlist',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

if USE_CLOUDINARY:
    CLOUDINARY_STORAGE = {
        'SECURE': True,
    }

    if not os.environ.get('CLOUDINARY_URL'):
        CLOUDINARY_STORAGE.update(
            {
                'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
                'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
                'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
            }
        )

    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS = {
    'username',
    'email',
}

ACCOUNT_SIGNUP_FIELDS = [
    'username*',
    'email*',
    'password1*',
    'password2*',
]

ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_ADAPTER = 'apps.users.adapters.AccountAdapter'

ACCOUNT_FORMS = {
    'signup': 'apps.users.forms.CustomSignupForm',
}

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'Unmatched Wiki <noreply@unmatched-wiki.local>'
