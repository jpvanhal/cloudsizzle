from django.http import HttpResponse
from django.template import Context, loader
from django import forms

def index(request):
    t = loader.get_template("frontpage/login-register.html")
    c = Context({'loginform': LoginForm()})
    return HttpResponse(t.render(c))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(render_value=False))
    
