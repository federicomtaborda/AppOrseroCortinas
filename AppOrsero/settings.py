"""
Django settings for AppOrsero project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os

from pathlib import Path

from django.template.context_processors import media
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-il$-x@!246l94h8o9sy(a1u%pxe@1xhv$)2fg(=rkz!@jzp&$k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

BASE_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'cliente',
    'tipocortina',
    'ordendetrabajo',
    'mercaderia',
    'propietario',
    'configuracion'
]

UNFOLD_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history"
]

DJANGO_ADMIN = [
    "django.contrib.admin",
]

INSTALLED_APPS = UNFOLD_APPS + BASE_APPS + DJANGO_ADMIN

UNFOLD = {
    "SITE_TITLE": 'ORSERO CORTINAS',
    "SITE_HEADER": 'ORSERO CORTINAS',
    "SITE_SUBHEADER": "Administracion",
    "SITE_URL": "/",
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "255 231 255",
            "100": "226 210 254",
            "200": "188 180 252",
            "300": "147 140 248",
            "400": "113 102 241",
            "500": "76 73 209",
            "600": "63 65 171",
            "700": "49 56 130",
            "800": "34 45 94",
            "900": "26 37 71",
            "950": "17 26 50"
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "es": "🇪🇸",
            },
        },
    },
    "THEME": "light",
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Autenticación y Autorización",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Grupos"),
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Usuarios"),
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
            {
                "title": "Propietario",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Propietario"),
                        "link": reverse_lazy("admin:propietario_propietario_changelist"),
                    },
                ],
            },
            # {
            #     "title": "Administración",
            #     "separator": True,
            #     "collapsible": True,
            #     "items": [
            #         {
            #             "title": _("Entradas de registros"),
            #             "link": reverse_lazy("admin:admin_logentry_changelist"),
            #         },
            #     ],
            # },
            {
                "title": "Clientes",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Clientes"),
                        "link": reverse_lazy("admin:cliente_cliente_changelist"),
                    },
                ],
            },
            {
                "title": "Colocador",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Colocadores"),
                        "link": reverse_lazy("admin:cliente_colocador_changelist"),
                    },
                ],
            },
            {
                "title": "Cortinas",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Crear Cortina"),
                        "link": reverse_lazy("admin:tipocortina_cortina_changelist"),
                    },
                    {
                        "title": _("Modelos"),
                        "link": reverse_lazy("admin:tipocortina_modelo_changelist"),
                    },
                    {
                        "title": _("Agregar Cortina"),
                        "link": reverse_lazy("admin:tipocortina_tipocortina_changelist"),
                    },
                ],
            },
            {
                "title": "Ordenes de Trabajo",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Nueva Orden"),
                        "link": reverse_lazy("admin:ordendetrabajo_ordentrabajo_changelist"),
                    },
                ],
            },
            {
                "title": "Mercaderia",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Ingresar Meracderia"),
                        "link": reverse_lazy("admin:mercaderia_mercaderia_changelist"),
                    },
                ],
            },
        ],
    },
    # "TABS": [
    #     {
    #         "models": ["venta.venta"],
    #         "items": [
    #             {
    #                 "title": _("Reportes"),
    #                 "icon": "person",
    #                 "link": reverse_lazy("admin:reporte_ventas"),
    #             },
    #             {
    #                 "title": _("Nota de Débito/Crédito"),
    #                 "icon": "person",
    #                 "link": reverse_lazy("admin:nota-credito-debito"),
    #             },
    #         ],
    #     },
    #     {
    #         "models": ["venta.compra"],
    #         "items": [
    #             {
    #                 "title": _("Nota de Crédito"),
    #                 "icon": "person",
    #                 "link": reverse_lazy("admin:nota_compra"),
    #             },
    #         ]
    #     }
    # ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AppOrsero.urls'

LOGOUT_REDIRECT_URL = '/admin/login/'

LOGIN_URL = "admin:login"

LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'AppOrsero', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

            ],
        },
    },
]

WSGI_APPLICATION = 'AppOrsero.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app-orsero',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = "d/m/Y"
DATE_INPUT_FORMATS = ["%d/%m/%Y", ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
