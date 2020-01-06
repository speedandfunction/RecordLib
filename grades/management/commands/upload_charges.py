from django.core.management.base import BaseCommand, CommandError
from grades.models import ChargeRecord
from grades.serializers import ChargeRecordSerializer
import csv
import os
import logging
import requests
from getpass import getpass

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Upload charges to a remote charges app from a csv table.


    This command is probably only to be used once when setting up a database. It will insert all the rows
    of the provided csv file, and won't consider whether rows are already present. So using it multiple times
    with the same csv file and the same database will lead to duplicates.    
    """
    help = "Upload charges to a remote charges app from a csv table."

    def add_arguments(self, parser):
        parser.add_argument("loginurl", help="URL of the login url for the app you're adding charges to")
        parser.add_argument("url", help="The url of the charges api create endpoint.")
        parser.add_argument("filepath", help="Path to csv file with charges to add")

    def handle(self, *args, **options):
        filepath = options['filepath']
        loginurl = options['loginurl']
        url = options['url']
        assert os.path.exists(filepath), f"File {filepath} does not exist!"


        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            new_charges = [ChargeRecord(**row) for row in reader]
        
        username = getpass(f"Username for {loginurl}?")
        pwd = getpass(f"Password: ")


        with requests.Session() as sess:
            resp = sess.get(loginurl)
            csrf = resp.cookies['csrftoken']
            auth_response = sess.post(
                loginurl, 
                data = {'csrfmiddlewaretoken': csrf, "username": username, "password": pwd})        
            assert auth_response.status_code == 200

            resp = sess.get(url)
            csrf = sess.cookies['csrftoken']
            for ch in new_charges:
                dt = ChargeRecordSerializer(ch).data
                dt.pop('id')
                dt['csrfmiddlewaretoken'] = csrf
                resp = sess.post(
                    url,
                    data = dt
                )
                logger.info(f"Uploaded charge {ch}")

        logger.info("Finished adding charge records.")