from django.http import HttpResponse
from django.template import Context, loader
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def index(request):
    t = loader.get_template("frontpage/login-register.html")
    c = Context({'loginform': AuthenticationForm(),
                 'registerform': RegisterForm()})
    return HttpResponse(t.render(c))


class RegisterForm(UserCreationForm):
    firstname = forms.CharField(label='First name', widget=forms.TextInput())
    lastname = forms.CharField(label='Last name', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.TextInput())


def submit_registration(request):
    
