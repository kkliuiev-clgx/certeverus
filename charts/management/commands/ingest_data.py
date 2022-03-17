import sys
import csv

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from charts.models import Client

from cvai import EncapsulationManager as em
from core.utils import get_engine

class Command(BaseCommand):
    help = 'Read local csv & excel files and load into Postgres'

    def add_arguments(self, parser):
        parser.add_argument(
            "--client-id",
            type=int,
            dest="client_id",
            help="Provide the Client ID for this ingestion",
        )

        parser.add_argument(
            "--process",
            action="store_true",
            dest="process",
            help="Process the clients that are ready for ingestion",
        )

    def handle(self, *args, **kwargs):
        process = kwargs.get("process")
        client_id = kwargs.get("client_id")
        if not process and not client_id:
            print("Please provide a --client-id option")
            sys.exit()

        if process:
            # For now we are limiting to processing one client at a time
            if Client.objects.filter(ingestion_status="processing").count():
                print("A client is already processing. Exiting...")
                sys.exit()
            client = Client.objects.filter(ingestion_status="ready_to_process").first()
            if not client:
                print("There is no client that is ready to process. Exiting...")
                sys.exit()

            client.ingestion_status = "processing"
            client.save()
        else:
            client = Client.objects.get(id=client_id)

        drivers, df , plan = em.pass_prepared_data(
            engine=get_engine(),
            save_data_to="postgres",
            source="local",
            client=client,
        )
