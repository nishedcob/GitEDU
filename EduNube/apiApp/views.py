
import six
import importlib

from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from authApp.tokens import validate_api_token
from EduNube.settings import DEFAULT_DOCKER_TAGS, DEFAULT_DOCKER_REGISTRY, VIRTUALIZATION_BACKEND

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CodeExecutionView(View):

    def get_virt_backend_str(self):
        virt_bk_str = VIRTUALIZATION_BACKEND.get(self.executor_name, None)
        if virt_bk_str is None:
            virt_bk_str = VIRTUALIZATION_BACKEND.get('default', None)
        return virt_bk_str

    virt_backend_str = get_virt_backend_str()

    def load_virt_backend(self):
        load_class = self.virt_backend_str
        try:
            module_path, class_name = load_class.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % load_class
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])
        mod = importlib.import_module(module_path)
        backend_manager_class = None
        try:
            backend_manager_class = getattr(mod, class_name)
        except AttributeError:
            msg = 'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name)
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])
        return backend_manager_class()

    virt_backend = load_virt_backend()

    executor_name = 'Generic'

    def get_docker_registry(self):
        return DEFAULT_DOCKER_REGISTRY.get('base', 'registry.gitlab.com')

    def get_docker_registry_user(self):
        return DEFAULT_DOCKER_REGISTRY.get('user', 'nishedcob')

    def get_docker_registry_repo(self):
        return '%s/%s' % (self.get_docker_registry_user(), DEFAULT_DOCKER_REGISTRY.get('repository', 'gitedu'))

    def get_full_docker_image_string(self):
        return '%s/%s/%s-executor' % (self.get_docker_registry(), self.get_docker_registry_repo(), self.executor_name)

    docker_image = get_full_docker_image_string()
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
