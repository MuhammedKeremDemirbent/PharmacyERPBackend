from django.urls import include, path
from .api import urlpatterns as api_urls
from .actions import urlpatterns as action_urls

urlpatterns = api_urls + action_urls
