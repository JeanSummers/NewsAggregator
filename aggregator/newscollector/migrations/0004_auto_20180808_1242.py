# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-08 09:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newscollector', '0003_article_content_short'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='source',
            new_name='link',
        ),
    ]
