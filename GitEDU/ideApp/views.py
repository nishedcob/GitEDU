import json
import hashlib
import time
import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
#from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

#from django_app_lti import models as lti_models
from . import constants
from .forms import CodeForm, CodeGlobalPermissionsForm, AddCollaboratorForm

from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager
from ideApp.CodePersistenceBackends.MongoDB.backend import MongoChangeFile

manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)

print("code persistence backend manager: <%s>" % manager)

# Create your views here.


class EditorClassView(View):

    def get(self, class_id):
        pass

    def post(self, class_id):
        pass


class EditorAssignmentView(View):

    def get(self, class_id, assignment_id):
        pass

    def post(self, class_id, assignment_id):
        pass


class GenericEditorFileView(View):
    form_class = CodeForm
    global_permission_form_class = CodeGlobalPermissionsForm
    collaborator_form_class = AddCollaboratorForm
    global_permission_initial = {
        'onlyAuthUsers': True,
        'onlyCollaborators': True,
        'globalCanWrite': False,
        'globalCanRead': False,
        'globalCanExecute': False,
        'globalCanDownload': False
    }
    template = 'editor/code.html'
    editorLangsAndCode = json.dumps(constants.EDITOR_LANGUAGES)
    newCode = None
    sync_str = None
    change_comment = "Edited from GitEDU"
    hash_algo = 'sha1'

    def validate_request(self, request, namespace, repository, change, file_path):
        return True

    def pre_request(self, request, namespace, repository, change, file_path):
        if not self.validate_request(request=request, namespace=namespace, repository=repository, change=change,
                                 file_path=file_path):
            raise PermissionDenied('Invalid Request')

    def get_edits(self, namespace, repository, file_path):
        pass

    def pre_get(self, request):
        manager.sync(self.sync_str)
        return request.user.username

    def proc_get(self, namespace, repository, file_path, change=None):
        return {
            'file_path': None,
            'file_contents': None,
            'prog_language': None
        }

    def post_get(self, request, file_path, file_contents, prog_language, user):
        form = self.form_class(initial={'file_name': file_path, 'code': file_contents, 'language': prog_language})
        orig = True
        edits = []
        global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
        return render(request, self.template, context={'form': form, 'globalPermForm': global_perm_form,
                                                       'owner': user, 'orig': orig, 'edits': edits,
                                                       'new': self.newCode,
                                                       'editorLang': self.editorLangsAndCode})

    def get(self, request, namespace, repository, file_path, change=None):
        self.pre_request(request=request, namespace=namespace, repository=repository, file_path=file_path,
                         change=change)
        user = self.pre_get(request=request)
        prepared_params = self.proc_get(namespace=namespace, repository=repository, file_path=file_path, change=change)
        prepared_params['user'] = user
        prepared_params['request'] = request
        return self.post_get(**prepared_params)

    def pre_post(self, request):
        recieved_form = self.form_class(request.POST)
        if recieved_form.is_valid():
            return recieved_form
        else:
            user = request.user.username
            orig = True
            edits = []
            global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
            return render(request, self.template, context={'form': recieved_form, 'globalPermForm': global_perm_form,
                                                           'owner': user, 'orig': orig, 'edits': edits,
                                                           'new': self.newCode,
                                                           'editorLang': self.editorLangsAndCode})

    def proc_post(self, request, namespace, repository, file_path, recieved_form, change=None):
        pass

    def post_post(self, namespace, repository, new_file_path, change=None):
        return redirect('ide:file_editor', namespace, repository, new_file_path)

    def post(self, request, namespace, repository, file_path, change=None):
        self.pre_request(request=request, namespace=namespace, repository=repository, file_path=file_path,
                         change=change)
        pre_proc_post = self.pre_post(request)
        if isinstance(pre_proc_post, self.form_class):
            self.proc_post(request=request, namespace=namespace, repository=repository, file_path=file_path,
                           recieved_form=pre_proc_post, change=change)
            return self.post_post(namespace=namespace, repository=repository,
                                  new_file_path=pre_proc_post.cleaned_data.get('file_path', file_path), change=change)
        elif isinstance(pre_proc_post, HttpResponse):
            return pre_proc_post
        else:
            raise ValueError("'%s' is an unknown type" % pre_proc_post)


