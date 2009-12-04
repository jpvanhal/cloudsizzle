from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context, loader
#from cloudsizzle.asi.loginHandler import LoginHandler
from studyplanner.session.forms import LoginForm
from cloudsizzle.asi.fakeAsi import FakeAsi

# Create your views here.
def index(request):
    # Form error message
    message = request.session.get('login_message', "");
    # pre-filled username
    pre_username = request.session.get('pre_username', "");
    # User sent the form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if FakeAsi.login(form.cleaned_data['username'],
                             form.cleaned_data['password']):
                request.session['login'] = form.cleaned_data['username']
                return HttpResponseRedirect('/')
            else:
                request.session['login_username'] = form.cleaned_data['username']
                request.session['login_message'] = "Invalid login, please retry"
                return HttpResponseRedirect('/session/')
    # No form sent
    else:
        form = LoginForm()
    
    # Render the form
    return render_to_response('login.html', {
        'form': form, 'message': message
    })
