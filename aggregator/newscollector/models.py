from django.db import models


class Article(models.Model):
    '''
    News model
    '''
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
        unique_together = ('title', 'date', 'origin_link', 'link')
