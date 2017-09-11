from django.conf.urls import url, include
from django.contrib import admin
from crypto import views
import settings
app_name='crypto'
urlpatterns = [
    url(r'^$',views.base,name='base'),
    url(r'^admin/', admin.site.urls),
    url(r'^quiz/',include('quiz.urls')),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^login/',views.loginm,name='loginm'),
    url(r'^logout/',views.logoutm,name='logoutm'),
    url(r'^(?P<uname>)[A-z]+/$',views.index,name='index'),
]