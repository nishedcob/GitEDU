from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class UserView(View):  # TODO

    def get(self, request, user):
        return HttpResponse("<html><body><h1>%s</h1></body></html>" % user)
