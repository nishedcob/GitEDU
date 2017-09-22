import json

from django.shortcuts import render
from django.views import View
#from django.http import JsonResponse

#from django_app_lti import models as lti_models
from . import constants
from .forms import CodeForm, CodeGlobalPermissionsForm, AddCollaboratorForm

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

    def get(self, request, namespace, repository, file_path):
        user = request.user.username
        form = self.form_class(initial={'file_name': file_path})
        orig = True
        edits = []
        global_perm_form = self.global_permission_form_class(initial=self.global_permission_initial)
        return render(request, self.template, context={'form': form, 'globalPermForm': global_perm_form,
                                                                   'owner': user, 'orig': orig, 'edits': edits,
                                                                   'new': self.newCode,
                                                                   'editorLang': self.editorLangsAndCode})

    def post(self, request, namespace, repository, file_path):
        pass
