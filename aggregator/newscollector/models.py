from django.db import models


class Article(models.Model):
    '''
    News model
    '''
    # Before changing this first check:
    # .serializers.article_to_news_dict()
    # .rss_manager parsers

    title = models.CharField(
        max_length=255,
        blank=True,
        default='NewsTitle')
    content = models.TextField(
        blank=True)
    content_short = models.TextField(
        blank=True)
    # Article image link
    thumbnail = models.CharField(
        max_length=255,
        blank=True)
    # Page from where rss came from
    origin_link = models.CharField(
        max_length=255,
        blank=True)
    # Page where original article can be found
    link = models.CharField(
        max_length=255)
    date = models.DateTimeField()

    class Meta:
        ordering = ['-date']
        # Before changing this first check:
        # .base_manager.save_single()
        unique_together = ('title', 'date', 'link')
