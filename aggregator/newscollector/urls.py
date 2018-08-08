from django.conf.urls import url
from .views import default, news_all, news_range, single_article, update_database

urlpatterns = [
    url('^$', default, name='default'),
    url('^all/+$', news_all, name='news_all'),
    url('^save/+$', update_database, name='update_database'),
    url('^(?P<start>\d+)-(?P<end>\d+)/+$', news_range, name='news_range'),
    url('^(?P<number>\d+)/+$', single_article, name='single_article'),
]
