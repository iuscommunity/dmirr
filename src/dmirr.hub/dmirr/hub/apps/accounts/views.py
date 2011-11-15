
from django.shortcuts import redirect
    
def index_view(request):
    if request.user.is_authenticated():
        return redirect('/account/%s/' % request.user.username)
    else:
        return redirect('/account/signin/')
    
