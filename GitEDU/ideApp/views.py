from django.shortcuts import render

from django.views import View
from django.http import JsonResponse

from django_app_lti import models as lti_models

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


class DecodeView(View):

    def get(self, request, resource_id):
        print("GET %s" % resource_id)
        print(request.user)
        resources = lti_models.LTIResource.objects.filter(id=resource_id)
        for resource in resources:
            courses = lti_models.LTICourse.objects.filter(id=resource.course.id)
            for course in courses:
                print("%s - %s" % (course.course_name_short, course.course_name))
        return JsonResponse(list(resources.values()), safe=False)

    def post(self, request, resource_id):
        print("POST %s" % resource_id)
        pass
