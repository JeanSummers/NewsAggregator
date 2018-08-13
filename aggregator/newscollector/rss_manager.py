from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


import json
import datetime
import feedparser
import dateparser

from feedparser import FeedParserDict


# No globals and forward declarations
def sources(name):
    '''
    Returns source object or None
    '''
    source = {
        'nasa': {
            'image': '',
            'link': 'https://www.nasa.gov/rss/dyn/Gravity-Assist.rss',
            'handler': Nasa_parser,
        },
        'times_sport': {
            'image': 'https://pmcvariety.files.wordpress.com/2013/08/t_logo_2048_black.png?w=1000&h=563&crop=1',
            'link': 'https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml',
            'handler': Times_Sport_parser,
        },
        '1prime_eco': {
            'image': 'http://www.sostav.ru/images/news/2013/12/25/384767484.jpg',
            'link': 'https://1prime.ru/export/rss2/state_regulation/index.xml',
            'handler': generic_handler,
        },
        '1prime_fin': {
            'image': 'http://www.sostav.ru/images/news/2013/12/25/384767484.jpg',
            'link': 'https://1prime.ru/export/rss2/finance/index.xml',
            'handler': generic_handler,
        },
        'lenta': {
            'image': 'https://icdn.lenta.ru/assets/webpack/images/04ceff52e5b673154a365683e768578e.lenta_og.png',
            'link': 'https://lenta.ru/rss/articles',
            'handler': generic_handler,
        }
    }

    if name is None:
        return [name for name in source]

    try:
        result = source[name]
    except:
        return None
    return result


# Fast way to abort parsing at any level
class ConstructionError(Exception):
    pass


NO_DEFAULT = ConstructionError()


#
# Handlers
#

def generic_handler(data: FeedParserDict, source):
    feed = attr(data, 'feed')
    items = attr(data, 'entries')
    if not isinstance(items, list):
        raise ConstructionError()

    news = []
    for item in items:
        result = get_generic_item(item, source)
        news.append(result)

    return news


def get_generic_item(item, source):
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
        'thumbnail': source['image'],
        'origin_link': source['link'],
        'link': field(item, 'link', ''),
        'date': parsed_date,
    }


def Times_Sport_parser(data: FeedParserDict, source):
    feed = attr(data, 'feed')
    image = field(feed, 'image')
    image_link = attr(image, 'href')

    items = attr(data, 'entries')
    if not isinstance(items, list):
        return [get_Times_Sport_item(items, image_link)]

    news = []
    for item in items:
        result = get_Times_Sport_item(item, image_link)
        news.append(result)

    return news


def get_Times_Sport_item(item, def_image):
    image = field(item, 'media_content', None)
    try:
        image_link = field(image[0], 'url')
    except:
        image_link = def_image

    date = field(item, 'published', None)
    if date is None:
        parsed_date = datetime.datetime.now()
    else:
        parsed_date = dateparser.parse(date)

    content = field(item, 'content', None)
    try:
        text = field(content[0], 'value')
    except:
        text = ''

    if text == '':
        text = field(content[0], 'value')

    return {
        'title': field(item, 'title', 'Без заголовка'),
        'content': '',
        'content_short': text,
        'thumbnail': sources('times_sport')['image'],
        'origin_link': sources('times_sport')['link'],
        'link': field(item, 'link', ''),
        'date': parsed_date,
    }


def Nasa_parser(data: FeedParserDict, source):
    feed = attr(data, 'feed')
    image = field(feed, 'image')
    image_link = attr(image, 'href')

    items = attr(data, 'entries')
    if not isinstance(items, list):
        return [get_Nasa_item(items, image_link)]

    news = []
    for item in items:
        result = get_Nasa_item(item, image_link)
        news.append(result)

    return news


def get_Nasa_item(item, def_image):
    date = field(item, 'published', None)
    if date is None:
        parsed_date = datetime.datetime.now()
    else:
        parsed_date = dateparser.parse(date)
    return {
        'title': field(item, 'title', 'Без заголовка'),
        'content': '',
        'content_short': field(item, 'summary', 'Без краткого содержания'),
        'thumbnail': def_image,
        'origin_link': sources('nasa')['link'],
        'link': field(item, 'link', ''),
        'date': parsed_date,
    }


#
# Handle router
#

def from_sources(*source_names):
    '''
    Collects data by appropriate handlers
    or returns empty array
    '''
    array = source_names
    if not source_names:
        array = sources(None)
    print(array)

    result = []
    for name in array:
        data = from_source(name)
        result.extend(data)
        print('Processed ', name)

    return result


def from_source(source_name):
    '''
    Collects data by appropriate handler
    or returns empty array
    '''
    source = sources(source_name)
    if source is None:
        return []

    link = source['link']
    feed = feedparser.parse(link)

    handler = source['handler']
    try:
        result = handler(feed, source)
    except ConstructionError:
        return []

    return result


#
# Convenient getters
#


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