class EditorFileView(GenericEditorFileView):

    sync_str = "NRF"
    change_comment = "Edited from GitEDU: Normal File Editor"

    def validate_request(self, request, namespace, repository, change, file_path):
        return True

    def proc_get(self, namespace, repository, file_path, change=None):
        repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
        repository_file = manager.select_preferred_backend_object(result_set=repository_files)
        if repository_file is None:
            manager.create_file(namespace=namespace, repository=repository, file_path=file_path, file_contents="",
                                language="ot")
            repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
            repository_file = manager.select_preferred_backend_object(result_set=repository_files)
        file_contents = ''
        if isinstance(repository_file,
                      manager.select_preferred_backend_object(manager.get_repository_file_class())):
            file_contents = repository_file.get_contents()
        prog_language = 'ot'
        if isinstance(repository_file,
                      manager.select_preferred_backend_object(manager.get_repository_file_class())):
            prog_language = repository_file.get_language()
        return {
            'file_path': file_path,
            'file_contents': file_contents,
            'prog_language': prog_language
        }

    def proc_post(self, request, namespace, repository, file_path, recieved_form, change=None):
        manager.sync(self.sync_str)
        repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
        repository_file = manager.select_preferred_backend_object(result_set=repository_files)
        if repository_file is None:
            manager.create_file(namespace=namespace, repository=repository, file_path=file_path,
                                file_contents="", language="ot")
            repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
            repository_file = manager.select_preferred_backend_object(result_set=repository_files)
        repository_objects = manager.get_repository(namespace=namespace, repository=repository)
        repository_object = manager.select_preferred_backend_object(result_set=repository_objects)
        if repository_object is None:
            manager.create_repository(namespace=namespace, repository=repository)
            repository_objects = manager.get_repository(namespace=namespace, repository=repository)
            repository_object = manager.select_preferred_backend_object(result_set=repository_objects)
        new_file_path = recieved_form.cleaned_data.get('file_name', file_path)
        language = recieved_form.cleaned_data.get('language', "ot")
        code = recieved_form.cleaned_data.get('code', "")
        if not isinstance(repository_file,
                          manager.select_preferred_backend_object(manager.get_repository_file_class())):
            repo_file_class = manager.select_preferred_backend_object(manager.get_repository_file_class())
            repository_file = repo_file_class(file_path=new_file_path, contents=code, repository=repository_object)
            manager.save_existent_file(namespace=namespace, repository=repository, file=repository_file)
        repository_file.set_file_path(new_file_path)
        repository_file.set_contents(code)
        repository_file.set_repository(repository_object)
        repository_file.set_language(language)
        repository_file.save()
        comment = self.change_comment
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if request.user.is_authenticated:
            author = request.user.username
        else:
            author = "Anonymous"
        hasher = hashlib.new(self.hash_algo)
        hasher.update(repository_file.__str__().encode('utf-8'))
        hasher.update(repository.encode('utf-8'))
        hasher.update(namespace.encode('utf-8'))
        hasher.update(comment.encode('utf-8'))
        hasher.update(author.encode('utf-8'))
        hasher.update(timestamp.encode('utf-8'))
        id = hasher.hexdigest()
        manager.create_change(namespace=namespace, repository=repository, id=id, comment=comment,
                              author=author, timestamp=timestamp)
        new_changes = manager.get_change(namespace=namespace, repository=repository, change=id)
        new_change = manager.select_preferred_backend_object(result_set=new_changes)
        new_change.save()
        mcf = MongoChangeFile(new_change, file_path, code, language, repository_file)
        mcf.save()
