""" Common form. Currently these are not so common, perhaps move them to login page"""
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    # Required fields have * at the end of label
    username = forms.CharField(label="Username*", min_length=4, max_length=20, error_messages={'required':'Please enter a username', 'min_length':'The username must be at least 4 characters', 'max_length':'The username must be less than 21 characters'})
    firstname = forms.CharField(label="First name", max_length=40, required=False, error_messages={'max_length':'First name must be less than 41 characters'})
    lastname = forms.CharField(label="Last name", max_length=40, required=False, error_messages={'max_length':'Last name must be less than 41 characters'})
    password = forms.CharField(label="Password*", min_length=4, widget=forms.PasswordInput, error_messages={'required':'Please enter a password', 'min_length':'Password must be at least 4 characters'})
    password_conf = forms.CharField(label="Confirm password*", min_length=4, widget=forms.PasswordInput, error_messages={'required':'Please confirm your password', 'min_length':'Password must be at least 4 characters'})
    email = forms.EmailField(label="E-mail*", max_length=60, error_messages={'required':'Please enter your e-mail', 'max_length':'E-mail must be less than 61 characters'})
    consent = forms.BooleanField(label="I give my consent to the research study*", required=True, error_messages={'required':'You must give your consent to research study in order to register'})
