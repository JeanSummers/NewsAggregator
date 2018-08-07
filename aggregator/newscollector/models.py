from django.db import models


class Article(models.Model):
    '''
    Модель новости
    '''
    title = models.CharField(
        max_length=255,
        blank=True,
        default='NewsTitle')
    content = models.TextField(
        blank=True)
    thumbnail = models.CharField(
        max_length=255,
        blank=True)
    origin_link = models.CharField(
        max_length=255,
        blank=True)
