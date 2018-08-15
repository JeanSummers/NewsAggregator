import requests
import json
import re

from django.core.serializers.json import DjangoJSONEncoder


urls = {
    'top-ru': 'top-headlines?country=ru&',
    'all-ru': 'everything?language=ru&page=1&&pageSize=10',
}


def getUrlBase(params):
    return 'https://newsapi.org/v2/' + params + 'apiKey=097449aeb12a4fb18f4137a93684ee62'


def makeUrl(endpoint='everything', **params):
    result = endpoint + '?'
    for param in params:
        result += param + '=' + params[param] + '&'
    result = getUrlBase(result)
    print(result)
    return result


cleanr = re.compile('<.*?>')


def cleanhtml(raw_html):
    return re.sub(cleanr, '', raw_html)


def ask_for(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    articles = data['articles']
    for article in articles:
        article['description'] = cleanhtml(article['description'])
    return articles


google_news_image = 'https://www.androidpolice.com/wp-content/uploads/2018/05/google-news-hero.png'


def format_article(article):
    import dateparser
    date = dateparser.parse(article['publishedAt'])

    result = {
        'id': 'google',
        'heading': article['title'],
        'thumbnail': article['urlToImage'] or google_news_image,
        'description': article['description'],
        'text': '',
        'link': article['url'],
        'date': date,
        'views_count': 0,
        'likes_count': 0,
        'dislikes_count': 0,
    }
    return result


def format_articles(articles):
    result = []
    for article in articles:
        result.append(format_article(article))
    return json.dumps(result, ensure_ascii=False, cls=DjangoJSONEncoder)


def every(page, pageSize, filters=[]):
    tags = ''
    for tag in filters:
        tags += tag + ' AND '

    url = makeUrl(
        endpoint='everything',
        q=tags + '(business OR финансы OR бизнес)',
        language='ru',
        page=str(page),
        pageSize=str(pageSize),
        sortBy='relevancy',
    )
    articles = ask_for(url)
    result = format_articles(articles)
    return result


def all():
    url = makeUrl(
        endpoint='everything',
        q='(business OR финансы OR бизнес)',
        language='ru',
        sortBy='date',
    )
    articles = ask_for(url)
    result = format_articles(articles)
    return result
