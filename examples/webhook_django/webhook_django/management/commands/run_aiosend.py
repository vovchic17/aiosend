import asyncio
import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from webhook_django.cryptopay import main


class Command(BaseCommand):
    help = "Create invoice and start Django server"

    def handle(self, *args, **options):
        if os.environ.get("RUN_MAIN") != "true":
            asyncio.run(main())
        call_command("runserver")
