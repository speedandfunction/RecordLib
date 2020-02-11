from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management.commands import createsuperuser
from django.contrib.auth.models import User
import secrets
import logging
import os


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Initialize an admin user"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_email = os.environ.get("ADMIN_EMAIL")
        if admin_username is None or admin_email is None:
            logger.info("env vars ADMIN_USERNAME or ADMIN_EMAIL are missing. Not creating initial admin.")
            return
        temp_password = secrets.token_urlsafe(30)
        admin_user = User.objects.filter(username=admin_username)
        if len(admin_user) == 0:
            # admin_user doesn't exist yet.
            User.objects.create_superuser(admin_username,admin_email, temp_password)
            logger.info(f"Temp admin {admin_username}: {temp_password}")
        else:
            logger.info("admin user already exists. Doing nothing.")

