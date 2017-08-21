"""GitEDU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

appname = "authApp"
urlpatterns = [
    url(r'^lti/decode/(?P<resource_id>[0-9]$)$', views.DecodeView.as_view(), name="lti_decode"),
    url("^login", auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    url("^logout", auth_views.logout, {'template_name': 'auth/logout.html', 'next_page': 'auth:login'}, name='logout'),
    url("^register", views.RegistrationView.as_view(), name='registration'),
]
