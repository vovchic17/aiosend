import asyncio
import os

import django

from django.core.management import execute_from_command_line

from webhook_django.cryptopay import main



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webhook_django.settings")
django.setup()

if os.environ.get("RUN_MAIN") != "true":
    asyncio.run(main())

execute_from_command_line(["manage.py", "runserver"])
