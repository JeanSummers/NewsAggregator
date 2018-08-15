from django.conf.urls import url
from .views import default, news_all, news_range, single_article, update_database, test, news_filtered_range

from .views import news_every, news_tagged

urlpatterns = [
    url('^$', default, name='default'),
    url('^test/+$', test, name='test'),
    url('^save/+$', update_database, name='update_database'),

    url('^all/(?P<start>\d+)-(?P<end>\d+)/+$',
        news_every, name='every_news'),
    url('^all/+$', news_all, name='news_all'),
    url('^tagged/(?P<start>\d+)-(?P<end>\d+)/(?P<coded_tags>[\d\S]+)/+$',
        news_tagged, name='tagged_nes'),

    url('^(?P<start>\d+)-(?P<end>\d+)/(?P<data>[\d\S]+)/+$',
        news_filtered_range, name='news_filtered_range'),
    url('^(?P<start>\d+)-(?P<end>\d+)/+$', news_range, name='news_range'),
    url('^(?P<number>\d+)/+$', single_article, name='single_article'),
]
