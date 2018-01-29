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

#from apiApp import execution_urls
from apiApp import views as api_views

appname = "apiApp"
urlpatterns = [
    url('^repospec/create$', api_views.CreateRepoSpecView.as_view()),
    url('^repospec/get$', api_views.GetRepoSpecView.as_view()),
    url('^repospec/get_or_create$', api_views.GetOrCreateRepoSpecView.as_view()),
    url('^repospec/edit$', api_views.EditRepoSpecView.as_view()),
    #url('^execute/', include(execution_urls))
]

API_ACTION_CREATE = 'create'
API_ACTION_STATUS = 'status'
API_ACTION_RESULT = 'result'
api_actions = [API_ACTION_CREATE, API_ACTION_STATUS, API_ACTION_RESULT]
url_template_create = '^execute/%s/%s/(?P<namespace>[a-zA-Z0-9-]*)/(?P<repository>[a-zA-Z0-9-]*)/$'
url_template_status_result = '^execute/%s/%s/(?P<id>[a-zA-Z0-9-]*)/$'
name_template = '%s-executor-%s'
languages = [
    {
        'language': 'Shell Script',
        'lang_url': 'shell',
        'view': {
            API_ACTION_CREATE: api_views.ShellCodeExecutionCreateView,
            API_ACTION_STATUS: api_views.ShellCodeExecutionStatusView,
            API_ACTION_RESULT: api_views.ShellCodeExecutionResultView
        }
    },
    {
        'language': 'Python 3',
        'lang_url': 'python3',
        'view': {
            API_ACTION_CREATE: api_views.Py3CodeExecutionCreateView,
            API_ACTION_STATUS: api_views.Py3CodeExecutionStatusView,
            API_ACTION_RESULT: api_views.Py3CodeExecutionResultView
        }
    },
    {
        'language': 'PostgreSQL',
        'lang_url': 'postgresql',
        'view': {
            API_ACTION_CREATE: api_views.PGSQLCodeExecutionCreateView,
            API_ACTION_STATUS: api_views.PGSQLCodeExecutionStatusView,
            API_ACTION_RESULT: api_views.PGSQLCodeExecutionResultView
        }
    }
]

for language in languages:
    if language.get('lang_url', None) is not None and language.get('view', None) is not None:
        for action in api_actions:
            if action == API_ACTION_CREATE:
                url_template = url_template_create
            elif action == API_ACTION_STATUS or action == API_ACTION_RESULT:
                url_template = url_template_status_result
            else:
                raise ValueError("Unknown API Action: '%s'" % action)
            lang_views = language.get('view')
            if lang_views is not None:
                view = lang_views.get(action)
                if view is not None:
                    urlpatterns.append(
                        url(
                            url_template % (action, language.get('lang_url')),
                            view.as_view(),
                            name=name_template % (language.get('lang_url'), action)
                        )
                    )

for urlpattern in urlpatterns:
    print(urlpattern)
