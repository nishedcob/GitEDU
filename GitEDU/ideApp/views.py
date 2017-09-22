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
            form = self.form_class(initial={'file_name': file_path})
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
            new_file_path = file_path

            return redirect('file-editor', namespace=namespace, repository=repository, file_path=new_file_path)
        else:
            raise PermissionDenied("Illegal Request")
