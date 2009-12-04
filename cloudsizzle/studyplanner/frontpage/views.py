from django.shortcuts import render_to_response

# Create your views here.
def frontpage(request):
    login = request.session.get('login', "")
    
    return render_to_response('frontpage.html', {
        'login': login
    })
