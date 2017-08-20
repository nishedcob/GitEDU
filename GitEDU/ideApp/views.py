from django.shortcuts import render
from django.views import View
#from django.http import JsonResponse

#from django_app_lti import models as lti_models

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
