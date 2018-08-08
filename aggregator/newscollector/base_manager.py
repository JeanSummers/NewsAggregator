'''
Database handlers

save()
accepts dicts or list of dicts
with fields named as Article fields

get()
retrieves all Articles,
article by id
or Articles in given range

'''

from .models import Article


def save(news):
    if type(news) is list:
        save_list(news)
    else:
        save_single(news)


def save_list(news: list):
    for article in news:
        save_single(article)


def save_single(article: dict):
    if article is None:
        return
    new, created = Article.objects.get_or_create(
        title=article['title'],
        date=article['date'],
        origin_link=article['origin_link'],
        link=article['link']
    )
    # shallow copy of article dict
    new.__dict__.update(article)
    new.save()


def get(pattern=None):
    if pattern is None:
        return get_all()
    if type(pattern) is int:
        return get_single(pattern)
    if type(pattern) is list:
        return get_range(pattern[0], pattern[1])
    return None


def get_all():
    return Article.objects.all()


def get_single(id):
    try:
        result = Article.objects.get(id=id)
    except:
        return None

    return result


def get_range(start, end):
    try:
        result = Article.objects.filter(id__gte=start, id__lte=end)
    except:
        return []

    return result
