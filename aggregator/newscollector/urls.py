from django.conf.urls import url
from .rss_manager import getJSON

urlpatterns = [
    url('^$', getJSON),
]
