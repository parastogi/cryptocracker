from django.http import HttpResponseRedirect
def login_required(function):
    def wrapper(request, *args, **kw):
        user=request.user
        print "login_required"
        if not (user.is_authenticated):
            return HttpResponseRedirect('/')
        else:
            return function(request, *args, **kw)
    return wrapper
