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
from ideApp.CodePersistenceBackends.MongoDB.mongodb_models import ChangeModel, ChangeFileModel, NamespaceModel,\
    RepositoryModel, RepositoryFileModel

from ideApp import git_server_http_endpoint

manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)

print("code persistence backend manager: <%s>" % manager)

# Create your views here.


class EditorClassView(View):  # TODO

    def get(self, class_id):
        pass

    def post(self, class_id):
        pass


class EditorAssignmentView(View):  # TODO

    def get(self, class_id, assignment_id):
        pass

    def post(self, class_id, assignment_id):
        pass


class NamespaceView(View):

    template = 'editor/namespace.html'
    sync_str = 'NR'

    def get(self, request, namespace):
        manager.sync(self.sync_str)
        context = {}
        backend_namespaces = manager.get_namespace(namespace=namespace)
        backend_namespace = manager.select_preferred_backend_object(result_set=backend_namespaces)
        context['namespace'] = backend_namespace
        backend_repositories = manager.list_repositories(namespace=namespace)
        prefered_backend_repositories = manager.select_preferred_backend_object(result_set=backend_repositories)
        context['repositories'] = []
        for backend_repository in prefered_backend_repositories:
            context['repositories'].append(backend_repository)
        context['detalles'] = True
        print("context: %s" % context)
        return render(request, self.template, context=context)


class RepositoryView(View):  # TODO

    def get(self, request, namespace, repository):
        return HttpResponse("<html><body><h1>%s / %s</h1></body></html>" % (namespace, repository))


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
    represents_change = False

    def validate_request(self, request, namespace, repository, change, file_path):
        return True

    def pre_request(self, request, namespace, repository, change, file_path):
        if not self.validate_request(request=request, namespace=namespace, repository=repository, change=change,
                                 file_path=file_path):
            raise PermissionDenied('Invalid Request')

    def get_edits(self, namespace, repository, file_path):
        manager.sync("NRF")
        namespace_objs = manager.get_namespace(namespace=namespace)
        namespace_obj = manager.select_preferred_backend_object(result_set=namespace_objs)
        repository_objs = manager.get_repository(namespace=namespace_obj, repository=repository)
        repository_obj = manager.select_preferred_backend_object(result_set=repository_objs)
        repository_file_objs = manager.get_file(namespace=namespace_obj, repository=repository_obj, file_path=file_path)
        repository_file_obj = manager.select_preferred_backend_object(result_set=repository_file_objs)
        file_edits = ChangeFileModel.objects.raw({
            'file': repository_file_obj.persistence_object.pk,
            'file_path': file_path
        })
        edits = []
        for file_edit in file_edits:
            change = ChangeModel.objects.raw({'_id': file_edit.change.pk}).first()
            edit = {
                'id': change.change_id,
                'author': change.author,
                'timestamp': change.timestamp.as_datetime().__str__(),
                'namespace': namespace,
                'repository': repository,
                'file_path': file_edit.file_path
            }
            edits.append(edit)
        edits.sort(key=lambda k: k['timestamp'])
        return edits

    def pre_get(self, request):
        manager.sync(self.sync_str)
        return request.user.username

    def proc_get(self, namespace, repository, file_path, change=None):
        return {
            'file_path': None,
            'file_contents': None,
            'prog_language': None
        }

    def post_get(self, request, namespace, repository, file_path, file_contents, prog_language, user, change):
        form = self.form_class(initial={'file_name': file_path, 'code': file_contents, 'language': prog_language})
        orig = True
        edits = self.get_edits(namespace=namespace, repository=repository, file_path=file_path)
        global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
        return self.render_editor(request, namespace, repository, form, global_perm_form, user, orig, edits, change)

    def get(self, request, namespace, repository, file_path, change=None):
        self.pre_request(request=request, namespace=namespace, repository=repository, file_path=file_path,
                         change=change)
        user = self.pre_get(request=request)
        prepared_params = self.proc_get(namespace=namespace, repository=repository, file_path=file_path, change=change)
        prepared_params['user'] = user
        prepared_params['request'] = request
        prepared_params['namespace'] = namespace
        prepared_params['repository'] = repository
        prepared_params['change'] = change
        return self.post_get(**prepared_params)

    def pre_post(self, request, namespace, repository, file_path):
        recieved_form = self.form_class(request.POST)
        if recieved_form.is_valid():
            return recieved_form
        else:
            user = request.user.username
            orig = True
            edits = self.get_edits(namespace=namespace, repository=repository, file_path=file_path)
            global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
            return self.render_editor(request, namespace, repository, recieved_form, global_perm_form, user, orig,
                                      edits)

    def proc_post(self, request, namespace, repository, file_path, recieved_form, change=None):
        pass

    def post_post(self, namespace, repository, new_file_path, change=None):
        return redirect('ide:file_editor', namespace, repository, new_file_path)

    def post(self, request, namespace, repository, file_path, change=None):
        self.pre_request(request=request, namespace=namespace, repository=repository, file_path=file_path,
                         change=change)
        pre_proc_post = self.pre_post(request, namespace, repository, file_path)
        if isinstance(pre_proc_post, self.form_class):
            this_proc_post = self.proc_post(request=request, namespace=namespace, repository=repository,
                                            file_path=file_path, recieved_form=pre_proc_post, change=change)
            if this_proc_post is not None and isinstance(this_proc_post, HttpResponse):
                return this_proc_post
            return self.post_post(namespace=namespace, repository=repository,
                                  new_file_path=pre_proc_post.cleaned_data.get('file_path', file_path), change=change)
        elif isinstance(pre_proc_post, HttpResponse):
            return pre_proc_post
        else:
            raise ValueError("'%s' is an unknown type" % pre_proc_post)

    def render_editor(self, request, namespace, repository, form, global_perm_form, user, orig, edits, change_id=None):
        context = {
            'form': form,
            'globalPermForm': global_perm_form,
            'owner': user,
            'orig': orig,
            'edits': edits,
            'new': self.newCode,
            'represents_change': self.represents_change,
            'editorLang': self.editorLangsAndCode,
            'namespace': namespace,
            'repository': repository
        }
        if self.represents_change and change_id is not None:
            context['change_id'] = change_id
        return render(request, self.template, context=context)


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
        try:
            old_pmcf = repository_file.persistence_object.current_change_file
            old_pchange = old_pmcf.change
            new_change.persistence_object.parent_change = old_pchange.pk
            new_change.save()
        except AttributeError:
            pass
        mcf = MongoChangeFile(new_change, file_path, code, language, repository_file)
        mcf.save()
        repository_file.persistence_object.current_change_file = mcf.persistence_object.pk
        repository_file.persistence_object.save()
        git_file_consumer = git_server_http_endpoint.FileGitSrvHTTPEpConsumer()
        git_edit_file = git_file_consumer.create_and_edit_contents_call(namespace=namespace, repository=repository,
                                                                        file_path=file_path, contents=code)
        return None


