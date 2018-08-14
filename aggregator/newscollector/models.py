from django.db import models


class NewsSource(models.Model):
    '''
    Describes source of articles.
    Contains type that tells which handler
    shall be used for parsing this source link.
    Many-to-one with Article
    '''

    SOURCE_TYPES = (
        ('rss', 'RSS-feed'),
        ('html', 'Html page'),
        ('google-news', 'Google News API'),
        ('yandex-news', 'Yandex News API'),
    )

    source_type = models.CharField(
        max_length=64,
        choices=SOURCE_TYPES,
        default='rss')
    link = models.URLField()
    last_checked = models.DateTimeField(
        null=True)
    # Default thumbnail link
    image = models.URLField(
        blank=True)

    def __str__(self):
        return self.source_type + ' [' + self.link + ']'


class Article(models.Model):
    '''
    Describes news article
    with title, text, thumbnail and link to full
    '''
    # Before changing this first check:
    # .serializers.article_to_news_dict()
    # .rss_manager parsers

    title = models.CharField(
        max_length=255,
        blank=True)
    content = models.TextField(
        blank=True)
    content_short = models.TextField(
        blank=True)
    # Article image link
    thumbnail = models.URLField(
        blank=True)
    # Page where original article can be found
    link = models.URLField()
    date = models.DateTimeField()
    source = models.ForeignKey(
        NewsSource,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        # Before changing this first check:
        # .base_manager.save_single()
        unique_together = ('title', 'date', 'link')
