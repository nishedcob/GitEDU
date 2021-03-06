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
    url(r'^ns/(?P<namespace>[a-zA-Z0-9]*)/$', views.NamespaceView.as_view(), name="namespace"),
    url(r'^new/namespace/$', views.NewNamespaceView.as_view(), name="new_namespace"),
    url(r'^new/repository/$', views.NewFullRepositoryView.as_view(), name="new_full_repository"),
    url(r'^new/repo_file/$', views.NewRepositoryFileFormView.as_view(), name="new_repo_file"),
    url(r'^repo/(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/', views.RepositoryView.as_view(),
        name="repository"),
    url(r'^rf/(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/(?P<file_path>[a-zA-Z0-9/]*\.[a-zA-Z0-9]*)$',
        views.EditorFileView.as_view(), name="file_editor"),
    url(r'^cf/(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/(?P<change>[a-z0-9]*)/(?P<file_path>[a-zA-Z0-9/]*\.[a-zA-Z0-9]*)$',
        views.EditorChangeFileView.as_view(), name="change_file_editor"),
    url(r'^checkout/(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/(?P<change>[a-z0-9]*)/$',
        views.CheckoutFileVersionView.as_view(), name="checkout"),
    url(r'execute/(?P<namespace>[a-zA-Z0-9]*)/(?P<repository>[a-zA-Z0-9]*)/', views.RepositoryExecutionView.as_view(),
        name='repository_execution'),
    url(r'execute/status/(?P<job_id>[a-zA-Z0-9-]*)/', views.ExecutionStatusView.as_view(), name='execution_status'),
    url(r'execute/result/(?P<job_id>[a-zA-Z0-9-]*)/', views.ExecutionResultView.as_view(), name='execution_result')
]
