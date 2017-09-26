import json

from django.shortcuts import render, redirect
from django.views import View
#from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

#from django_app_lti import models as lti_models
from . import constants
from .forms import CodeForm, CodeGlobalPermissionsForm, AddCollaboratorForm

from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager

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

class EditorFileView(View):

    form_class = CodeForm
    global_permission_form_class = CodeGlobalPermissionsForm
    collaborator_form_class = AddCollaboratorForm
    global_permission_initial = {'onlyAuthUsers': True,
               'onlyCollaborators': True,
               'globalCanWrite': False,
               'globalCanRead': False,
               'globalCanExecute': False,
               'globalCanDownload': False
               }
    template = 'editor/code.html'
    editorLangsAndCode = json.dumps(constants.EDITOR_LANGUAGES)
    newCode = None

    def validate_request(self, request, namespace, repository, file_path):
        return True

    def get(self, request, namespace, repository, file_path):
        if self.validate_request(request, namespace, repository, file_path):
            user = request.user.username
            repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
            repository_file = manager.select_preferred_backend_object(result_set=repository_files)
            if repository_file is None:
                manager.create_file(namespace=namespace, repository=repository, file_path=file_path, file_contents="")
                repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
                repository_file = manager.select_preferred_backend_object(result_set=repository_files)
            file_contents = ''
            if isinstance(repository_file, manager.select_preferred_backend_object(manager.get_repository_file_class())):
                file_contents = repository_file.get_file_contents()
            form = self.form_class(initial={'file_name': file_path, 'code': file_contents})
            orig = True
            edits = []
            global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
            return render(request, self.template, context={'form': form, 'globalPermForm': global_perm_form,
                                                                       'owner': user, 'orig': orig, 'edits': edits,
                                                                       'new': self.newCode,
                                                                       'editorLang': self.editorLangsAndCode})
        else:
            raise PermissionDenied("Illegal Request")

    def post(self, request, namespace, repository, file_path):
        if self.validate_request(request, namespace, repository, file_path):
            recieved_form = self.form_class(request.POST)
            if recieved_form.is_valid():
                repository_files = manager.get_file(namespace=namespace, repository=repository, file_path=file_path)
                repository_file = manager.select_preferred_backend_object(result_set=repository_files)
                if repository_file is None:
                    manager.create_file(namespace=namespace, repository=repository, file_path=file_path,
                                        file_contents="")
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
                repository_file.set_file_contents(code)
                repository_file.set_repository(repository_object)
                repository_file.save()
                return redirect('ide:file_editor', namespace, repository, new_file_path)
            else:
                user = request.user.username
                orig = True
                edits = []
                global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
                return render(request, self.template, context={'form': recieved_form, 'globalPermForm': global_perm_form,
                                                                       'owner': user, 'orig': orig, 'edits': edits,
                                                                       'new': self.newCode,
                                                                       'editorLang': self.editorLangsAndCode})
        else:
            raise PermissionDenied("Illegal Request")
