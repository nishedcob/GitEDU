from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from django.views import View


class UserView(View):  # TODO

    template = 'social/user.html'

    def get(self, request, user):
        username = user
        same = (request.user.username == username)
        try:
            user_obj = User.objects.get(username=user)
        except ObjectDoesNotExist:
            raise Http404("User %s does not exist" % username)
        tiene_codigo = False
        esCollab = False
        context = self.build_context(username=username, same=same, user=user_obj, tiene_codigo=tiene_codigo,
                                     esCollab=esCollab)
        print("context: %s" % context)
        return render(request, self.template, context=context)

    def build_context(self, username, same, user, tiene_codigo, esCollab):
        return {
            "username": username,
            "same": same,
            "user": user,
            "tiene_codigo": tiene_codigo,
            "esCollab": esCollab
        }
