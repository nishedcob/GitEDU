from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from GitEDU.settings import CODE_PERSISTENCE_BACKEND_MANAGER_CLASS, load_code_persistence_backend_manager
from ideApp.CodePersistenceBackends.MongoDB import mongodb_models as ide_mongodb_models
from ideApp import models as ide_models
from ideApp import forms as ide_forms
from socialApp import models as social_models

# Create your views here.
manager = load_code_persistence_backend_manager(CODE_PERSISTENCE_BACKEND_MANAGER_CLASS)


class UserView(View):

    namespace_form = ide_forms.NamespaceForm
    repository_form = ide_forms.FullRepositoryForm
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
        personal_repos = set(personal_repos)
        groups = []
        group_memberships = social_models.GroupMembership.objects.filter(person=person_obj)
        for group_membership in group_memberships:
            groups.append(group_membership.group)
        groups = set(groups)
        group_repos = []
        for group in groups:
            group_repositories = ide_models.Repository.objects.filter(owning_group=group)
            for_group_repos = {(group_repo.namespace, group_repo.name) for group_repo in group_repositories}
            for_group_repos = for_group_repos - personal_repos
            for group_repo in for_group_repos:
                group_repos.append(group_repo)
        group_repos = set(group_repos)
        group_repos = group_repos - personal_repos
        modified_repos = []
        changes_made = ide_mongodb_models.ChangeModel.objects.raw({'author': username})
        for change_made in changes_made:
            repo = change_made.repository
            ns = repo.namespace
            modified_repos.append((ns.name, repo.name))
        modified_repos = set(modified_repos)
        modified_repos = modified_repos - personal_repos
        modified_repos = modified_repos - group_repos
        tiene_codigo = False
        esCollab = False
        context = self.build_context(username=username, same=same, user=user_obj, tiene_codigo=tiene_codigo,
                                     esCollab=esCollab, personal_repos=personal_repos, group_repos=group_repos,
                                     modified_repos=modified_repos)
        print("context: %s" % context)
        return render(request, self.template, context=context)

    def build_context(self, username, same, user, tiene_codigo, esCollab, personal_repos, group_repos, modified_repos):
        has_personal_repos = len(personal_repos) > 0
        has_group_repos = len(group_repos) > 0
        has_modified_repos = len(modified_repos) > 0
        context = {
            "username": username,
            "same": same,
            "user": user,
            "namespace_form": self.namespace_form(),
            "repository_form": self.repository_form(),
            "tiene_codigo": tiene_codigo,
            "esCollab": esCollab,
            'has_personal_repos': has_personal_repos,
            'has_group_repos': has_group_repos,
            'has_modified_repos': has_modified_repos
        }
        if has_personal_repos:
            context['personal_repos'] = personal_repos
        if has_group_repos:
            context['group_repos'] = group_repos
        if has_modified_repos:
            context['modified_repos'] = modified_repos
        return context
