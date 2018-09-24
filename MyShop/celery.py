import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'Celery' Program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyShop.settings')

app = Celery('MyShop')

app.config_from_object('django.conf.settings')  # load any custom configurations from settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # Celery will look for task.py which will
#  load asynchronous task defined there

# don't forget to import celery in __init__.py file


# start celery -> celery -A MyShop worker -l info
