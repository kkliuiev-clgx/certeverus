from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email_is_confirmed")


admin.site.register(Profile, ProfileAdmin)
