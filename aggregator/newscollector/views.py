'''
Handlers for http-requests
'''

from django.http import HttpResponse

from .serializers import articles_to_news_json, article_to_news_json
import newscollector.base_manager as base

import base64
import json

import newscollector.handlers.google_api as api


#
# Save all sources to database
#

def update_database(request):
    import newscollector.common as common
    common.update_database()
    return HttpResponse('Database updated!')


#
# All feed with paging
#

def news_all(request, page):
    return news_all_pagesize(request, page, 10)


def news_all_pagesize(request, page, pageSize):
    articles = base.get_range(
        (int(page) - 1) * int(pageSize),
        int(page) * int(pageSize))
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


#
# Search news with paging
#

def news_search(request, tags, page):
    return news_search_pagesize(request, tags, page, 10)


def news_search_pagesize(request, tags, page, pageSize):
    tag_list = tags_to_list(tags)
    dynamic = api.get_articles(1, 100, tag_list)
    base.save_list(dynamic)
    articles = base.get_filtered_range(
        (int(page) - 1) * int(pageSize),
        int(page) * int(pageSize),
        tag_list)
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


#
# Weekly news about clients and companies
#

def news_relevant(request, tags):
    tag_list = tags_to_list(tags)
    dynamic = api.get_articles(1, 100, tag_list)
    base.save_list(dynamic)
    articles = base.get_filtered_range(0, 100, tag_list)
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


def construct_html(data):
    result = ''
    for item in data:
        result += '<h2>' + item.title + '</h2><br>'
        result += '<img src="' + \
            (item.thumbnail or item.source.image) + '" height="100">'
        result += '<p>' + item.content_short + '</p>'
        result += '<p>' + str(item.source) + '</p>'
        result += '<a href="' + item.link + '">Ссылка</a><br>'
    return result


#
# General purpose
#

def tags_to_list(tags):
    tag_list = tags.split(sep=',')
    return [item.strip() for item in tag_list]


def test(request):
    return HttpResponse(api.all(), content_type='application/json', charset='utf-8')


#
# Deprecated
#


def default(request):
    return news_range(request, 0, 10)


def news_all_d(request):
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


def news_filtered_range(request, start, end, data):
    decoded = base64.b64decode(data).decode("utf-8")
    strings = json.loads(decoded)
    articles = base.get_filtered_range(start, end, strings)
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


def news_every(request, start, end):
    pageSize = int(end) - int(start)
    page = int(end) // pageSize
    result = api.every_d(page, pageSize)
    return HttpResponse(result)


def news_tagged(request, start, end, coded_tags):
    decoded_tags = base64.b64decode(coded_tags).decode("utf-8")
    tags = json.loads(decoded_tags)
    pageSize = int(end) - int(start)
    page = int(end) // pageSize
    result = api.every_d(page, pageSize, tags)
    return HttpResponse(result)
