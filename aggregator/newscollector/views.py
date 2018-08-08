'''
Handlers for http-requests
'''

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .serializers import articles_to_news_json, article_to_news_json
import newscollector.rss_manager as rss
import newscollector.base_manager as base


def default(request):
    return news_range(request, 0, 10)


def news_all(request):
    articles = base.get_all()
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


def single_article(request, number):
    article = base.get_single(number)
    jstr = article_to_news_json(article)
    return HttpResponse(jstr)


def news_range(request, start, end):
    articles = base.get_range(start, end)
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


def update_database(request):
    data = rss.from_source('nasa')
    base.save(data)
    return HttpResponse('Database updated!')
