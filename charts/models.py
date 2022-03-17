import os

from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

get_model = apps.get_model


class Client(models.Model):

    STATUS_CHOICES = (
        ("unprocessed", "Unprocessed"),
        ("ready_to_process", "Ready to process"),
        ("processing", "Processing"),
        ("processed", "Processed"),
        ("error", "Error during processing"),
    )

    name = models.CharField(max_length=255, db_index=True)
    ingestion_status = models.CharField(max_length=255, db_index=True, default="unprocessed", choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.name}"

    def get_drivers_table_name(self):
        return f"drivers_for_client_{self.id}"

    def get_dfclean_table_name(self):
        return f"dfclean_for_client_{self.id}"

    def get_plan_table_name(self):
        return f"plan_for_client_{self.id}"

    def get_files(self, ingestion_type):
        clientFile = get_model("charts", "ClientFile")
        return ClientFile.objects.filter(
            client=self,
            ingestion_type=ingestion_type,
        )

    def get_storage_backend(self):
        if settings.DEFAULT_FILE_STORAGE == "storages.backends.s3boto3.S3Boto3Storage":
            return "s3"
        return "file"


class ClientFile(models.Model):

    INGESTION_TYPES = (
        ("driver", "Drivers (only single file allowed)"),
        ("combined_data", "Actuals (only single file allowed)"),
        ("plan", "Plan (multiple files allowed)"),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    file = models.FileField()
    ingestion_type = models.CharField(max_length=255, db_index=True, choices=INGESTION_TYPES)
    ingestion_status = models.CharField(max_length=255, db_index=True, default="unprocessed", choices=Client.STATUS_CHOICES)
    ingestion_error = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return os.path.basename(self.file.name)

    def get_file_info(self):
        name, ext = os.path.splitext(self.file.name)
        return name, ext.lower().replace(".", "")


class ClientUser(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
