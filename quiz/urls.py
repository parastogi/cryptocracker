from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^past$',views.past,name="past"),
        url(r'^future$',views.future,name="future"),
        url(r'^live$',views.live,name="live"),
        url(r'^create_contest$',views.create_contest,name="create_contest")

]
