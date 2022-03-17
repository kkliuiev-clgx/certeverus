import json

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm
)
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from core.forms import SignupForm, ResetPasswordForm
from core.tokens import account_activation_token
from core.mixins import LoginRequiredResponseMixin, CsrfMixin


class LoginView(CsrfMixin, TemplateView):
    template_name = "core/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

    def post(self, request, *args, **kwargs):
        rtn = {
            "success": False,
            "message": "",
        }
        data = json.loads(request.body)
        status = 200

        form = AuthenticationForm(request=request, data=data)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                rtn["success"] = True
                rtn["redirect"] = reverse("dashboard")
        else:
            status=401
            rtn["errors"] = form.errors

        return JsonResponse(rtn, status=status)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        rtn = {
            "success": False,
            "message": "",
        }
        status = 200

        logout(request)

        rtn["success"] = True
        rtn["redirect"] = reverse("dashboard")

        return JsonResponse(rtn, status=status)


class SignupView(TemplateView):
    template_name = "core/signup.html"

    action = None
    data = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.action == "confirm":
            context["title"] = "Confirm"
        else:
            context["title"] = "Signup"

        if self.data:
            context["data"] = json.dumps(self.data, default=str)
        return context

    def get(self, request, *args, **kwargs):
        if self.action == "confirm":
            return self.confirm(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        rtn = {
            "success": False,
            "message": "",
        }
        data = json.loads(request.body)
        status = 200

        form = SignupForm(data=data)
        if form.is_valid():
            user = form.save(commit=True) # Commit so profile is saved
            user.is_active = False
            user.save()

            # Send confirmation email
            subject = settings.ACCOUNT_ACTIVATION_EMAIL_SUBJECT
            message = render_to_string("core/activation_email.html", {
                "user": user,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            rtn["success"] = True
            rtn["redirect"] = reverse("login")
            rtn["message"] = "You are successfully signed up. You can activate your account by confirming your email."
        else:
            rtn["message"] = "Failed to signup. Encountered the validation errors below!"
            rtn["errors"] = form.errors

        return JsonResponse(rtn, status=status)

    def confirm(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        self.data = {
            "success": False,
            "message": True,
        }

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (AttributeError, TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_is_confirmed = True
            user.save()
            login(request, user)

            self.data["success"] = True
            self.data["message"] = "Your email has been successfully confirmed. You are now logged in!"
            self.data["redirect"] = reverse("dashboard")

        else:
            self.data["message"] = "Failed to confirm this email. Try again!"

        return super().get(request, *args, **kwargs)


class ResetPasswordView(TemplateView):
    template_name = "core/reset_password.html"

    action = None
    data = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reset password"
        if self.action == "confirm":
            self.data["uid"] = kwargs.get("uidb64")
            self.data["token"] = kwargs.get("token")

        if self.data:
            context["data"] = json.dumps(self.data, default=str)
        return context

    def get(self, request, *args, **kwargs):
        if self.action == "confirm":
            return self.confirm(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        rtn = {
            "success": False,
            "message": "",
        }
        data = json.loads(request.body)
        status = 200

        form = ResetPasswordForm(data=data)
        if form.is_valid():
            if data.get("step") == 1:
                user = User.objects.filter(email__iexact=data.get("email")).first()

                if user:
                    # Send confirmation email
                    subject = settings.FORGOT_PASSWORD_EMAIL_CONFIRMATION_SUBJECT
                    message = render_to_string("core/reset_password_confirmation_email.html", {
                        "user": user,
                        "domain": get_current_site(request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    })
                    user.email_user(subject, message)

                rtn["success"] = True
                rtn["message"] = "If your account exists then you will get an email with the confirmation code. "

            elif data.get("step") == 2:

                uidb64 = kwargs.get("uidb64")
                token = kwargs.get("token")

                try:
                    uid = force_text(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)
                except (AttributeError, TypeError, ValueError, OverflowError, User.DoesNotExist):
                    user = None

                if user is not None and account_activation_token.check_token(user, token) and user.profile.reset_password:
                    user.profile.reset_password = False
                    user.profile.save()
                    user.set_password(data.get("password1"))
                    user.save()

                    rtn["success"] = True
                    rtn["message"] = "Your password has been successfully changed. You can login now!"
                    rtn["redirect"] = reverse("login")

                else:
                    rtn["message"] = "Failed to reset your password. The token may have expired. Try again from step 1!"

        else:
            if data.get("step") == 1:
                rtn["message"] = "Failed to send confirmation email. Encountered the validation errors below!"
            elif data.get("step") == 2:
                rtn["message"] = "Failed to reset password. Encountered the validation errors below!"
            rtn["errors"] = form.errors

        return JsonResponse(rtn, status=status)

    def confirm(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        self.data = {
            "success": False,
            "message": True,
        }

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (AttributeError, TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.profile.reset_password = True
            user.profile.save()

            self.data["success"] = True
            self.data["message"] = "Your email has been successfully confirmed. You can now change your password!"

        else:
            self.data["message"] = "Failed to confirm this email. Try again!"
            self.data["redirect"] = reverse("reset_password")

        return super().get(request, *args, **kwargs)


class DashboardView(LoginRequiredResponseMixin, TemplateView):
    login_url = "/login/"
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        return context


def status(request):
    return JsonResponse({'status': 'OK'})
