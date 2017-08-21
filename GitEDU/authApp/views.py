from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User

from django_app_lti import models as lti_models

from .forms import RegistrationForm

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

    def get(self, request):
        form = self.form_class()
        return render(request=request, template_name=self.template, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('login')
        else:
            return render(request=request, template_name=self.template, context={'form': form})
