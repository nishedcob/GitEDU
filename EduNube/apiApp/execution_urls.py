
"""EduNube URL Configuration

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

from apiApp import views as api_views

#appname = "apiApp"
urlpatterns = [
]

url_template = '%s/(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/(?P<file_path>[a-zA-Z0-9/]*\.[a-zA-Z0-9]*)$'
name_template = '%s-executor'
languages = [
    {
        'language': 'Shell Script',
        'lang_url': 'shell',
        'view': api_views.ShellExecutionView
    },
    {
        'language': 'Python 3',
        'lang_url': 'python3',
        'view': api_views.Python3ExecutionView
    },
    {
        'language': 'PostgreSQL',
        'lang_url': 'postgresql',
        'view': api_views.PostgreSQLExecutionView
    }
]

for language in languages:
    if language.get('lang_url', None) is not None and language.get('view', None) is not None:
        urlpatterns.append(
            url(url_template % language.get('lang_url'),
                language.get('view'),
                name=name_template % language.get('lang_url')))
