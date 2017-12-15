from django.conf.urls import url, include
from django.contrib import admin
from crypto import views
from django.conf.urls.static import static
from django.conf import settings

app_name='crypto'
urlpatterns = [
    url(r'^$',views.base,name='base'),
    url(r'^admin/', admin.site.urls),
    url(r'^quiz/',include('quiz.urls')),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^login/',views.loginm,name='loginm'),
    url(r'^logout/',views.logoutm,name='logoutm'),
    url(r'make_admin/',views.make_admin,name='make_admin'),
    url(r'admin-form/',views.admin_form,name='admin_form'),
    # url(r'^create_contest/',views.create_contest,name='create_contest'),
    url(r'^(?P<uname>[0-z]+)/$',views.index,name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
