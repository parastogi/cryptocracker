from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from crypto.models import Profile
from django.views import generic
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from crypto.decorators import login_required
# from django.views.decorators.cache import cache_control

def base(request):
    print "base"
    return render(request,'crypto/base.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def index(request,uname):
    print "index"

    return render(request,'crypto/base.html')

@login_required
def create_contest(request):

    return render(request,'crypto/create_contest.html')

def signup(request):
    print request.POST.get('username'),"l"
    user=User(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
    user.set_password(request.POST['password'])
    user.save()
    profile=Profile(user=user,roll=request.POST['roll'],phone=request.POST['ph_no'])
    profile.save()
    return redirect('/')
#

def loginm(request):
    print "1"
    print request.POST.get('username'),request.POST.get('password')

    user=User.objects.get(username=request.POST.get('username'))
    print user.username,user.password
    user = authenticate(request, username=user.username, password=request.POST.get('password'))
    print user
    if user is not None:
        login(request,user)
        return redirect('/'+user.username+'/')
    else:
        print "Wrong"
        return redirect('/')

@login_required
def logoutm(request):
    logout(request)
    return redirect('/')
