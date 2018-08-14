'''
Handlers for http-requests
'''

from django.http import HttpResponse

from .serializers import articles_to_news_json, article_to_news_json
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
    import newscollector.tasks as tasks
    tasks.update_database()
    return HttpResponse('Database updated!')


def news_filtered_range(request, start, end, data):
    import base64
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    decoded = base64.b64decode(data).decode("utf-8")
    strings = json.loads(decoded)
    articles = base.get_filtered_range(start, end, strings)
    jstr = articles_to_news_json(articles)
    return HttpResponse(jstr)


def test(request):
    return HttpResponse('<h1>This is test page</h1>')
