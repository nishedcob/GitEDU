
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from authApp.tokens import validate_api_token
from EduNube.settings import DEFAULT_DOCKER_TAGS

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CodeExecutionView(View):

    csrf_token_template = 'auth/csrf_token.html'

    executor_name = 'Generic'

    docker_image = 'registry.gitlab.com/nishedcob/gitedu/%s-executor' % executor_name
    docker_tag = DEFAULT_DOCKER_TAGS.get('default', None) if DEFAULT_DOCKER_TAGS.get(executor_name, None) is None\
        else DEFAULT_DOCKER_TAGS.get(executor_name)

    def build_docker_string(self):
        if not self.docker_image:
            raise ValueError('Docker_Image can\'t be None')
        if self.docker_tag:
            return "%s:%s" % (self.docker_image, self.docker_tag)
        return self.docker_image

    def post_proc_steps(self):
        return [self.validate_call, self.pre_proc, self.proc, self.post_proc]

    def authenticate(self, request):
        client_token = request.POST.get('token')
        if client_token is None:
            raise PermissionDenied("No client token provided")
        if not validate_api_token(client_api_token=client_token):
            raise PermissionDenied("Invalid Token")

    def not_authorized(self, request, reason):
        raise reason

    def validate_call(self, request, namespace, repository, file_path):
        return None

    def pre_proc(self, request, namespace, repository, file_path):
        return None

    def proc(self, request, namespace, repository, file_path):
        return None

    def post_proc(self, request, namespace, repository, file_path):
        return None

    def post(self, request, namespace, repository, file_path):
        try:
            self.authenticate(request=request)
            for func in self.post_proc_steps():
                response = func(request=request, namespace=namespace, repository=repository, file_path=file_path)
                if response is not None:
                    return response
            return None
        except PermissionDenied as pe:
            return self.not_authorized(request=request, reason=pe)

    def get(self, request, namespace, repository, file_path):
        # TODO: Return CSRF Token
        return render(request, self.csrf_token_template)
        #return HttpResponse("<h1>%s</h1><br><h2>%s</h2><br><h2>%s</h2>" % (namespace, repository, file_path))


class ShellExecutionView(CodeExecutionView):

    executor_name = 'shell'

    # can override with:
    #docker_image = 'registry.gitlab.com/nishedcob/gitedu/shell-executor'
    # can override default pulled from settings with:
    #docker_tag = None


class Python3ExecutionView(CodeExecutionView):

    executor_name = 'python3'

    # can override with:
    #docker_image = 'registry.gitlab.com/nishedcob/gitedu/python3-executor'
    # can override default pulled from settings with:
    #docker_tag = None


class PostgreSQLExecutionView(CodeExecutionView):

    executor_name = 'postgresql'

    # can override with:
    #docker_image = 'registry.gitlab.com/nishedcob/gitedu/postgresql-executor'
    # can override default pulled from settings with:
    #docker_tag = None
