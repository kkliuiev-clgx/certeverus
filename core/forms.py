from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(max_length=254)
    last_name = forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )

    def save(self, commit=True):
        instance = super(SignupForm, self).save(commit=False)
        if commit:
            instance.save()

        instance.refresh_from_db() # Load the profile instance created by the signal
        instance.profile.save()
        return instance


class ResetPasswordForm(forms.Form):
    step = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False, validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        step = cleaned_data.get("step")
        email = cleaned_data.get("email")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if step == 1:
            if not email:
                self.add_error(
                    "email",
                    "This field is required",
                )
        elif step == 2:
            if not password1:
                self.add_error(
                    "password1",
                    "This field is required",
                )

            if not password2:
                self.add_error(
                    "password2",
                    "This field is required",
                )

            if password1 and password2 and password1 != password2:
                self.add_error(
                    "password1",
                    "The passwords do not match",
                )

                self.add_error(
                    "password2",
                    "The passwords do not match",
                )
