import logging
from typing import Any, Optional
from django.core.management.base import BaseCommand
from apps.explore_tab_crawling.models import *
from apps.explore_tab_crawling.views import *

class Command(BaseCommand):
    help = 'Crawl explore tab data'

    def handle(self, *args: Any, **options):
        logging.info('delete words and article')
        # Content.objects.all().delete()
        # Hashtag.objects.all().delete()

        logging.info('run explore tab data crawler')

        save_contents()
        save_hashtags()

        self.stdout.write(self.style.SUCCESS('Successfully loaded crawl data.'))