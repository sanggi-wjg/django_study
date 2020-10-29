import pytest

from sample import settings


@pytest.fixture(scope = 'session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'backend',
        'USER'    : 'root',
        'HOST'    : '127.0.0.1',
        'PASSWORD': 'wpdlwl',
        'PORT'    : '33061',
    }
