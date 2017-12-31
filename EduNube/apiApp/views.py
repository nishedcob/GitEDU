
import six
import importlib

from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import PermissionDenied

from authApp.tokens import validate_api_token
from EduNube.settings import DEFAULT_DOCKER_TAGS, DEFAULT_DOCKER_REGISTRY, VIRTUALIZATION_BACKEND
from apiApp.Validation import RepoSpec
from apiApp import models

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class CodeExecutionView(View):

    def get_virt_backend_str(self):
        virt_bk_str = VIRTUALIZATION_BACKEND.get(self.executor_name, None)
        if virt_bk_str is None:
            virt_bk_str = VIRTUALIZATION_BACKEND.get('default', None)
        return virt_bk_str

    #virt_backend_str = get_virt_backend_str()

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

    #virt_backend = load_virt_backend()

    executor_name = 'Generic'

    def get_docker_registry(self):
        return DEFAULT_DOCKER_REGISTRY.get('base', 'registry.gitlab.com')

    def get_docker_registry_user(self):
        return DEFAULT_DOCKER_REGISTRY.get('user', 'nishedcob')

    def get_docker_registry_repo(self):
        return '%s/%s' % (self.get_docker_registry_user(), DEFAULT_DOCKER_REGISTRY.get('repository', 'gitedu'))

    def get_full_docker_image_string(self):
        return '%s/%s/%s-executor' % (self.get_docker_registry(), self.get_docker_registry_repo(), self.executor_name)

    #docker_image = get_full_docker_image_string()
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


class RepoSpecFactory:

    def create_repospec(self, repo, parent=None):
        return RepoSpec.create(parent=parent, repo=repo)

    def get_repospec(self, repo=None, token=None):
        if repo is None and token is None:
            raise ValueError("Repo and Token can't both be None")
        else:
            params = {}
            if repo is not None:
                params['repo'] = repo
            if token is not None:
                params['token'] = token
            return models.RepoSpec.objects.get(**params)

    def get_or_create_repospec(self, repo=None, token=None, parent=None, edit_parent_if_found=False,
                               create_if_token_not_found=False):
        repospec = self.get_repospec(repo=repo, token=token)
        if repospec is None:
            if repo is None:
                raise ValueError("Can't create a new repospec with a repo that hasn't been specified")
            if token is None and not create_if_token_not_found:
                raise ValueError("It is impossible to create a new RepoSpec with a specific token specified beforehand")
            return self.create_repospec(repo=repo, parent=parent)
        else:
            if parent is not None and repospec.parent_repo != parent:
                if edit_parent_if_found:
                    repospec.parent_repo = parent
                else:
                    raise ValueError("Parent is distinct on found repospec, no permission to edit")
            return repospec

    def edit_repospec(self, repo=None, token=None, repospec=None, parent=None, new_repo=None, regen_secret_key=False):
        if repospec is None:
            try:
                repospec = self.get_repospec(repo=repo, token=token)
            except Exception:
                raise ValueError("Repo, Token and RepoSpec can't all be None")
        return RepoSpec.update_repospec(repospec=repospec, parent=parent, repo=new_repo,
                                        regen_secret_key=regen_secret_key)


