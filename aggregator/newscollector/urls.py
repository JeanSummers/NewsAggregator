from django.conf.urls import url

# Url handlers
from .views import default, test, update_database
from .views import news_all, news_all_pagesize
from .views import news_search, news_search_pagesize
from .views import news_relevant


# Deprecated start
from .views import news_all_d, news_range, single_article, news_filtered_range
from .views import news_every, news_tagged
# Deprecated end


urlpatterns = [
    url('^test/+$', test, name='test'),

    # Save all sources to database
    url('^save/+$', update_database, name='update_database'),

    # All feed with paging
    url('^all/page=(?P<page>\d+)/+$',
        news_all, name='all_news'),
    url('^all/page=(?P<page>\d+)/pageSize=(?P<pageSize>\d+)/+$',
        news_all_pagesize, name='all_news_pagesize'),

    # Search news with paging
    url('^search/(?P<tags>[^/]+)/page=(?P<page>\d+)/+$',
        news_search, name='search_news'),
    url('^search/(?P<tags>[^/]+)/page=(?P<page>\d+)/pageSize=(?P<pageSize>\d+)/+$',
        news_search_pagesize, name='search_news_pagesize'),

    # Weekly news about clients and companies
    url('^relevant/(?P<tags>[^/]+)+$',
        news_relevant, name='relevant_news'),


    # Deprecated
    # Maybe already unused
    # here only for compability
    url('^$', default, name='default'),
    url('^all/(?P<start>\d+)-(?P<end>\d+)/+$',
        news_every, name='every_news'),
    url('^all/+$', news_all_d, name='news_all'),
    url('^tagged/(?P<start>\d+)-(?P<end>\d+)/(?P<coded_tags>[\d\S]+)/+$',
        news_tagged, name='tagged_nes'),
    url('^(?P<start>\d+)-(?P<end>\d+)/(?P<data>[\d\S]+)/+$',
        news_filtered_range, name='news_filtered_range'),
    url('^(?P<start>\d+)-(?P<end>\d+)/+$', news_range, name='news_range'),
    url('^(?P<number>\d+)/+$', single_article, name='single_article'),
]
