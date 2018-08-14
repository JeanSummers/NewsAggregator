'''
Provides parse(url) function
where url is a valid rss-feed link
'''


from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

import json
import datetime
import feedparser
import dateparser


# Fast way to abort parsing at any level
class ConstructionError(Exception):
    pass


#
# Handler
#

def parse(url):
    '''
    Returns list which may or may not
    contain items from rss-feed given in url
    '''
    try:
        return get_items(url)
    except ConstructionError:
        return []


def get_items(url):
    '''
    Get items from feed or raise ConstructionError
    '''
    data = feedparser.parse(url)

    feed = attr(data, 'feed')
    items = attr(data, 'entries')

    if not isinstance(items, list):
        raise ConstructionError()

    news = []
    for item in items:
        result = get_item(item)
        news.append(result)

    return news


def get_item(item):
    '''
    Get item from item list or raise ConstructionError
    '''
    import pytz

    date = field(item, 'published', None)
    if date is None:
        parsed_date = pytz.UTC.localize(datetime.datetime.now())
    else:
        parsed_date = dateparser.parse(date)

    text = field(item, 'content', None)
    try:
        text = field(content[0], 'value')
    except:
        text = ''

    if not text:
        text = field(item, 'summary', '')
    if not text:
        text = field(item, 'description', '')

    return {
        'title': field(item, 'title', 'Без заголовка'),
        'content': '',
        'content_short': text,
        'thumbnail': '',
        'link': field(item, 'link', ''),
        'date': parsed_date,
    }


#
# Convenient getters
#

NO_DEFAULT = ConstructionError()


def field(dictionary, field, default=NO_DEFAULT):
    '''
    Get dictionary field or raise construction error
    if no default provided
    '''
    if field in dictionary and dictionary[field] is not None:
        return dictionary[field]
    return check_default(default)


def attr(obj, attribute, default=NO_DEFAULT):
    '''
    Get object attribute or raise construction error
    if no default provided
    '''
    if hasattr(obj, attribute) and getattr(obj, attribute) is not None:
        return getattr(obj, attribute)
    return check_default(default)


def check_default(value):
    global NO_DEFAULT
    if value == NO_DEFAULT:
        raise NO_DEFAULT
    return value
