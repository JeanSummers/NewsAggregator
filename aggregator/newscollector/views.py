'''
Handlers for http-requests
'''

from django.http import HttpResponse

from .serializers import articles_to_news_json, article_to_news_json
import newscollector.base_manager as base

import base64
import json

import newscollector.handlers.google_api as api


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
    import newscollector.common as common
    common.update_database()
    return HttpResponse('Database updated!')


def news_filtered_range(request, start, end, data):
    decoded = base64.b64decode(data).decode("utf-8")
    strings = json.loads(decoded)
    articles = base.get_filtered_range(start, end, strings)
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


def test(request):
    return HttpResponse(api.all(), content_type='application/json', charset='utf-8')


def news_every(request, start, end):
    pageSize = int(end) - int(start)
    page = int(end) // pageSize
    result = api.every(page, pageSize)
    return HttpResponse(result)


def news_tagged(request, start, end, coded_tags):
    decoded_tags = base64.b64decode(coded_tags).decode("utf-8")
    tags = json.loads(decoded_tags)
    pageSize = int(end) - int(start)
    page = int(end) // pageSize
    result = api.every(page, pageSize, tags)
    return HttpResponse(result)
