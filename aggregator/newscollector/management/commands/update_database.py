from django.core.management.base import BaseCommand

import newscollector.tasks as tasks


class Command(BaseCommand):

    help = 'Drains article from all sources and saves in database'

    def handle(self, *args, **options):
        tasks.update_database()
