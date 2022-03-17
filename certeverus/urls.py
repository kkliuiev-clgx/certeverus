from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from core.views import (
    LoginView,
    LogoutView,
    SignupView,
    ResetPasswordView,
    status,
    # DashboardView
)

from charts.views import DashboardView, APIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", DashboardView.as_view(), name="dashboard"),
    path("status/", status, name="status"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("confirm/<str:uidb64>/<str:token>/", SignupView.as_view(action="confirm"), name="confirm_email"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view(action="confirm"), name="reset_password_confirmation"),

    path("api/clients/", APIView.as_view(action="get_client_data"), name="get_client_data"),
    path("api/clients/<int:client_id>/chart/", APIView.as_view(action="get_chart_data"), name="get_chart_data"),
]

admin.site.site_header = "CerteVerus Admin"
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
