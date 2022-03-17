import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


class LoginRequiredResponseMixin(LoginRequiredMixin):

    def __init__(self, *args, **kwargs):
        self.data = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.profile.avatar:
            avatar_url = self.request.user.profile.avatar.url
        else:
            avatar_url = None

        self.data["user"] = {
            "username": self.request.user.username,
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
            "avatar": avatar_url,
        } 

        if self.data:
            context["data"] = json.dumps(self.data, default=str)

        return context


class CsrfMixin:
    """
    This mixin ensures that the csrf cookie is set for the GET request
    """
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
