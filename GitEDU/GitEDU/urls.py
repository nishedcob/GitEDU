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
from django.conf.urls import url, include
from django.contrib import admin

#from ideApp import urls as ide_urls
#import ideApp.urls
import authApp.urls
#import socialApp.urls

import django_app_lti.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include(authApp.urls, namespace="auth")),
    url(r'^lti/', include(django_app_lti.urls, namespace="lti")),
    #url(r'^ide/', include(ideApp.urls, namespace="ide")),
    #url(r'^social/', include(socialApp.urls, namespace="social"))
]
