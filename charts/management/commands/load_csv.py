import csv

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from .models import Client

class Command(BaseCommand):
    help = 'Read CSV file and load to example.models.Data'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename', 
            type=str, 
            help='The full path to the csv file'
        )

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        field_row = {
            "parent": 0,
            "end_of_month": 1,
            "charting_category": 2,
            "driver": 3,
            "value_driver": 4,
        }
        # Get admin user to attach to client
        user = User.objects.get(username="admin")
        # Get client
        client, created = Client.objects.get_or_create(
            **{
                "user": user,
                "name": "DigiX Solutions"
            }
        )
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            count = 0
            for row in spamreader:
                entry = {}
                if count:
                    for k, v in field_row.items():
                        entry[k] = row[v]
                    # Add client
                    entry["client"] = client
                    data, created = Data.objects.get_or_create(
                        **entry
                    )
                count += 1
