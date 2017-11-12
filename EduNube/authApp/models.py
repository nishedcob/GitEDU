from django.db import models

from authApp import constants

# Create your models here.


class APIToken(models.Model):
    app_name = models.CharField(max_length=constants.MAX_APP_NAME_LENGTH, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    expires = models.BooleanField(default=False)
    expire_date = models.DateTimeField(default=None, blank=True, null=True)
    secret_key = models.CharField(max_length=constants.SECRET_KEY_SIZE, unique=True)
    token = models.CharField(max_length=constants.TOKEN_SIZE)
