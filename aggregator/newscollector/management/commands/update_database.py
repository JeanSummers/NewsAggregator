from django.core.management.base import BaseCommand

import newscollector.common as common


class Command(BaseCommand):

    help = 'Drains article from all sources and saves in database'

    def handle(self, *args, **options):
        common.update_database()
