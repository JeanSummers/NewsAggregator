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

# Fast save
from django.db import transaction


def save(news):
    if type(news) is list:
        save_list(news)
    else:
        save_single(news)


@transaction.atomic  # Fast save
def save_list(news: list):
    for article in news:
        save_single(article)


def save_single(article: dict):
    if article is None:
        return
    new, created = Article.objects.get_or_create(
        title=article['title'],
        date=article['date'],
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
        result = Article.objects.all()[int(start): int(end)]
    except:
        return []

    return result


def get_filtered_range(start, end, filters: list):
    articles = Article.objects.all()

    lowcased = [item.lower() for item in filters]

    '''
    matches = []
    for pattern in lowcased:
        matches.append(
            articles.filter(title__icontains=pattern) |
            articles.filter(content_short__icontains=pattern))

    result = Article.objects.none()
    for match in matches:
        result = result | match
    '''

    articles = list(articles)
    articles = list(filter(
        lambda item: match_any(
            [item.title.lower(), item.content_short.lower()], lowcased),
        articles))

    return articles[int(start): int(end)]


def match_any(items, patterns):
    for item in items:
        for pattern in patterns:
            if item.find(pattern) != -1:
                return True
    return False