@method_decorator(csrf_exempt, name='dispatch')
class RepoSpecGenericView(View, RepoSpecFactory):

    repospec = None

    def authenticate(self, request):
        client_token = request.POST.get('token')
        if client_token is None:
            raise PermissionDenied("No client token provided")
        if not validate_api_token(client_api_token=client_token):
            raise PermissionDenied("Invalid Token")

    def post_proc_steps(self):
        return [self.validate_call, self.post_pre_proc, self.post_proc, self.post_post_proc]

    def validate_call(self, request):
        if request.POST.get('repo') is None and request.POST.get('repospec_token') is None:
            raise ValueError("Repo and Token can't both be None")
        self.repospec = self.get_repospec(repo=request.POST.get('repo'), token=request.POST.get('repospec_token'))
        return None

    def post_pre_proc(self, request):
        return None

    def post_proc(self, request):
        return None

    def post_post_proc(self, request):
        return None

    def post(self, request):
        try:
            self.authenticate(request=request)
            for func in self.post_proc_steps():
                response = func(request=request)
                if response is not None:
                    return response
            return None
        except PermissionDenied as pe:
            return self.not_authorized(request=request, reason=pe)

    def return_repospec(self, only_token=False):
        token = self.repospec.token
        if type(token) == bytes:
            token = str(token, 'utf-8')
        json_data = {
            'token': token
        }
        if not only_token:
            repo = self.repospec.repo
            print("type repo: %s" % type(repo))
            print("repo: %s" % repo)
            if type(repo) == tuple:
                repo = repo[0]
            if type(repo) == list:
                repo = repo[0]
            if type(repo) == bytes:
                repo = str(repo, 'utf-8')
            #print("repo: %s" % repo)
            json_data['repo'] = repo,
            #print("repo (json data): %s" % json_data['repo'])
            #print(repo)
            if self.repospec.parent_repo is not None:
                #print("inside parent_repo")
                parent = self.repospec.parent_repo
                if type(parent) == bytes:
                    parent = str(parent, 'utf-8')
                json_data['parent'] = parent
            #print(repo)
            # Without this line here, which shouldn't be necessary,
            # json_data['repo'] incurs wacky data type corruption??? str -> tuple, no idea why
            json_data['repo'] = repo
            #print(repo)
        #print(json_data)
        #for key, value in json_data.items():
        #    print("%s : %s" % (key, value))
        return JsonResponse(data=json_data)


class CreateRepoSpecView(RepoSpecGenericView):

    def post_proc_steps(self):
        return [self.validate_call, self.post_proc]

    def validate_call(self, request):
        if request.POST.get('repo') is None:
            raise ValueError("A repo must be specified")
        return None

    def post_proc(self, request):
        repo = request.POST.get('repo')
        parent = request.POST.get('parent')
        self.repospec = self.create_repospec(repo=repo, parent=parent)
        return self.return_repospec(only_token=True)


class GetRepoSpecView(RepoSpecGenericView):

    def post_proc_steps(self):
        return [self.validate_call, self.post_proc]

    def post_proc(self, request):
        return self.return_repospec()


class EditRepoSpecView(RepoSpecGenericView):

    def post_proc_steps(self):
        return [self.validate_call, self.post_proc]

    def post_proc(self, request):
        parent = request.POST.get('parent')
        new_repo = request.POST.get('new_repo')
        regen_secret_key = request.POST.get('regen_secret_key') == "True"
        print("regen_secret_key: %s" % regen_secret_key)
        self.repospec = self.edit_repospec(repospec=self.repospec, parent=parent, new_repo=new_repo,
                                           regen_secret_key=regen_secret_key)
        return self.return_repospec(only_token=True)


class GetOrCreateRepoSpecView(RepoSpecGenericView):

    def post_proc_steps(self):
        return [self.validate_call, self.post_pre_proc, self.post_proc]

    def validate_call(self, request):
        try:
            super(GetOrCreateRepoSpecView, self).validate_call(request)
        except models.models.ObjectDoesNotExist:
            pass
        if self.repospec is None and request.POST.get('repo') is None:
            raise ValueError("Repo can't be None because we are creating a new RepoSpec")
        return None

    def post_pre_proc(self, request):
        if self.repospec is not None:
            exact_match = request.POST.get('exact_match') == "True"
            if exact_match:
                parent = request.POST.get('parent')
                if parent is not None and parent != self.repospec.parent_repo:
                    raise Http404("Found RepoSpec doesn't match parent")
            return self.return_repospec()
        return None

    def post_proc(self, request):
        repo = request.POST.get('repo')
        parent = request.POST.get('parent')
        self.repospec = self.create_repospec(repo=repo, parent=parent)
        return self.return_repospec(only_token=True)
