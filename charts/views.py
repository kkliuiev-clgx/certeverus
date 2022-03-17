import json

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from core.mixins import LoginRequiredResponseMixin

from charts.models import ClientUser

from charts.utils import get_driver_items, get_parent_items, get_chart_data, get_attrib_items, get_filter_items, get_label_items



class DashboardView(LoginRequiredResponseMixin, TemplateView):
    login_url = "/login/"
    template_name = "charts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        return context


class APIView(LoginRequiredMixin, View):

    action = None

    def get(self, request, *args, **kwargs):

        if self.action == "get_client_data":
            return self.get_client_data(request, *args, **kwargs)
        elif self.action == "get_chart_data":
            return self.get_chart_data(request, *args, **kwargs)

    def get_client_data(self, request, *args, **kwargs):
        rtn = {
            "success": False,
        }

        client_user = ClientUser.objects.filter(user=request.user).last()

        if client_user:
            rtn = {
                "success": True,
                "data": {
                    "client": {
                        "id": client_user.client.id,
                        "name": client_user.client.name,
                        "ingestion_status": client_user.client.ingestion_status,
                    },
                    "drivers": get_driver_items(client_user.client),
                    "parents": get_parent_items(client_user.client),
                    "attribs": get_attrib_items(client_user.client),

                    "labels": get_label_items(client_user.client),
                    "filtered_by": get_filter_items(client_user.client)

                }
            }

        return JsonResponse(rtn, safe=False)

    def get_chart_data(self, request, *args, **kwargs):
        client_user = ClientUser.objects.get(
            user=request.user,
            client__id=kwargs.get("client_id"),
        )
        if client_user.client.ingestion_status == "processed":
            rtn = {
                "success": True,
                "data": get_chart_data(client_user.client, request.GET)
            }
        else:
            rtn = {
                "success": False,
                "message": "Data ingestion is not complete"
            }
        return JsonResponse(rtn)
