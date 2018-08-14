from django.contrib import admin
from .models import Article, NewsSource

admin.site.register([
    Article,
    NewsSource
])
