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

from . import views

appname = "ideApp"
urlpatterns = [
    url(r'^(?P<class_id>[0-9]*)/$', views.EditorClassView.as_view(), name="class"),
    url(r'^(?P<class_id>[0-9]*)/(?P<assignment_id>[0-9]*)$', views.EditorAssignmentView.as_view(), name="assignment"),
    url(r'^(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/(?P<file_path>[a-zA-Z0-9/]*\.[a-zA-Z0-9]*)$', views.EditorFileView.as_view(), name="file_editor"),
]
