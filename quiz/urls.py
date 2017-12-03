from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^past$',views.past,name="past"),
        url(r'^live$',views.live,name="live"),
        url(r'^future$',views.future,name="future"),


        url(r'^past/(?P<hello>[0-9]+)/$',views.past_contest,name='past_contest'),
        url(r'^past/(?P<hello>[0-9]+)/leaderboard/$',views.past_leader,name='past_leader'),
        url(r'^(?P<hello>[0-9]+)/$',views.contest,name='contest'),
        url(r'^(?P<hello>[0-9]+)/submit$',views.submit,name='submit'),
        url(r'^(?P<hello>[0-9]+)/live/$',views.live_contest,name='live_contest'),
        url(r'^(?P<hello>[0-9]+)/register/$',views.register,name='register'),
        url(r'^(?P<hello>[0-9]+)/registeration/$',views.registeration,name='registeration'),
        url(r'^(?P<hello>[0-9]+)/live/leaderboard/$',views.leaderboard,name='leaderboard'),

        url(r'^create_contest$',views.create_contest,name="create_contest"),
        url(r'^edit_contest/(?P<contest_id>[0-9]+)$',views.edit_contest, name='edit_contest'),

        url(r'^(?P<contest_id>[0-9]+)/ajax$',views.ajax_q,name="ajax_q"),
]
