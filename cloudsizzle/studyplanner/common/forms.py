""" Common form. Currently these are not so common, perhaps move them to login page"""
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    # Required fields have * at the end of label
    username = forms.CharField(min_length=4, max_length=20, label="Username*")
    firstname = forms.CharField(max_length=40, required=False, label="First name")
    lastname = forms.CharField(max_length=40, required=False, label="Last name")
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, label="Password*")
    password_conf = forms.CharField(min_length=4, widget=forms.PasswordInput, label="Confirm password*")
    email = forms.EmailField(max_length=60, required=False, label="E-mail*")
    consent = forms.BooleanField(required=True, label="I give my consent to the research study*")
