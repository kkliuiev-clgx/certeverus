from django.contrib import admin
from .models import Client, ClientFile, ClientUser


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ingestion_status")


class ClientUserAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "user")


class ClientFileAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "file", "ingestion_type", "ingestion_status")
    readonly_fields = ["ingestion_status"]


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientUser, ClientUserAdmin)
admin.site.register(ClientFile, ClientFileAdmin)
