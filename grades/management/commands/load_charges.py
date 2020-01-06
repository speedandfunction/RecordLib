from django.core.management.base import BaseCommand, CommandError
from grades.models import ChargeRecord
import csv
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Load a file of charges into the database of a locally running grades app.
    """
    help = "Load charge records into the database of a local grades app from a csv file"

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        filepath = options['filepath']
        assert os.path.exists(filepath), f"File {filepath} does not exist!"

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ChargeRecord(**row).save()
                logger.info(f"Added {row}")
        
        logger.info("Finished adding charge records.")