class EditorChangeFileView(GenericEditorFileView):

    sync_str = "NRF"
    change_comment = "Edited from GitEDU: Change File Editor"
    represents_change = True

    def validate_request(self, request, namespace, repository, change, file_path):
        return True

    def proc_get(self, namespace, repository, file_path, change=None):
        if change is None:
            raise ValueError("Change can't be None")
        if not isinstance(change, str):
            raise ValueError("Change must be a string")
        persisted_namespaces = NamespaceModel.objects.raw({'name': namespace})
        persisted_namespace = persisted_namespaces.first()
        persisted_repositories = RepositoryModel.objects.raw({'name': repository, 'namespace': persisted_namespace.pk})
        persisted_repository = persisted_repositories.first()
        persisted_changes = ChangeModel.objects.raw({'change_id': change, 'repository': persisted_repository.pk})
        persisted_change = persisted_changes.first()
        persisted_change_files = ChangeFileModel.objects.raw({'file_path': file_path, 'change': persisted_change.pk})
        persisted_change_file = persisted_change_files.first()
        file_contents = persisted_change_file.contents
        prog_language = persisted_change_file.prog_language
        return {
            'file_path': file_path,
            'file_contents': file_contents,
            'prog_language': prog_language
        }

    def proc_post(self, request, namespace, repository, file_path, recieved_form, change=None):
        manager.sync(self.sync_str)
        repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
        repository_file = manager.select_preferred_backend_object(result_set=repository_files)
        repository_objects = manager.get_repository(namespace=namespace, repository=repository)
        repository_object = manager.select_preferred_backend_object(result_set=repository_objects)
        new_file_path = recieved_form.cleaned_data.get('file_name', file_path)
        language = recieved_form.cleaned_data.get('language', "ot")
        code = recieved_form.cleaned_data.get('code', "")
        persisted_repository = repository_object.persistence_object
        persisted_changes = ChangeModel.objects.raw({'change_id': change, 'repository': persisted_repository.pk})
        persisted_change = persisted_changes.first()
        new_change_file = ChangeFileModel()
        new_change_file.prog_language = language
        new_change_file.file_path = new_file_path
        new_change_file.file = repository_file.persistence_object.pk
        new_change_file.contents = code
        comment = self.change_comment
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if request.user.is_authenticated:
            author = request.user.username
        else:
            author = "Anonymous"
        hasher = hashlib.new(self.hash_algo)
        hasher.update(new_change_file.__str__().encode('utf-8'))
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
        old_pchange = persisted_change.pk
        new_change.persistence_object.parent_change = old_pchange
        new_change.save()
        new_change.persistence_object.save()
        new_change_file.change = new_change.persistence_object.pk
        new_change_file.save()
        return redirect('ide:change_file_editor', namespace, repository, new_change.persistence_object.change_id, file_path)


class CheckoutFileVersionView(View):

    sync_str = "NRF"

    def get(self, request, namespace, repository, change):
        if not self.validate_request(request, namespace, repository):
            raise PermissionDenied("Insufficient permision to carry out the requested operation")
        manager.sync(self.sync_str)
        managed_repositories = manager.get_repository(namespace, repository)
        managed_repository = manager.select_preferred_backend_object(result_set=managed_repositories)
        persisted_changes = ChangeModel.objects.raw({
            'change_id': change,
            'repository': managed_repository.persistence_object.pk
        })
        persisted_change = persisted_changes.first()
        persisted_change_files = ChangeFileModel.objects.raw({
            'change': persisted_change.pk
        })
        file_path = None
        for pcf in persisted_change_files:
            prf = RepositoryFileModel.objects.raw({
                '_id': pcf.file.pk
            }).first()
            repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=prf.file_path)
            repository_file = manager.select_preferred_backend_object(result_set=repository_files)
            prf.contents = pcf.contents
            prf.prog_language = pcf.prog_language
            prf.file_path = pcf.file_path
            prf.current_change_file = pcf
            prf.save()
            repository_file.persistence_object = prf
            repository_file.load_persisted_values()
            repository_file.save()
            if file_path is None:
                file_path = prf.file_path
        if file_path is None:
            raise Exception("No file checked out")
        git_file_consumer = git_server_http_endpoint.FileGitSrvHTTPEpConsumer()
        git_edit_file = git_file_consumer.create_and_edit_contents_call(namespace=namespace, repository=repository,
                                                                        file_path=file_path,
                                                                        contents=repository_file.get_contents())
        return redirect('ide:file_editor', namespace, repository, file_path)

    def validate_request(self, request, namespace, repository):
        return True
