from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse

import json

from EduNube.settings import AUTH_TOKENS_SHOW

from authApp import forms
from authApp.models import APIToken
from authApp.tokens import update_api_token

# Create your views here.


class TokensView(PermissionRequiredMixin, View):

    permission_required = 'auth_admin.manage_tokens'

    form = forms.APITokenForm
    template = 'auth/tokens.html'

    def build_context(self, form=None):
        if form is None:
            raise ValueError("Form can't be None")
        tokens = list(APIToken.objects.all())
        exist_tokens = tokens is not None and len(tokens) > 0
        return {
            'exist_tokens': exist_tokens,
            'tokens': tokens,
            'form': form,
            'show': {
                'app_name': AUTH_TOKENS_SHOW.get('app_name', True),
                'dates': AUTH_TOKENS_SHOW.get('dates', True),
                'date_create': AUTH_TOKENS_SHOW.get('date_create', True),
                'date_edit': AUTH_TOKENS_SHOW.get('date_edit', True),
                'date_expire': AUTH_TOKENS_SHOW.get('date_expire', True),
                'secret': AUTH_TOKENS_SHOW.get('secret', False),
                'token': AUTH_TOKENS_SHOW.get('token', True),
                'full_token': AUTH_TOKENS_SHOW.get('full_token', False),
                'edit': AUTH_TOKENS_SHOW.get('edit', True),
                'delete': AUTH_TOKENS_SHOW.get('delete', True),
                'regenerate_secret': AUTH_TOKENS_SHOW.get('regenerate_secret', True)
            }
        }

    def get(self, request):
        empty_form = self.form()
        context = self.build_context(form=empty_form)
        return render(request, self.template, context)

    def post(self, request):
        form_response = self.form(request.POST)
        if form_response.is_valid():
            api_token = form_response.save(commit=False)
            print(api_token.expire_date)
            api_token.expire_date = api_token.expire_date.__str__()
            print(api_token.expire_date)
            update_api_token(api_token=api_token, regen_secret_key=True)
            # Update a second time to correct timestamp issue
            update_api_token(api_token=api_token, regen_secret_key=False)
        else:
            context = self.build_context(form=form_response)
            return render(request, self.template, context)
        return redirect('auth:tokens')


class TokenView(PermissionRequiredMixin, View):

    permission_required = 'auth_admin.read_tokens'

    template = 'auth/token.html'

    def build_context(self, api_token=None):
        if api_token is None:
            raise ValueError("API_Token can't be None")
        return {
            'app_name': api_token.app_name,
            'created_date': api_token.created_date.__str__(),
            'edit_date': api_token.edit_date.__str__(),
            'expires': api_token.expires,
            'expire_date': api_token.expire_date.__str__(),
            'secret_key': api_token.secret_key,
            'token': api_token.token
        }

    def get(self, request, app_name):
        if app_name is None:
            raise ValueError("App_Name can't be None")
        api_token = APIToken.objects.get(app_name=app_name)
        api_token_dict = self.build_context(api_token=api_token)
        return HttpResponse(json.dumps(api_token_dict), status=200, content_type="application/json")


class DeleteTokenView(PermissionRequiredMixin, View):

    permission_required = 'auth_admin.manage_tokens'

    def get(self, request, app_name):
        if app_name is None:
            raise ValueError("App_Name can't be None")
        api_token = APIToken.objects.get(app_name=app_name)
        api_token.delete()
        return redirect('auth:tokens')


class SecretTokenView(PermissionRequiredMixin, View):

    permission_required = 'auth_admin.manage_tokens'

    def get(self, request, app_name):
        if app_name is None:
            raise ValueError("App_Name can't be None")
        api_token = APIToken.objects.get(app_name=app_name)
        update_api_token(api_token=api_token, regen_secret_key=True)
        return redirect('auth:edit_token', app_name)


class EditTokenView(PermissionRequiredMixin, View):

    permission_required = 'auth_admin.manage_tokens'

    form = forms.APITokenForm
    template = 'auth/token_edit.html'

    def build_context(self, form=None, app_name=None):
        if form is None:
            raise ValueError("Form can't be None")
        context = {
            'form': form
        }
        if app_name is not None:
            context['app_name'] = app_name
        return context

    def get(self, request, app_name):
        api_token = APIToken.objects.get(app_name=app_name)
        token_form = self.form(instance=api_token)
        context = self.build_context(form=token_form, app_name=app_name)
        return render(request, self.template, context)

    def post(self, request, app_name):
        old_token = APIToken.objects.get(app_name=app_name)
        form_response = self.form(request.POST)
        form_response.instance = old_token
        if form_response.is_valid():
            api_token = form_response.save(commit=False)
            print(api_token.expire_date)
            api_token.expire_date = api_token.expire_date.__str__()
            print(api_token.expire_date)
            update_api_token(api_token=api_token, regen_secret_key=False)
        else:
            context = self.build_context(form=form_response)
            return render(request, self.template, context)
        return redirect('auth:tokens')
