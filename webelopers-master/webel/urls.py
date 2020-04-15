from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from seDa import settings
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('', views.index),
    path('register', views.signup),
    path('login', views.login_view),
    path('logout', views.logout_view),
    path('contact', views.contact),
    path('profile', views.profile),
    path('panel', views.panel),
    path('setting', views.setting),
    path('makecourse', views.make_course),
    path('courses', views.courses),
]
