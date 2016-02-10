# -*- coding: utf-8 -*-

#DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('MFL-analyzer admin', 'mail@vitaly-bogomolov.ru'),
)

MANAGERS = ADMINS
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    'tpl',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
)

appspot_id = 'mfl-pipetechnology'
