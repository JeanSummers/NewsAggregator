from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


import json
import datetime
import feedparser
from feedparser import FeedParserDict


# No globals and forward declarations
def sources(name):
    source = {
        'nasa': {
            'link': 'https://www.nasa.gov/rss/dyn/Gravity-Assist.rss',
            'handler': Nasa_parser
        }
    }

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


def Nasa_parser(data: FeedParserDict):
    feed = attr(data, 'feed')
    def_image = field(feed, 'image')
    def_image_link = attr(def_image, 'href')

    items = attr(data, 'entries')
    if not isinstance(items, list):
        return [get_Nasa_item(items, def_image_link)]

    news = []
    for item in items:
        result = get_Nasa_item(item, def_image_link)
        news.append(result)

    return news


def get_Nasa_item(item, def_image):
    import dateparser
    date = field(item, 'published', None)
    if date is None:
        parsed_date = datetime.datetime.now()
    else:
        parsed_date = dateparser.parse(date)

    return {
        'title': field(item, 'title', 'Без заголовка'),
        'content': field(item, 'summary', 'Без текста'),
        'content_short': field(item, 'summary', 'Без краткого содержания'),
        'thumbnail': def_image,
        'origin_link': sources('nasa')['link'],
        'link': field(item, 'link', ''),
        'date': str(parsed_date),
    }


#
# Handle router
#


def from_source(source_name):
    '''
    Redirects data to appropriate handler
    or returns None
    '''
    if sources(source_name) is None:
        return None

    link = sources(source_name)['link']
    feed = feedparser.parse(link)

    handler = sources(source_name)['handler']
    try:
        result = handler(feed)
    except ConstructionError:
        return None

    return result


#
# Convinient getters
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
