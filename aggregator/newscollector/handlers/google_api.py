import requests
import json
import re

from django.core.serializers.json import DjangoJSONEncoder


API_KEY = '097449aeb12a4fb18f4137a93684ee62'


#
# Public functions
#

def get_articles(page, pageSize, filters=[]):
    query = construct_query(filters)
    url = construct_url(page, pageSize, query)
    data = ask_for(url)
    source = get_source()

    result = [to_article_dict(item, source) for item in data]

    return result


#
# Helpers
#

def construct_url(page, pageSize, query):
    return make_url(
        endpoint='everything',
        q=query,
        language='ru',
        page=str(page),
        pageSize=str(pageSize),
        sortBy='relevancy',
    )


def construct_query(filters):
    query = ' OR '.join(filters)
    tags = ''
    if query:
        tags = '(' + query + ') AND '

    return tags + '(business OR финанс OR бизнес OR Сбербанк)'


def to_article_dict(data, source):
    import dateparser
    date = dateparser.parse(data['publishedAt'])

    return {
        'title': data['title'] or '',
        'content': '',
        'content_short': data['description'] or '',
        'thumbnail': data['urlToImage'] or '',
        'link': data['url'],
        'date': date,
        'source': source,
    }


def get_source():
    from newscollector.models import NewsSource
    return NewsSource.objects.get(source_type='google-news')


#
# General purpose
#

def make_url(endpoint='everything', **params):
    result = endpoint + '?'
    for param in params:
        result += param + '=' + params[param] + '&'
    result = get_url_base(result)
    return result


def get_url_base(params):
    return 'https://newsapi.org/v2/' + params + 'apiKey=' + API_KEY


def ask_for(url):
    print('Making News Api Request: ', url)
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    articles = data['articles']
    for article in articles:
        article['description'] = clean_html(article['description'])
    return articles


cleanr = re.compile('<.*?>')


def clean_html(raw_html):
    return re.sub(cleanr, '', raw_html)

#
# Deprecated
#


google_news_image = 'https://www.androidpolice.com/wp-content/uploads/2018/05/google-news-hero.png'


def format_article_d(article):
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


def format_articles_d(articles):
    result = []
    for article in articles:
        result.append(format_article_d(article))
    return json.dumps(result, ensure_ascii=False, cls=DjangoJSONEncoder)


def every_d(page, pageSize, filters=[]):
    query = ' OR '.join(filters)
    tags = ''
    if query:
        tags = '(' + query + ') AND '

    url = make_url(
        endpoint='everything',
        q=tags + '(business OR финанс OR бизнес OR Сбербанк)',
        language='ru',
        page=str(page),
        pageSize=str(pageSize),
        sortBy='relevancy',
    )
    articles = ask_for(url)
    result = format_articles_d(articles)
    return result


def all_d():
    url = make_url(
        endpoint='everything',
        q='(business OR финансы OR бизнес)',
        language='ru',
        sortBy='date',
    )
    articles = ask_for(url)
    result = format_articles_d(articles)
    return result
