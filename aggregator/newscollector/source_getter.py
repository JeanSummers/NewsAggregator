from .models import NewsSource

from .handlers import rss


def all(*sources):
    '''
    Collects data by appropriate handlers
    or returns empty array

    Output list of Article-like dictionaries
    '''
    array = sources
    if not sources:
        array = list(NewsSource.objects.all())

    result = []
    for source in array:
        data = single(source)
        result.extend(data)
        if not result:
            print(source, 'Unavailable!')
        else:
            print('Processed ', source)
    return result


def single(source: NewsSource):
    '''
    Collects data by appropriate handler
    or returns empty array

    Output Article-like dictionary
    '''
    source_type = source.source_type
    if source_type != 'rss':
        return []

    results = rss.parse(source.link)
    for result in results:
        result['source'] = source
    return results
