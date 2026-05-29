import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Waits until the database connection
    becomes available before continuing.
    """

    def handle(self, *args, **options):
        self.stdout.write(
            "Waiting for database connection..."
        )

        database_connection = None

        while not database_connection:
            try:
                database_connection = connections["default"]
                database_connection.cursor()

            except OperationalError:
                self.stdout.write(
                    "Database unavailable, retrying in 1 second..."
                )

                time.sleep(1)

        self.stdout.write(
            self.style.SUCCESS(
                "Database connection established successfully!"
            )
        )