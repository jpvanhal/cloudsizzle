"""
Common forms.

Currently these are not so common, perhaps move them to login page

"""
from django import forms
# For custom form validation (password verification)
from django.forms.util import ErrorList


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    # Required fields have * at the end of label
    username = forms.CharField(
        label="Username*",
        min_length=4,
        max_length=20,
        error_messages={
            'required': 'Please enter a username',
            'min_length': 'The username must be at least 4 characters',
            'max_length': 'The username must be less than 21 characters'
        }
    )
    firstname = forms.CharField(
        label="First name",
        max_length=40,
        required=False,
        error_messages={
            'max_length': 'First name must be less than 41 characters'
        }
    )
    lastname = forms.CharField(
        label="Last name",
        max_length=40,
        required=False,
        error_messages={
            'max_length': 'Last name must be less than 41 characters'
        })
    password = forms.CharField(
        label="Password*",
        min_length=4,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please enter a password',
            'min_length': 'Password must be at least 4 characters'
        }
    )
    password_conf = forms.CharField(
        label="Confirm password*",
        min_length=4,
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Please confirm your password',
            'min_length': 'Password must be at least 4 characters'
        }
    )
    email = forms.EmailField(
        label="E-mail*",
        max_length=60,
        error_messages={
            'required': 'Please enter your e-mail',
            'max_length': 'E-mail must be less than 61 characters'
        }
    )
    consent = forms.BooleanField(
        label="I give my consent to the research study*",
        required=True,
        error_messages={
            'required': 'You must give your consent to research study in '
                        'order to register'
        }
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        password_conf = cleaned_data.get("password_conf")

        # Only display the error about password mismatches if
        # both password and confirmation are given.
        if password and password_conf and password != password_conf:
            msg = u"Passwords did not match."
            self._errors["password"] = ErrorList([msg])
            # If the template design is changed to display
            # errors near their associated fields you might
            # want to uncomment this.
            #self._errors["password_conf"] = ErrorList([msg])

            # Django example also removed the fields from cleaned
            # data. I'm not sure whether it is relevant here.
            del cleaned_data["password"]
            del cleaned_data["password_conf"]

        return cleaned_data
