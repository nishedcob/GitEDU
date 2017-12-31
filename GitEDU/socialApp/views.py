from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager
from ideApp import models as ide_models
from socialApp import models as social_models

# Create your views here.
manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)


class UserView(View):  # TODO

    template = 'social/user.html'

    def get(self, request, user):
        username = user
        same = (request.user.username == username)
        try:
            user_obj = User.objects.get(username=user)
        except ObjectDoesNotExist:
            raise Http404("User %s does not exist" % username)
        person_obj = social_models.Person.objects.get_or_create(user=user_obj)[0]
        personal_repositories = ide_models.Repository.objects.filter(owner=person_obj)
        personal_repos = []
        for personal_repository in personal_repositories:
            personal_repos.append((personal_repository.namespace, personal_repository.name))
        tiene_codigo = False
        esCollab = False
        context = self.build_context(username=username, same=same, user=user_obj, tiene_codigo=tiene_codigo,
                                     esCollab=esCollab, personal_repos=personal_repos)
        print("context: %s" % context)
        return render(request, self.template, context=context)

    def build_context(self, username, same, user, tiene_codigo, esCollab, personal_repos):
        has_personal_repos = len(personal_repos) > 0
        context = {
            "username": username,
            "same": same,
            "user": user,
            "tiene_codigo": tiene_codigo,
            "esCollab": esCollab,
            'has_personal_repos': has_personal_repos
        }
        if has_personal_repos:
            context['personal_repos'] = personal_repos
        return context
