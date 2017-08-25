from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User

from django_app_lti import models as lti_models

from .forms import RegistrationForm

from GitEDU import settings

# Create your views here.

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


class RegistrationView(View):

    form_class = RegistrationForm
    template = 'auth/registration.html'
    role = "Usuario"

    def user_post_registration(self, user):
        pass

    def get(self, request):
        form = self.form_class()
        return render(request=request, template_name=self.template, context={'form': form, 'role': self.role})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            self.user_post_registration(user=user)
            return redirect('auth:login')
        else:
            return render(request=request, template_name=self.template, context={'form': form, 'role': self.role})


class StudentRegistrationView(RegistrationView):

    role = "Estudiante"

    def user_post_registration(self, user):
        pass


class TeacherRegistrationView(RegistrationView):

    role = "Docente"

    def user_post_registration(self, user):
        pass


class LTICredentialsView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            raise PermissionError("No tiene acceso a esta vista hasta que se autentica...")

        lti_expose = settings.LTI_CONFIG_EXPOSE

        lti_cred_json = {}

        if lti_expose['LTI_KEYS']:
            if lti_expose['LTI_ASSIGNMENT_KEY']:
                lti_cred_json['LTI_ASSIGNMENT_KEY'] = {
                    settings.LTI_ASSIGNMENTS_KEY: settings.LTI_OAUTH_CREDENTIALS[settings.LTI_ASSIGNMENTS_KEY]
                }
            if lti_expose['LTI_CLASS_KEY']:
                lti_cred_json['LTI_CLASS_KEY'] = {
                    settings.LTI_CLASSES_KEY: settings.LTI_OAUTH_CREDENTIALS[settings.LTI_CLASSES_KEY]
                }
            if lti_expose['LTI_OTHER_KEYS']:
                lti_cred_json['LTI_OTHER_KEYS'] = settings.LTI_OAUTH_CREDENTIALS

        if lti_expose['LTI_SETUP']:
            lti_cred_json['LTI_SETUP'] = settings.LTI_SETUP

        return JsonResponse(lti_cred_json)
