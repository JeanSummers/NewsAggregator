from django.conf.urls import url
from .views import default, news_all, news_range, single_article, update_database, test, news_filtered_range

urlpatterns = [
    url('^$', default, name='default'),
    url('^all/+$', news_all, name='news_all'),
    url('^test/+$', test, name='test'),
    url('^save/+$', update_database, name='update_database'),
    url('^(?P<start>\d+)-(?P<end>\d+)/(?P<data>[\d\S]+)/+$',
        news_filtered_range, name='news_filtered_range'),
    url('^(?P<start>\d+)-(?P<end>\d+)/+$', news_range, name='news_range'),
    url('^(?P<number>\d+)/+$', single_article, name='single_article'),
]
